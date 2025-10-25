from django.shortcuts import render, redirect
from .models import BasicInfo, Picture, RoutineDetails, Governrate


def register(request):
    if request.method == 'POST':
        name = request.POST.get('full_name')
        age = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('current_weight')
        weight_measure_date = request.POST.get('measurement_date')
        gender = request.POST.get('gender')
        images = request.FILES.getlist('male_photos')
        sizes = request.POST.get('female_measurements') if gender == 'female' else None
        education = request.POST.get('occupation')
        governrate_name = request.POST.get('place_of_living')
        whatsapp_number = request.POST.get('phone')
        email = request.POST.get('email')
        telegram_username = request.POST.get('telegram_user')
        goal = request.POST.get('fitness_goal')
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

        routine = RoutineDetails.objects.create(
            goal=goal,
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
        governrate = Governrate.objects.get_or_create(
            governrate_name, _ =governrate_name
        )

        member_info = BasicInfo.objects.create(
            name=name,
            age=age,
            height=height,
            weight=weight,
            weight_measure_date=weight_measure_date,
            gender=gender,
            sizes=sizes,
            education=education,
            place=governrate,
            whatsapp_number=whatsapp_number,
            email=email,
            telegram_username=telegram_username,
            plan=plan,
            recommend_us=recommend_us,
            routine_details=routine
        )

        Picture.objects.bulk_create([Picture(member=member_info, images=image) for image in images])

        return redirect('home')
    
    return render(request, 'members/form.html')

