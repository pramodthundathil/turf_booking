from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name= 'index'),
    path('booking',views.booking,name= 'booking'),
    path('about',views.about,name = 'about'),
    path('contact',views.contact,name='contact'),
    
    path('signin',views.signin,name= 'signin'),
    path('manager_home',views.manager_home,name='manager_home'),
    path('signout',views.signout,name='signout'),
    path('signup',views.signup,name="signup"),
    path('manage_turf',views.manage_turf,name= 'manage_turf'),
    
    path('add_turf',views.add_turf,name= 'add_turf'),
    path('edit_turf',views.edit_turf,name= 'edit_turf'),
    path("AddTimeSlot",views.AddTimeSlot,name="AddTimeSlot"),
    path("SlotList",views.SlotList,name="SlotList"),
    path("Deleteslot/<int:pk>",views.Deleteslot,name="Deleteslot")
    
]

