from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
	is_patient= models.BooleanField(default=False)
	is_doctor= models.BooleanField(default=False)
	name=models.CharField(max_length=80)
	contact=models.IntegerField(default=90)
	city=models.CharField(max_length=30)
	district=models.CharField(max_length=30)
	state=models.CharField(max_length=30)
	pic = models.ImageField(upload_to = 'images/', default = './static/img/default.png', null=True)

class Patient(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
	# name=models.CharField(max_length=80)

	def __str__(self):
		return self.user.name

class Doctor(models.Model):
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
	user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
	license=models.IntegerField(default=60)
	specialisation=models.CharField(max_length=20, choices=SPECIALISATION, null=True)

	def __str__(self):
		return self.user.name

class Appointment(models.Model):
	patient=models.ForeignKey(Patient,on_delete=models.CASCADE,unique=False, null=False)
	doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,unique=False, null=False)
	date=models.DateField(auto_now_add=False, null=False)
	time=models.TimeField(auto_now_add=False, null=False)
	booked_by_doctor= models.BooleanField(default=False)
	# is_doctor= models.BooleanField(default=False)
	def __str__(self):
		return self.patient.user.name +' + ' + self.doctor.user.name