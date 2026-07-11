from modeltranslation.translator import register, TranslationOptions
from . import models

@register(models.Brief)
class BriefTranslationOptions(TranslationOptions):
    fields = ('brief_title', 'brief_content') 

@register(models.Info)
class InfoTranslationOptions(TranslationOptions):
    fields = ('slogan',) 

@register(models.AboutUs)
class AboutUsTranslationOptions(TranslationOptions):
    fields = ('about_us_content',) 

@register(models.Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ('text',)
    
@register(models.Packadges)
class PackadgesTranslationOptions(TranslationOptions):
    fields = ('name','time',)

@register(models.Footer)
class FooterTranslationOptions(TranslationOptions):
    fields = ('footer_slogan',)