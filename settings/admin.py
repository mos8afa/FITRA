from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin


from . import models

class SomeModelAdmin(SummernoteModelAdmin): 
    summernote_fields = '__all__'

class StoriesAndPacksAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    list_display = ['name']

admin.site.register(models.Info,SomeModelAdmin)
admin.site.register(models.Brief,SomeModelAdmin)
admin.site.register(models.AboutUs,SomeModelAdmin)
admin.site.register(models.Footer)
admin.site.register(models.SocialLinks)
admin.site.register(models.SuccessfullStories,StoriesAndPacksAdmin)
admin.site.register(models.Packadges,StoriesAndPacksAdmin)
admin.site.register(models.PackadgeAdvantage)
admin.site.register(models.PackadgeDisadvantage)


