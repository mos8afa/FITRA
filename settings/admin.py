from django import forms
from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from . import models
from solo.admin import SingletonModelAdmin
from adminsortable2.admin import SortableTabularInline, SortableAdminBase


class SingletonSummernoteAdmin(SummernoteModelAdmin, TranslationAdmin, SingletonModelAdmin):
    summernote_fields = '__all__'

class PackadgeFeatureInline(SortableTabularInline):
    model = models.PackadgeFeature
    extra = 1

class PacksAdmin(SortableAdminBase, SummernoteModelAdmin, TranslationAdmin):
    summernote_fields = '__all__'
    list_display = ['name']
    inlines = [PackadgeFeatureInline]

admin.site.register(models.Info, SingletonSummernoteAdmin)
admin.site.register(models.Brief, SingletonSummernoteAdmin)
admin.site.register(models.AboutUs, SingletonSummernoteAdmin)
admin.site.register(models.Footer, SingletonSummernoteAdmin)
admin.site.register(models.SocialLinks, SingletonModelAdmin)

admin.site.register(models.SuccessfullStories)
admin.site.register(models.Packadges, PacksAdmin)
admin.site.register(models.Feature, TranslationAdmin)