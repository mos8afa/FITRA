from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import Member, Picture, Governorate, Goals
from django.template.loader import render_to_string
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner

signer = TimestampSigner()

def register(request):
    if request.method == 'POST':
        name = request.POST.get('full_name')
        age = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('current_weight')
        weight_measure_date = request.POST.get('measurement_date')
        gender = request.POST.get('gender')
        images = request.FILES.getlist('male_photos') 
        sizes = request.POST.get('female_measurements') 
        education = request.POST.get('occupation')
        governorate_name = request.POST.get('place_of_living')
        whatsapp_number = request.POST.get('phone')
        email = request.POST.get('email')
        telegram_username = request.POST.get('telegram_user')
        goals = request.POST.getlist('fitness_goal')
        meals_num = request.POST.get('meals_per_day')
        daily_spend = request.POST.get('food_budget')
        measure_scale = request.POST.get('measuring_scale')
        workout_days = request.POST.get('workout_days')
        training_type = request.POST.get('training_location')
        habits = request.POST.get('habit')
        before_nutrition = request.POST.get('past_nutrition')
        plan = request.POST.get('plan_type')
        injuries = request.POST.get('illness')
        another_sports = request.POST.get('other_sports')
        previous_gym = request.POST.get('gym_before')
        confidence = request.POST.get('confidence')
        comeback = request.POST.get('return_continuity')
        hear_about_us = request.POST.get('how_hear')
        recommend_us = request.POST.get('recommendation_rating')

        existing_member = Member.objects.filter(email=email, is_activated=True).first()
        if existing_member:
            return render(request, 'members/form.html', {
                'alert_message': 'هذا البريد الإلكتروني مستخدم بالفعل. الرجاء استخدام بريد آخر.'
            })

        governorate, _ = Governorate.objects.get_or_create(governorate_name=governorate_name)

        member_info = Member.objects.create(
            name=name,
            age=age,
            height=height,
            weight=weight,
            weight_measure_date=weight_measure_date,
            gender=gender,
            sizes=sizes,
            education=education,
            place=governorate,
            whatsapp_number=whatsapp_number,
            email=email,
            telegram_username=telegram_username,
            plan=plan,
            recommend_us=recommend_us,
            meals_num=meals_num,
            daily_spend=daily_spend,
            measure_scale=measure_scale,
            workout_days=workout_days,
            training_type=training_type,
            habits=habits,
            before_nutrition=before_nutrition,
            injuries=injuries,
            another_sports=another_sports,
            previous_gym=previous_gym,
            confidence=confidence,
            comeback=comeback,
            hear_about_us=hear_about_us
        )

        Goals.objects.bulk_create([
            Goals(member=member_info, goal=goal) for goal in goals
        ])

        if images:
            Picture.objects.bulk_create([
                Picture(member=member_info, images=image) for image in images
            ])

        token = signer.sign(member_info.id)
        activation_link = request.build_absolute_uri(
            reverse('members:activate', kwargs={'token': token})
        )

        subject = 'تفعيل حسابك في Fitra'
        message = render_to_string('members/activation_email.html', {
            'name': name,
            'activation_link': activation_link,
        })

        send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [email], html_message=message)

        return render(request, 'members/form.html', {
            'alert_message': 'تحقق من بريدك الإلكتروني لتفعيل الحساب.'
        })

    return render(request, 'members/form.html')


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
