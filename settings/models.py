from django.db import models

class Info(models.Model):
    logo = models.ImageField(verbose_name = 'Logo', upload_to = 'settings/')
    slogan = models.CharField(verbose_name ='Slogan', max_length = 200 )

class Brief(models.Model): 
    home = models.OneToOneField(Info, on_delete = models.CASCADE, related_name = 'info_brief')   
    brief_title = models.CharField(verbose_name ='Brief Title', max_length = 100 )
    brief_content = models.TextField(verbose_name ='Brief')
    brief_image = models.ImageField(verbose_name = 'Brief Image', upload_to ='settings/') 

class AboutUs(models.Model):
    home = models.OneToOneField(Info, on_delete = models.CASCADE, related_name = 'info_about_us')
    about_us_content =  models.TextField(verbose_name ='About Us')
    about_us_image = models.ImageField(verbose_name ='About US Image', upload_to='settings/')

class Footer(models.Model):
    home = models.OneToOneField(Info, on_delete = models.CASCADE, related_name = 'info_footer')
    footer_slogan = models.CharField(verbose_name ='Footer Slogan', max_length = 200 )
    footer_image = models.ImageField(verbose_name = 'Footer Image', upload_to ='settings/')

class SocialLinks(models.Model):
    home = models.OneToOneField(Info, on_delete = models.CASCADE, related_name = 'info_links')
    youtube = models.URLField(verbose_name ='Youtube Link', max_length = 100, blank=True)  
    whatsapp = models.URLField(verbose_name ='Whatsapp Link', max_length = 100, blank=True)   
    facebook = models.URLField(verbose_name ='Facebook Link', max_length = 100, blank=True)
    instagram = models.URLField(verbose_name ='Instagram Link', max_length = 100, blank=True)
    instagram_page = models.URLField(verbose_name ='Instagram Page Link', max_length = 100, blank=True)
    tiktok = models.URLField(verbose_name ='Tiktok Link', max_length = 100, blank=True)
    telegram = models.URLField(verbose_name ='Telegram Link', max_length = 100, blank=True)

class SuccessfullStories(models.Model):
    name = models.CharField(verbose_name = 'Name', max_length = 200)
    before_image = models.ImageField(verbose_name = 'Before Image', upload_to ='settings/') 
    after_image = models.ImageField(verbose_name = 'After Image', upload_to ='settings/') 
    def __str__(self):
        return self.name

class PackadgeAdvantage(models.Model):
    advantages = models.TextField(verbose_name = 'Pack Advantages')
    def __str__(self):
        return self.advantages

class PackadgeDisadvantage(models.Model):
    disadvantages = models.TextField(verbose_name = 'Pack Disadvantages')
    def __str__(self):
        return self.disadvantages

class Packadges(models.Model):
    name  = models.CharField(verbose_name = 'Packadge', max_length = 200)
    before_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    after_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    time = models.CharField(verbose_name = 'Duration', max_length = 100)
    image = models.ImageField(verbose_name ='Packadge Image', upload_to='settings/')
    advantages = models.ManyToManyField(PackadgeAdvantage, blank = True, null = True, related_name = 'packadge_pros')
    disadvantages = models.ManyToManyField(PackadgeDisadvantage, blank = True, null = True, related_name = 'packadge_cons')
    

    

