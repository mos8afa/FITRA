from django import forms
from django.core.validators import RegexValidator
from .models import (
    GENDER, FITNESS_GOAL, MEALS, WORKOUT_DAYS, TRAINING_TYPE, PLAN,
    DAILY_SPENDING, MEAURMENT_SCALE, PREVIOUS_GYM, CONFIDENCE, COMEBACK,
    HEAR_ABOUT_US, RECOMMEND_US, GOVERNORATE,
)

phone_validator = RegexValidator(
    regex=r'^01\d{9}$',
    message='رقم الهاتف يجب أن يبدأ بـ 01 ويتكون من 11 رقم بالضبط.'
)


class RegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=60, required=True)
    age = forms.IntegerField(min_value=10, max_value=100, required=True)
    height = forms.DecimalField(min_value=0, max_value=299.99, decimal_places=2, required=True)
    current_weight = forms.DecimalField(min_value=0, max_value=299.99, decimal_places=2, required=True)
    measurement_date = forms.DateField(required=True)
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect, required=True)

    female_measurements = forms.CharField(widget=forms.Textarea, required=False)

    occupation = forms.CharField(max_length=150, required=True)
    place_of_living = forms.ChoiceField(choices=GOVERNORATE, required=True)

    phone = forms.CharField(max_length=13, required=True, validators=[phone_validator])
    email = forms.EmailField(required=False)
    telegram_user = forms.CharField(max_length=50, required=False)

    fitness_goal = forms.MultipleChoiceField(
        choices=FITNESS_GOAL, widget=forms.CheckboxSelectMultiple, required=True
    )
    meals_per_day = forms.ChoiceField(choices=MEALS, widget=forms.RadioSelect, required=True)
    food_budget = forms.ChoiceField(choices=DAILY_SPENDING, widget=forms.RadioSelect, required=True)
    measuring_scale = forms.ChoiceField(choices=MEAURMENT_SCALE, widget=forms.RadioSelect, required=True)
    workout_days = forms.ChoiceField(choices=WORKOUT_DAYS, widget=forms.RadioSelect, required=True)
    training_location = forms.ChoiceField(choices=TRAINING_TYPE, widget=forms.RadioSelect, required=True)
    habit = forms.CharField(widget=forms.Textarea, required=True)
    past_nutrition = forms.CharField(widget=forms.Textarea, required=True)
    plan_type = forms.ChoiceField(choices=PLAN, widget=forms.RadioSelect, required=True)
    illness = forms.CharField(widget=forms.Textarea, required=True)
    other_sports = forms.CharField(widget=forms.Textarea, required=False)

    gym_before = forms.ChoiceField(choices=PREVIOUS_GYM, widget=forms.RadioSelect, required=True)
    confidence = forms.ChoiceField(choices=CONFIDENCE, widget=forms.RadioSelect, required=True)
    return_continuity = forms.ChoiceField(choices=COMEBACK, widget=forms.RadioSelect, required=True)

    how_hear = forms.MultipleChoiceField(
        choices=HEAR_ABOUT_US, widget=forms.CheckboxSelectMultiple, required=False
    )

    recommendation_rating = forms.TypedChoiceField(
        choices=RECOMMEND_US, coerce=int, widget=forms.RadioSelect, required=True
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        return phone

    def clean(self):
        cleaned_data = super().clean()
        gender = cleaned_data.get('gender')

        if gender == 'MALE':
            photos = self.files.getlist('male_photos')
            if not photos:
                self.add_error(None, 'من فضلك ارفع الصور المطلوبة (4 صور).')
            else:
                for photo in photos:
                    if not photo.content_type.startswith('image/'):
                        self.add_error(None, f'الملف "{photo.name}" ليس صورة صالحة.')
                    if photo.size > 10 * 1024 * 1024:  # 10 MB
                        self.add_error(None, f'حجم الصورة "{photo.name}" أكبر من 10 ميجا.')

        elif gender == 'FEMALE':
            if not cleaned_data.get('female_measurements'):
                self.add_error('female_measurements', 'من فضلك أدخل قياساتك.')

        return cleaned_data