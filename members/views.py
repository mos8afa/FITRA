from .forms import RegistrationForm
from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from .models import Member, Picture, Governorate, Goals, HearAboutUs

signer = TimestampSigner()


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data

            email = data.get("email")

            if email:
                existing_member = Member.objects.filter(
                    email=email,
                    is_activated=True
                ).first()

                if existing_member:
                    return render(
                        request,
                        "members/form.html",
                        {
                            "form": form,
                            "alert_message": "هذا البريد الإلكتروني مستخدم بالفعل. الرجاء استخدام بريد آخر."
                        },
                    )

            governorate, _ = Governorate.objects.get_or_create(
                governorate_name=data["place_of_living"]
            )

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

            subject = "تفعيل حسابك في Fitra"

            message = render_to_string(
                "members/activation_email.html",
                {
                    "name": data["full_name"],
                    "activation_link": activation_link,
                },
            )

            if email:
                send_mail(
                    subject,
                    "",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    html_message=message,
                )

            return render(
                request,
                "members/form.html",
                {
                    "form": RegistrationForm(),
                    "alert_message": "تحقق من بريدك الإلكتروني لتفعيل الحساب.",
                },
            )

        return render(
            request,
            "members/form.html",
            {
                "form": form,
            },
        )

    return render(
        request,
        "members/form.html",
        {
            "form": RegistrationForm(),
        },
    )

def activate_account(request, token):
    try:
        member_id = signer.unsign(token, max_age=60*60*24)
        member = Member.objects.get(id=member_id)

        if not member.is_activated:
            member.is_activated = True
            member.save()

        return render(request, 'members/activation_success.html')

    except SignatureExpired:
        try:
            unsigned_data = signer.unsign(token)  
            member_id = int(unsigned_data)
            Member.objects.filter(id=member_id, is_activated=False).delete()
        except Exception:
            pass
        return render(request, 'members/activation_failed.html')

    except (BadSignature, Member.DoesNotExist):
        try:
            unsigned_data = signer.unsign(token)
            member_id = int(unsigned_data)
            Member.objects.filter(id=member_id, is_activated=False).delete()
        except Exception:
            pass
        return render(request, 'members/activation_failed.html')
