from .forms import RegistrationForm
from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from .models import Member, Picture, Governorate, Goals, HearAboutUs
from datetime import date
from django_ratelimit.decorators import ratelimit
from django.db import transaction
import traceback


signer = TimestampSigner()


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data

            email = data.get("email")

            if email:
                activated_exists = Member.objects.filter(
                    email=email,
                    is_activated=True
                ).exists()

                if activated_exists:
                    form.add_error('email', 'هذا البريد الإلكتروني مستخدم بالفعل. الرجاء استخدام بريد آخر.' if request.LANGUAGE_CODE == 'ar' else 'This email is already in use. Please use another email.')
                    return render(
                        request,
                        "members/form.html",
                        {
                            "form": form,
                            "today": date.today()
                        },
                    )

                
                Member.objects.filter(email=email, is_activated=False).delete()

            with transaction.atomic():                          
                governorate, _ = Governorate.objects.get_or_create(
                    governorate_name=data["place_of_living"]
                )

                current_language = request.LANGUAGE_CODE

                member_info = Member.objects.create(
                    name=data["full_name"],
                    age=data["age"],
                    height=data["height"],
                    weight=data["current_weight"],
                    weight_measure_date=data["measurement_date"],
                    gender=data["gender"],
                    sizes=data.get("female_measurements", ""),
                    education=data["occupation"],
                    place=governorate,
                    whatsapp_number=data["phone"],
                    email=email,
                    telegram_username=data.get("telegram_user"),
                    plan=data["plan_type"],
                    recommend_us=data["recommendation_rating"],
                    meals_num=data["meals_per_day"],
                    daily_spend=data["food_budget"],
                    measure_scale=data["measuring_scale"],
                    workout_days=data["workout_days"],
                    training_type=data["training_location"],
                    habits=data["habit"],
                    before_nutrition=data["past_nutrition"],
                    injuries=data["illness"],
                    another_sports=data.get("other_sports"),
                    previous_gym=data["gym_before"],
                    confidence=data["confidence"],
                    comeback=data["return_continuity"],
                    preferred_language=current_language,  
                )

            
                Goals.objects.bulk_create([
                    Goals(member=member_info, goal=goal)
                    for goal in data["fitness_goal"]
                ])

                HearAboutUs.objects.bulk_create([
                    HearAboutUs(
                        member=member_info,
                        source=source
                    )
                    for source in data["how_hear"]
                ])

                images = request.FILES.getlist("male_photos")
                if images:
                    Picture.objects.bulk_create([
                        Picture(member=member_info, images=image)
                        for image in images
                    ])

            token = signer.sign(member_info.id)

            activation_link = request.build_absolute_uri(
                reverse(
                    "members:activate",
                    kwargs={"token": token},
                )
            )

            subject = "تفعيل حسابك في Fitra" if current_language == 'ar' else "Activate Your Fitra Account"

            message = render_to_string(
                "members/activation_email.html",
                {
                    "name": data["full_name"],
                    "activation_link": activation_link,
                    "language": current_language,
                },
            )

            email_sent = False
            email_error = None
            
            if email:
                try:
                    send_mail(
                        subject,
                        "",
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        html_message=message,
                        fail_silently=False,
                    )
                    email_sent = True
                except Exception as e:
                    email_error = str(e)
                    traceback.print_exc()

            if email and email_sent:
                success_message = "تم إنشاء حسابك بنجاح! تحقق من بريدك الإلكتروني لتفعيل الحساب." if current_language == 'ar' else "Account created successfully! Check your email to activate your account."
            elif email and not email_sent:
                success_message = f"تم إنشاء حسابك ولكن فشل إرسال البريد الإلكتروني. الرجاء التواصل مع الدعم." if current_language == 'ar' else f"Account created but email failed to send. Please contact support. Error: {email_error}"
            else:
                success_message = "تم إنشاء حسابك بنجاح! لم يتم توفير بريد إلكتروني للتفعيل." if current_language == 'ar' else "Account created successfully! No email provided for activation."
            
            return render(
                request,
                "members/form.html",
                {
                    "form": RegistrationForm(),
                    "success_message": success_message,
                    "today": date.today()
                },
            )

        return render(
            request,
            "members/form.html",
            {
                "form": form,
                "today": date.today()
            },
        )

    return render(
        request,
        "members/form.html",
        {
            "form": RegistrationForm(),
            "today": date.today()
        },
    )

def activate_account(request, token):
    try:
        member_id = signer.unsign(token, max_age=60*60*24)
        member = Member.objects.get(id=member_id)

        if not member.is_activated:
            member.is_activated = True
            member.save()

        return render(request, 'members/activation_success.html', {'member': member})

    except SignatureExpired:
        try:
            unsigned_data = signer.unsign(token)  
            member_id = int(unsigned_data)
            member = Member.objects.filter(id=member_id, is_activated=False).first()
            preferred_language = member.preferred_language if member else 'en'
            member.delete() if member else None
        except Exception:
            preferred_language = 'en'
        return render(request, 'members/activation_failed.html', {'preferred_language': preferred_language})

    except (BadSignature, Member.DoesNotExist):
        try:
            unsigned_data = signer.unsign(token)
            member_id = int(unsigned_data)
            member = Member.objects.filter(id=member_id, is_activated=False).first()
            preferred_language = member.preferred_language if member else 'en'
            member.delete() if member else None
        except Exception:
            preferred_language = 'en'
        return render(request, 'members/activation_failed.html', {'preferred_language': preferred_language})


def ratelimited_view(request, exception):
    message = "لقد قمت بمحاولات كثيرة جداً. الرجاء المحاولة لاحقاً." if request.LANGUAGE_CODE == 'ar' else "Too many attempts. Please try again later."
    return render(request, "members/form.html", {
        "form": RegistrationForm(),
        "error_message": message,
        "today": date.today()
    }, status=429)