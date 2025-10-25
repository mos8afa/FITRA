from django.contrib import admin
from .models import Governorate, RoutineDetails, Goals, BasicInfo, Picture


class PictureInline(admin.TabularInline):
    model = Picture
    extra = 1
    readonly_fields = ['images']


class GoalsInline(admin.TabularInline):
    model = Goals
    extra = 1


class RoutineDetailsInline(admin.StackedInline):
    model = RoutineDetails
    extra = 0
    show_change_link = True
    fieldsets = (
        ('Training & Nutrition Info', {
            'fields': (
                'meals_num',
                'training_type',
                'workout_days',
                'daily_spend',
                'measure_scale',
                'before_nutrition',
                'injuries',
                'previous_gym',
                'another_sports',
                'habits',
            )
        }),
        ('Mindset & Motivation', {
            'fields': (
                'confidence',
                'comeback',
                'hear_about_us',
            )
        }),
    )


@admin.register(BasicInfo)
class BasicInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'plan', 'place', 'join_date', 'recommend_us')
    list_filter = ('gender', 'plan', 'place', 'join_date')
    search_fields = ('name', 'email', 'whatsapp_number')
    readonly_fields = ('join_date', 'weight_measure_date')

    fieldsets = (
        ('Personal Information', {
            'fields': (
                'name',
                'age',
                'gender',
                'education',
                'place',
                'plan',
                'recommend_us',
            )
        }),
        ('Physical Data', {
            'fields': (
                'height',
                'weight',
                'weight_measure_date',
                'sizes',
            )
        }),
        ('Contact Details', {
            'fields': (
                'whatsapp_number',
                'email',
                'telegram_username',
            )
        }),
        ('Routine Details', {
            'fields': ('routine_details',)
        }),
    )

    inlines = [GoalsInline, PictureInline]


@admin.register(Governorate)
class GovernrateAdmin(admin.ModelAdmin):
    list_display = ('governorate_name',)
    search_fields = ('governorate_name',)


@admin.register(RoutineDetails)
class RoutineDetailsAdmin(admin.ModelAdmin):
    list_display = ('training_type', 'workout_days', 'daily_spend', 'previous_gym', 'confidence')
    list_filter = ('training_type', 'workout_days', 'confidence')
    search_fields = ('before_nutrition', 'injuries')


@admin.register(Goals)
class GoalsAdmin(admin.ModelAdmin):
    list_display = ('member', 'goal')
    list_filter = ('goal',)
    search_fields = ('member__name', 'goal')


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('member', 'images')
    search_fields = ('member__name',)