from django import forms
from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from . import models

class PackadgesForm(forms.ModelForm):
    class Meta:
        model = models.Packadges
        fields = '__all__'
        widgets = {
            'advantages': forms.CheckboxSelectMultiple,
            'disadvantages': forms.CheckboxSelectMultiple,
        }

class SomeModelAdmin(SummernoteModelAdmin, TranslationAdmin):
    summernote_fields = '__all__'

class PacksAdmin(SummernoteModelAdmin, TranslationAdmin):
    summernote_fields = '__all__'
    list_display = ['name']
    form = PackadgesForm   

admin.site.register(models.Info, SomeModelAdmin)
admin.site.register(models.Brief, SomeModelAdmin)
admin.site.register(models.AboutUs, SomeModelAdmin)
admin.site.register(models.Footer)
admin.site.register(models.SocialLinks)
admin.site.register(models.SuccessfullStories)
admin.site.register(models.Packadges, PacksAdmin)
admin.site.register(models.PackadgeAdvantage, TranslationAdmin)
admin.site.register(models.PackadgeDisadvantage, TranslationAdmin)
