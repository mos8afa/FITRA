from django.shortcuts import render
from . import models 

def home(request):
    info = models.Info.objects.last()
    brief = models.Brief.objects.last()
    about_us = models.AboutUs.objects.last()
    footer = models.Footer.objects.last()
    social_links = models.SocialLinks.objects.last()
    successful_stories = models.SuccessfullStories.objects.all().order_by('-id')[:10]
    packadges = models.Packadges.objects.all()
    
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
