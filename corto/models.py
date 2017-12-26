from django.db import models

#done with user authentication
class User(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    def __str__(self):
        return str(self.id)
    def __unicode__(self):
        return str(self.id)

class Urls(models.Model):
    original = models.CharField(max_length=1000)
    shortan = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    clicks = models.IntegerField(default=0)
    def __str__(self):
        return str(self.original)+","+str(self.shortan)

class User_urls(models.Model):
    url_id = models.ForeignKey('Urls', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)

class Browser_url(models.Model):
    browser_token = models.CharField(max_length=1000)
    url_id = models.ForeignKey('Urls', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)

class Click(models.Model):
    urlId =  models.ForeignKey('Urls', on_delete=models.CASCADE)
    platform = models.CharField(max_length=100)
    browser = models.CharField(max_length=100)
    device = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    def __str__(self):
        return str(self.id)
