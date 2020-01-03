from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from languages.fields import LanguageField

class Profile(models.Model):
    USER = 'User'
    AUTHOR = 'Author'
    EDITOR = 'Editor'
    ROLE_CHOICES = (
        (USER, 'User'),
        (AUTHOR, 'Author'),
        (EDITOR, 'Editor'),
    )
    HIGH_SCHOOL = 'High School'
    UNIVERSITY = 'University'
    MASTER_DEGRE = 'Master Degree'
    PHD = 'Phd'
    ROLE_CHOICES1 = (
        (HIGH_SCHOOL, 'High School'),
        (UNIVERSITY, 'University'),
        (MASTER_DEGRE, 'Master Degree'),
        (PHD, 'Phd'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    image = models.ImageField(default='media/profile_pics/default.jpg', upload_to='profile_pics')    
    role = models.CharField(max_length=30,choices=ROLE_CHOICES, null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)    
    education = models.CharField(max_length=50 ,choices=ROLE_CHOICES1, null=True, blank=True)
    language = LanguageField(max_length=30,blank=True, help_text='The languages that you can speak')
    profession = models.CharField(max_length=50,blank=True, help_text='Profession')
    phone = PhoneNumberField(blank=True, help_text='Contact phone number')
    email = models.CharField(max_length=50, blank=True)
    biography = models.TextField(max_length=500, blank=True,  help_text='Biography')
    
    def __str__(self): 
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

# Create your models here.
