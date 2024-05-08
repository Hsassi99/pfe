from django.db import models
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
# Create your models here.
class Drone(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=15)
    port = models.IntegerField()

    def __str__(self):
        return self.name
class usr (models.Model):
    usr_name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())



from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
