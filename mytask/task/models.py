from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.forms.extras import SelectDateWidget 


class Task(models.Model):
	name = models.CharField(max_length=200)
	desc = models.TextField()
	created = models.DateField(default = datetime.today())
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.name

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	secondary_email = models.CharField(max_length=120)
	gender = models.CharField(max_length=2)

class UserForm(ModelForm):
	username = forms.CharField(error_messages={'required':'Please enter UserName'})
	password = forms.CharField(error_messages={'required':'Please enter Password'})
	email = forms.EmailField(error_messages={'required':'Please enter Email'})
	first_name = forms.CharField(error_messages={'required':'Please enter FirstName'})
	last_name = forms.CharField(error_messages={'required':'Please enter LastName'})
	
	class Meta:
		model = User
		fields = ['username','password','email','first_name','last_name']

class UserProfileForm(ModelForm):
	SEX = ((u'M',u'Male'),(u'F',u'Female'),)
	secondary_email = forms.EmailField(error_messages={'required':'Please enter SecondaryEmail'})
	gender = forms.ChoiceField(error_messages={'required':'Please enter Gender'},choices=SEX)

	class Meta:
		model = UserProfile
		exclude = ["user"]

class LoginForm(ModelForm):
	class Meta:
		model = User
		fields = ['username','password']

class TaskForm(ModelForm):
	#created = forms.DateField(widget=SelectDateWidget(),input_formats=('%b. %d, %Y',))
	#created = forms.DateField(widget=forms.widgets.DateInput(format='%Y-%m-%d'),input_formats=('%Y-%m-%d',))
	created = forms.DateField(widget=SelectDateWidget(),input_formats=('%Y-%m-%d',),initial=datetime.today)

	class Meta:
		model = Task
		exclude = ['user']