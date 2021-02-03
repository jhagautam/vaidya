from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404,reverse
from django.conf import settings
from django.views import generic
from django.urls import reverse_lazy
from mainapp.models import *
from django.views.generic import CreateView
from mainapp.forms import *
from django.db.models import Count, Sum , Avg, Max, Min
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory, modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
import datetime
from django.utils import timezone
from django.forms.models import model_to_dict
from copy import copy
from django.core.serializers.json import DjangoJSONEncoder
import json

# Create your views here.
def UPOST(post, obj):
    '''Updates request's POST dictionary with values from object, for update purposes'''
    post = copy(post)
    for k,v in model_to_dict(obj).iteritems():
        if k not in post: post[k] = v
    return post

def index(request):
	context={}
	return render(request, 'mainapp/index.html', context)

def patientregister(request):
	if request.method == 'POST':
		form = patientRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = patientRegistrationForm()
	return render(request,'mainapp/register.html',{'form':form,'title':'Sign Up'})

def doctorregister(request):
	if request.method == 'POST':
		form = doctorRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = doctorRegistrationForm()
	return render(request,'mainapp/register.html',{'form':form,'title':'Sign Up'})
@login_required(login_url='/login/')
def login_redirect_view(request):
	if request.user.is_doctor:
		d=Appointment.objects.all().filter(doctor=request.user.id).filter(booked_by_doctor=False)
		today=datetime.date.today()
		context={'appointments':d,'today':today}
		return render(request, 'mainapp/doctor_home.html', context)
	else:
		x=request.user.id
		print('login redirect view me', x)
		appointments=Appointment.objects.filter(patient=x).filter(booked_by_doctor=False).order_by('-date')
		today=datetime.date.today()
		context={'appointments':appointments,'today':today}
		return render(request, 'mainapp/patient_home.html', context)

@login_required(login_url='/login/')
def doctorlist(request):
		if request.method == 'POST':
			city=request.POST['city']
			specialisation_of_doc=request.POST['specialisation_of_doc']
			print(city,specialisation_of_doc)
			cities=Doctor.objects.order_by().values('user__city').distinct()
			doctor=Doctor.objects.all()
			specialisations=Doctor.objects.values('specialisation').distinct()
			q=Doctor.objects.filter(user__city=city).filter(specialisation=specialisation_of_doc)
			# q=list(q)
			context={'q':q,'cities':cities, 'specialisations':specialisations, 'doctor':doctor}
			return render(request, 'mainapp/doctorlist.html', context)
@login_required(login_url='/login/')
def booking(request):
	cities=Doctor.objects.order_by().values('user__city').distinct()
	doctor=Doctor.objects.all()
	specialisations=Doctor.objects.values('specialisation').distinct()
	context={'cities':cities, 'specialisations':specialisations, 'doctor':doctor}
	return render(request, 'mainapp/booking.html', context)
@login_required(login_url='/login/')
def bookslot(request, p_k):
	User = get_user_model()
	doc=User.objects.get(pk=p_k)
	x=datetime.date.today()
	context={'doc':doc,'x':x}
	return render(request, 'mainapp/slot_book.html', context)
@login_required(login_url='/login/')
def date_selected(request):
	if request.method == 'POST':
			booking_date=request.POST['date']
			doctor_id=request.POST['doctor']
			q=Appointment.objects.filter(date=booking_date)
			context={'q':q,'booking_date':booking_date, 'doctor_id':doctor_id}
			return render(request, 'mainapp/book_time.html', context)
@login_required(login_url='/login/')
def time_selected(request):
	if request.method == 'POST':
			User = get_user_model()
			booking_date=request.POST['date']
			doctor_id=request.POST['doctor']
			time_booked=request.POST['time']
			user_model=User.objects.all()
			context={'time_booked':time_booked,'booking_date':booking_date, 'doctor_id':doctor_id,'user_model':user_model}
			return render(request, 'mainapp/confirm_booking.html', context)

@login_required(login_url='/login/')
def confirm_booking(request):
	form=appointment_form()
	if request.method == 'POST':
		form=appointment_form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login_redirect_view')

		context={'form' : form}
		return render(request,'mainapp/test.html', context)

@login_required(login_url='/login/')
def delete_appointment(request, pk):
	aptmnt=Appointment.objects.get(id=pk)
	if request.method == "POST":
		aptmnt.delete()
		return redirect('login_redirect_view')
	context={'item':aptmnt}
	return render(request,'mainapp/delete.html', context)
@login_required(login_url='/login/')
def booking_by_doc(request):
	x=datetime.date.today()
	context={'x':x,}
	return render(request, 'mainapp/select_date.html', context)
@login_required(login_url='/login/')
def date_selected_doc(request):
	if request.method == 'POST':
			booking_date=request.POST['date']
			q=Appointment.objects.filter(date=booking_date)
			context={'q':q,'booking_date':booking_date}
			return render(request, 'mainapp/select_time.html', context)
@login_required(login_url='/login/')
def time_selected_doc(request):
	if request.method == 'POST':
			User = get_user_model()
			booking_date=request.POST['date']
			time_booked=request.POST['time']
			user_model=User.objects.all()
			context={'time_booked':time_booked,'booking_date':booking_date,'user_model':user_model}
			return render(request, 'mainapp/confirm_booking_doc.html', context)
@login_required(login_url='/login/')
def confirm_booking_doc(request):
	form=appointment_form()
	if request.method == 'POST':
		form=appointment_form(request.POST)
		if form.is_valid():
			# form.booked_by_doctor=True
			form.save()
			return redirect('login_redirect_view')

		context={'form' : form}
		return render(request,'mainapp/test.html', context)

@login_required(login_url='/login/')
def doc_edit_profile(request):
	User = get_user_model()
	user=User.objects.get(id=request.user.id)
	doctor=Doctor.objects.get(user=request.user)
	if request.method == "POST":
		Name=request.POST["fname"]
		Contact=request.POST["fcontact"]
		City=request.POST["fcity"]
		District=request.POST["fdistrict"]
		State=request.POST["fstate"]
		# Pic=request.FILES["fpic"]
		user.name=Name
		user.contact=Contact
		user.city=City
		user.district=District
		user.state=State

		if len(request.FILES) !=0:
			user.pic=request.FILES["fpic"]
		user.save()
		License=request.POST["flicense"]
		Specialisation=request.POST["fspecialisation"]
		doctor.license=License
		doctor.specialisation=Specialisation
		doctor.save()
		return redirect('login_redirect_view')
			

	context={'doctor':doctor}
	return render(request,'mainapp/doctor_edit_profile.html', context)
@login_required(login_url='/login/')
def patient_edit_profile(request):
	User = get_user_model()
	user=User.objects.get(id=request.user.id)
	if request.method == "POST":
		Name=request.POST["fname"]
		Contact=request.POST["fcontact"]
		City=request.POST["fcity"]
		District=request.POST["fdistrict"]
		State=request.POST["fstate"]
		user.name=Name
		user.contact=Contact
		user.city=City
		user.district=District
		user.state=State

		if len(request.FILES) != 0:
			user.pic=request.FILES["fpic"]
		user.save()
		return redirect('login_redirect_view')
			

	context={}
	return render(request,'mainapp/patient_edit_profile.html', context)