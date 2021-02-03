from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('login/',auth_views.LoginView.as_view(template_name='mainapp/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='mainapp/logout.html'),name='logout'),
    # path('patientregister/', patientregister.as_view(), name='patientregister'),
    path('patientregister/', patientregister, name='patientregister'),
    path('doctorregister/', doctorregister, name='doctorregister'),
    path('login_redirect/', login_redirect_view, name='login_redirect_view'),
    path('booking/', booking, name='booking'),
    path('slot_book/<str:p_k>/', bookslot, name='slot_book'),
    path('delete_appointment/<str:pk>/', delete_appointment, name='delete_appointment'),
    path(r'update_doctor_list/', doctorlist),
    path(r'date_selected/', date_selected),
    path(r'time_selected/', time_selected),
    path(r'confirm_booking/', confirm_booking),
    path('booking_by_doc/',booking_by_doc, name='booking_by_doc'),
    path('date_selected_doc/', date_selected_doc, name='date_selected_doc'),
    path('time_selected_doc/', time_selected_doc, name='time_selected_doc'),
    path('confirm_booking_doc/', confirm_booking_doc, name='confirm_booking_doc'),
    path('doc_edit_profile/', doc_edit_profile, name='doc_edit_profile'),
    path('patient_edit_profile/', patient_edit_profile, name='patient_edit_profile'),
    ]

if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 