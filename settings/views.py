from django.shortcuts import render
from . import models 

def home(request):
    info = models.Info.get_solo()
    brief = models.Brief.get_solo()
    about_us = models.AboutUs.get_solo()
    footer = models.Footer.get_solo()
    social_links = models.SocialLinks.get_solo()
    successful_stories = models.SuccessfullStories.objects.all().order_by('-id')[:10]
    packadges = models.Packadges.objects.prefetch_related('advantages', 'disadvantages').all()
    slogan_words = footer.footer_slogan.split()

    words = slogan_words[:7]            
    b_word = slogan_words[7:8]       
    words2 = slogan_words[8:]            

    word_string = " ".join(words)
    b_word_string = " ".join(b_word)
    word_string2 = " ".join(words2)

    return render(request, 'settings/home.html', {
        'info': info,
        'brief': brief,
        'about_us': about_us,
        'footer': footer,
        'social_links': social_links,
        'footer_slogan': word_string,
        'footer_slogan_2': word_string2,
        'broken_word': b_word_string,
        'successful_stories':successful_stories,
        'packadges':packadges,
    })