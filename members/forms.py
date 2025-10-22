from django import forms
from .models import BasicInfo, RoutineDetails, Picture, Size

class MemberForm(forms.ModelForm):
    class Meta:
        model = BasicInfo
        fields = '__all__'
        exclude = ['routine_details','pictures','sizes','join_date']
        labels = {
            'name':'Full Name',
            'age' : 'Age',
            'height' : 'Height (CM)',
            'weight':'Current Weight (KG)',
            'weight_measure_date':'Weight Measurement Date',
            'gender':'Gender',
            'education':'Occupation or Academic Year',
            'place':'Place Of Living',
            'whatsapp_number':'Phone Number (with WhatsApp)',
            'email':'Email (Optional)',
            'telegram_username':'Telegram User (Optional)', 
            'plan':'Your Plan',
            'recommend_us':'How do you recommend us to a friend?',
        }
        wedgets = {
            'name':forms.TextInput(attrs={ 'class':"w-full p-3 border-2 border-gray-600 rounded-lg focus:border-main-fitra focus:ring focus:ring-main-fitra/50 transition duration-150", 'placeholder':"Enter your full name"}),
            'age':forms.NumberInput(attrs={'class':"w-full p-3 border-2 border-gray-600 rounded-lg focus:border-main-fitra focus:ring focus:ring-main-fitra/50 transition duration-150", 'placeholder':"Enter your age (number)"}),
            'height':forms.NumberInput(attrs={'class':"w-full p-3 border-2 border-gray-600 rounded-lg focus:border-main-fitra focus:ring focus:ring-main-fitra/50 transition duration-150", 'placeholder':"Enter your height in CM"}),
            'weight':forms.NumberInput(attrs={'class':"w-full p-3 border-2 border-gray-600 rounded-lg focus:border-main-fitra focus:ring focus:ring-main-fitra/50 transition duration-150", 'placeholder':"Enter your current weight in KG"}),
            'weight_measure_date':forms.NumberInput(attrs={'class':"w-full p-3 border-2 border-gray-600 rounded-lg focus:border-main-fitra focus:ring focus:ring-main-fitra/50 transition duration-150"}),
            'education':forms.TextInput(attrs={'class':"w-full p-3 border-2 border-gray-600 rounded-lg focus:border-main-fitra focus:ring focus:ring-main-fitra/50 transition duration-150", 'placeholder':"e.g., Engineer, 4th Year Science"}),
            'whatsapp_number':forms.NumberInput(attrs={'class':"w-full p-3 border-2 border-gray-600 rounded-lg focus:border-main-fitra focus:ring focus:ring-main-fitra/50 transition duration-150", 'placeholder':"e.g., 01XXXXXXXXX"}),
            'email':forms.EmailInput(attrs={'class':"w-full p-3 border-2 border-gray-600 rounded-lg focus:border-main-fitra focus:ring focus:ring-main-fitra/50 transition duration-150", 'placeholder':"Your answer"}),
            'telegram_username':forms.TextInput(attrs={'class':"w-full p-3 border-2 border-gray-600 rounded-lg focus:border-main-fitra focus:ring focus:ring-main-fitra/50 transition duration-150", 'placeholder':"Like @example"}),
        }

class RoutineDetailsForm(forms.ModelForm):
    class Meta:
        model =RoutineDetails
        fields = '__all__'
        labels = {
            'goal':'Fitness Goal',
            'meals_num':'How many meals can you eat per day?',
            'daily_spend':'How much can you spend daily on your training food?',
            'measure_scale':'Do you have a measuring scale or would you measure with spoons (not accurate)?',
            'workout_days':'Available days for workout?',
            'training_type':'Do you seek training at home or at the gym?',
            'habits':'Do you have any daily or weekly habit (good or bad)?',
            'before_nutrition':'Tell me about your nutrition in the past 6-3 months (How many meals, type of food)',
            'injuries':'Do you suffer from any illness or injury that affects your performance (If Yes explain)',
            'another_sports':'Do You Play Any Sports Besides the gym (If Yes explain) ',
            'previous_gym':'Have You Ever Hit The GYM Before?',
            'confidence':'Are You Confident Enough to Take Up a Sports Lifestyle',
            'comeback':'In Case of Lack of Continuity, Will You Come Back Again?',
            'hear_about_us':'How did you hear about "FITRA"?',

        }

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = '__all__'
        labels = {
            'side1':'Side 1',
            'side2':'Side 2',
            'front':'Front',
            'back':'Back',
        }

class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = '__all__'
        labels = {
            'right_arm':'Right Arm',
            'left_arm':'Left Arm',
            'right_thigh':'Right Thigh',
            'left_thigh':'Left Tigh',
            'waist':'Waist',
            'belly':'Belly from level of umbilicus',
            'chest':'Chest',
        }