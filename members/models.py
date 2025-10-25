from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _


GENDER = [
    ('MALE','Male'),
    ('FEMALE','Female'),
]

FITNESS_GOAL = [
    ('FAT LOSS','Fat loss'),
    ('INCREASE MUSCLE MASS','Increase muscle mass'),
    ('INCREASE STRENTH','Increase strenth'),
    ('INCREASE ENDURANCE','Increase endurance'),
    ('TRAIN FOR FUNCTIONALITY','Train for functionality'),
    ('HAVING FUN','Having fun'),
    ('POST REHABILITATION STRENTH','Post rehabilitation strenth'),
]

MEALS = [
    ('A MEAL','A meal'),
    ('2 MEALS','2 meals'),
    ('3 MEALS','3 meals'),
    ('4 MEALS','4 meals'),
    ('5 MEALS','5 meals'),

]

WORKOUT_DAYS = [ 
    ('A DAY','A day'),
    ('2 DAYS','2 days'),
    ('3 DAYS','3 days'),
    ('4 DAYS','4 days'),
    ('5 DAYS','5 days'),
    ('6 DAYS','6 days'),
]

TRAINING_TYPE = [
    ('GYM','Gym'),
    ('HOME','Home'),
]

PLAN = [
    ('RARE','Rare'),
    ('EPIC','Epic'),
    ('LEGENDARY','Legendary'),
]

DAILY_SPENDING = [
    ('LESS THAN 100 BUCKS', 'Less than 100 bucks'),
    ('100-150 BUCKS','100-150 bucks'),
    ('150-200 BUCKS','150-200 bucks'),
    ('MORE THAN 200 BUCKS','More then 200 bucks'),
]

MEAURMENT_SCALE = [
    ('I DO HAVE','I do have'),
    ('I DO NOT HAVE','I do not have'),
    ('NO, BUT I WILL','No, but i will'),
]

PREVIOUS_GYM = [
    ('YES','Yes'),
    ('NO','No'),
]

CONFIDENCE = [
    ('ABSOLUTELY','Absolutely'),
    ('MAYBE','Maybe'),
    ('NO','No'),
]

COMEBACK = [
    ('ABSOLUTELY','Absolutely'),
    ('NOT SURE','Not sure'),
]

HEAR_ABOUT_US = [
    ('A FRIEND','A friend'),
    ('FACEBOOK','Facebook'),
    ('INSTAGRAM','Instagram'),
    ('TIKTOK','Tiktok'),
    ('OTHER','Other'),
]

RECOMMEND_US = [
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
]

GOVERNORATE = [
    ("Alexandria","Alexandria"),
    ("Aswan","Aswan"),
    ("Asyut","Asyut"),
    ('Beheira','Beheira'),
    ('Beni Suef','Beni Suef'),
    ("Cairo","Cairo"),
    ("Dakahlia","Dakahlia"),
    ("Damietta","Damietta"),
    ("Faiyum","Faiyum"),
    ("Gharbia","Gharbia"),
    ("Giza","Giza"),
    ("Ismailia","Ismailia"),
    ("Kafr El Sheikh","Kafr El Sheikh"),
    ("Luxor","Luxor"),
    ("Matruh","Matruh"),
    ("Minya","Minya"),
    ("Monufia","Monufia"),
    ("New Valley",'New Valley (Wadi El Gedid)'),
    ("North Sinai","North Sinai"),
    ("Port Said","Port Said"),
    ("Qalyubia","Qalyubia"),
    ("Qena","Qena"),
    ("Red Sea","Red Sea"),
    ("Sharqia","Sharqia"),
    ("Sohag","Sohag"),
    ("South Sinai","South Sinai"),
    ("Suez","Suez"),
]

class Governorate(models.Model):
    governorate_name = models.CharField(verbose_name=_('Governrate name'), max_length=30, choices=GOVERNORATE)
    def __str__(self):
        return self.governorate_name

class RoutineDetails(models.Model):
    meals_num = models.CharField(verbose_name=_('Meals number'), max_length=7, choices=MEALS)
    training_type = models.CharField(verbose_name=_('Gym or home'), max_length=4, choices=TRAINING_TYPE)
    workout_days = models.CharField(verbose_name=_('Workout available days'), max_length=6, choices=WORKOUT_DAYS)
    daily_spend = models.CharField(verbose_name=_('Daily spend'), max_length=20, choices=DAILY_SPENDING)
    measure_scale = models.CharField(verbose_name=_('Having measurement scale'), max_length=15, choices=MEAURMENT_SCALE)
    before_nutrition = models.TextField(verbose_name=_('Previous Nutrition'))
    injuries = models.TextField(verbose_name=_('Injuries'))
    previous_gym = models.CharField(verbose_name=_('Previous gym'), max_length=3, choices=PREVIOUS_GYM)
    another_sports = models.TextField(verbose_name=_('Another Sports'), blank=True, null= True)
    habits = models.TextField(verbose_name=_('Any Habits'))
    confidence = models.CharField(verbose_name=_('Confidence'), max_length=10, choices=CONFIDENCE)
    comeback = models.CharField(verbose_name=_('Comeback'), max_length=10, choices=COMEBACK)
    hear_about_us = models.CharField(verbose_name=_('Hear about us'), max_length=10, choices=HEAR_ABOUT_US)


class BasicInfo(models.Model):
    join_date = models.DateField(verbose_name=_('Join Date'), auto_now_add=True)
    name = models.CharField(verbose_name=_('Name'), max_length=60)
    age = models.PositiveSmallIntegerField(verbose_name=_('Age'))
    height = models.DecimalField(verbose_name=_('Height (cm)'), max_digits=5, decimal_places=2)
    weight = models.DecimalField(verbose_name=_('Weight (kg)'), max_digits=5, decimal_places=2)
    weight_measure_date = models.DateField(verbose_name=_('Weight Measurement Date'), default= datetime.date.today)
    whatsapp_number = models.CharField(verbose_name=_('Whatsapp Number'), max_length=13)
    email = models.EmailField(verbose_name=_('Email'))
    telegram_username = models.CharField(verbose_name=_('Telegram User'), max_length=50, blank=True, null=True)
    place = models.ForeignKey(Governorate,on_delete=models.PROTECT, related_name='user_governorate')
    gender = models.CharField(verbose_name=_('Gender'), max_length=6, choices=GENDER)
    education = models.CharField(verbose_name=_('Education'), max_length=150)
    sizes = models.TextField(null=True, blank=True)
    plan = models.CharField(verbose_name=_('Plan'), max_length=9, choices=PLAN)
    recommend_us = models.IntegerField(verbose_name=_('Recommend us'), choices=RECOMMEND_US)
    routine_details = models.OneToOneField(RoutineDetails, on_delete= models.CASCADE, related_name= 'user_routine_details')
    def __str__(self):
        return self.name

class Goals(models.Model):
    member = models.ForeignKey(BasicInfo,on_delete=models.CASCADE, related_name='user_goals')
    goal = models.CharField(verbose_name=_('Fitness Goal'), max_length=30, choices=FITNESS_GOAL)

class Picture(models.Model):
    member = models.ForeignKey(BasicInfo,on_delete=models.CASCADE, related_name='user_images')
    images = models.ImageField(verbose_name=_('images'), upload_to='members/', null=True, blank=True)


    



