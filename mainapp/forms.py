from django.forms import ModelForm
from .models import *
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import SplitDateTimeWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


class appointment_form(ModelForm):
	class Meta:
		model = Appointment
		fields = '__all__'

class patientRegistrationForm(UserCreationForm):
	name=forms.CharField(max_length=80)
	contact=forms.IntegerField()
	city=forms.CharField(max_length=30)
	district=forms.CharField(max_length=30)
	state=forms.CharField(max_length=30)
	pic=forms.ImageField()

	class Meta(UserCreationForm.Meta):
		model =User
		# fields='__all__'
		# fields= ['name', 'contact', 'city','district','state','license' ]

	@transaction.atomic
	def save(self):
		user= super().save(commit=False)
		user.is_patient= True
		user.name=self.cleaned_data.get('name')
		user.contact=self.cleaned_data.get('contact')
		user.city=self.cleaned_data.get('city')
		user.district=self.cleaned_data.get('district')
		user.state=self.cleaned_data.get('state')
		user.save()
		patient = Patient.objects.create(user=user)
		
		patient.save()
		return user


class doctorRegistrationForm(UserCreationForm):
	SPECIALISATION=(
	('PEDITRICIAN','Pediatrician'),
	('GYNECOLOGIST','Gynecologist '),
	('SURGEON','Surgeon'),
	('PSYCHIATRIST','Psychiatrist'),
	('CARDIOLOGIST','Cardiologist'),
	('DERMATOLOGIST','Dermatologist'),
	('GASTROENTEROLOGIST','Gastroenterologist'),
	('NEPHROLOGIST','Nephrologist')
	)
	name=forms.CharField(max_length=80)
	contact=forms.IntegerField()
	city=forms.CharField(max_length=30)
	district=forms.CharField(max_length=30)
	state=forms.CharField(max_length=30)
	pic=forms.ImageField()
	license=forms.IntegerField()
	specialisation=forms.ChoiceField(choices = SPECIALISATION) 

	class Meta(UserCreationForm.Meta):
		model =User
		# fields='__all__'

	@transaction.atomic
	def save(self):
		user= super().save(commit=False)
		user.is_doctor= True
		user.name=self.cleaned_data.get('name')
		user.contact=self.cleaned_data.get('contact')
		user.city=self.cleaned_data.get('city')
		user.district=self.cleaned_data.get('district')
		user.state=self.cleaned_data.get('state')
		user.save()
		doctor = Doctor.objects.create(user=user)
		doctor.license = self.cleaned_data.get('license')
		doctor.specialisation=self.cleaned_data.get('specialisation')
		doctor.save()
		return user