from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from booking.models import TurfDetails,TimeSlot
from booking.forms import TurfDetailsForm, TimeSlotForm
from .forms import UserAddForm
from .decorators import admin_only
from django.contrib.auth.decorators import login_required


# Create your views here.
# index rendering....
@admin_only
def index(request):
    return render (request,'index.html')

@login_required(login_url="signin")
def manager_home(request):
    return render(request,'turf_manager_home.html')

@login_required(login_url="signin")
def booking(request):
    Turf_details = TurfDetails.objects.all() 
    area = []
    cat = []
    for i in Turf_details:
        area.append(i.Turf_area)
        cat.append(i.Turf_catogary)
    area = list(set(area))
    cat = list(set(cat))
    context = {
        "area":area,
        'cat':cat
    }
        
    return render(request, 'booking.html',context)

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

@login_required(login_url="signin")
def manage_turf(request):
    return render(request,'manage_turf.html')

def signup(request):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,"User Created")
            return redirect('signin')
    return render(request,"register.html",{"form":form})

def signin(request):
    
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        
        user1 = authenticate(request, username = username , password = password)
        
        if user1 is not None:
            request.session['username'] = username
            request.session['password'] = password
            login(request, user1)
            return redirect('index')
    
    return render(request, 'login.html')

def signout(request):
    
    logout(request)
    return redirect('index')


# turf settings manager

@login_required(login_url="signin")
def add_turf(request):
    form = TurfDetailsForm()
    
    if request.method == 'POST':
        form = TurfDetailsForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'New Turf Added to list')
            return redirect('manage_turf')
        
    return render(request,'add_turf.html',{"form":form})

@login_required(login_url="signin")
def edit_turf(request):
    
    turf = TurfDetails.objects.all()
    if request.method=='POST':
        Turf_id = request.POST['submit']
        Turf_det = TurfDetails.objects.get(Turf_id = Turf_id)
        Turf_det.delete()
        messages.info(request,'Turf Deleted succesfully')
        return redirect('edit_turf')
    
    return render(request,'edit_turf.html',{'turf':turf})

@login_required(login_url="signin")
def AddTimeSlot(request):
    form = TimeSlotForm()
    if request.method == "POST":
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            Timeslot = form.cleaned_data.get("TimeSlot")
            Turf = form.cleaned_data.get("Turf")
            Date = form.cleaned_data.get("Date")
            if TimeSlot.objects.filter(TimeSlot = Timeslot, Turf = Turf,Date = Date).exists():
                messages.info(request,"Time Slot Already in list")
                return redirect("AddTimeSlot")
            else:
                form.save()
                messages.info(request,"Time Slot Added list")
                return redirect("AddTimeSlot")
            
    return render(request,"addtimeslot.html",{"form":form})

@login_required(login_url="signin")
def SlotList(request):
    
    slots = TimeSlot.objects.all()
    context = {
        "slots":slots
    }
    return render(request,"slotlist.html",context)

def Deleteslot(request,pk):
    slot = TimeSlot.objects.get(id = pk)
    slot.delete()
    messages.info(request,"Slot deleted")
    return redirect("SlotList")

