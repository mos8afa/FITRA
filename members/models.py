from django.db import models
import datetime

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

class Governrate(models.Model):
    name = models.CharField(verbose_name='Governrate name', max_length=50)
    def __str__(self):
        return self.name

class Picture(models.Model):
    side1 = models.ImageField(verbose_name='Side 1 photo', upload_to='members/')
    side2 = models.ImageField(verbose_name='Side 2 photo', upload_to='members/')
    front = models.ImageField(verbose_name='Front photo', upload_to='members/')
    back = models.ImageField(verbose_name='Back photo', upload_to='members/')

class Size(models.Model):
    right_arm = models.CharField(verbose_name='Right Arm', max_length=4)
    left_arm = models.CharField(verbose_name='Left Arm', max_length=4)
    right_thigh = models.CharField(verbose_name='Right Thigh', max_length=4)
    left_thigh = models.CharField(verbose_name='Left Thigh', max_length=4)
    waist = models.CharField(verbose_name='Waist', max_length=4)
    belly = models.CharField(verbose_name='Belly', max_length=4)
    chest = models.CharField(verbose_name='Chest', max_length=4)

class RoutineDetails(models.Model):
    goal = models.CharField(verbose_name='Fitness Goal', max_length=30, choices=FITNESS_GOAL)
    meals_num = models.CharField(verbose_name='Meals number', max_length=7, choices=MEALS)
    training_type = models.CharField(verbose_name='Gym or home', max_length=4, choices=TRAINING_TYPE)
    workout_days = models.CharField(verbose_name='Workout available days', max_length=6, choices=WORKOUT_DAYS)
    daily_spend = models.CharField(verbose_name='Daily spend', max_length=20, choices=DAILY_SPENDING)
    measure_scale = models.CharField(verbose_name='Having measurement scale', max_length=15, choices=MEAURMENT_SCALE)
    before_nutrition = models.TextField(verbose_name='Previous Nutrition')
    injuries = models.TextField(verbose_name='Injuries')
    previous_gym = models.CharField(verbose_name='Previous gym', max_length=3, choices=PREVIOUS_GYM)
    another_sports = models.TextField(verbose_name='Another Sports')
    habits = models.TextField(verbose_name='Any Habits')
    confidence = models.CharField(verbose_name='Confidence', max_length=10, choices=CONFIDENCE)
    comeback = models.CharField(verbose_name='Comeback', max_length=10, choices=COMEBACK)
    hear_about_us = models.CharField(verbose_name='Hear about us', max_length=10, choices=HEAR_ABOUT_US)

class BasicInfo(models.Model):
    name = models.CharField(verbose_name='Name', max_length=60)
    age = models.PositiveSmallIntegerField(verbose_name='Age')
    height = models.DecimalField(verbose_name='Height (cm)', max_digits=5, decimal_places=2)
    weight = models.DecimalField(verbose_name='Weight (kg)', max_digits=5, decimal_places=2)
    weight_measure_date = models.DateField(verbose_name='Weight Measurement Date', default= datetime.date.today)
    whatsapp_number = models.CharField(verbose_name='Whatsapp Number', max_length=13)
    email = models.EmailField(verbose_name='Email')
    telegram_username = models.CharField(verbose_name='Telegram User', max_length=50, blank=True, null=True)
    place = models.ForeignKey(Governrate,on_delete=models.PROTECT, related_name='user_governrate')
    gender = models.CharField(verbose_name='Gender', max_length=6, choices=GENDER)
    education = models.CharField(verbose_name='Education', max_length=150)
    pictures = models.OneToOneField(Picture, on_delete=models.CASCADE, related_name='user_pictures', null=True, blank=True)
    sizes = models.OneToOneField(Size, on_delete=models.CASCADE, related_name='user_body_size',null=True, blank=True)
    plane = models.CharField(verbose_name='Plan', max_length=9, choices=PLAN)
    recommend_us = models.IntegerField(verbose_name='Recommend us', choices=RECOMMEND_US)
    routine_details = models.OneToOneField(RoutineDetails, on_delete= models.CASCADE, related_name= 'user_routine_details')
    def __str__(self):
        return self.name
    



    



