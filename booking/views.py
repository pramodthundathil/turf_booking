from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from .models import TurfDetails, Booking_Confirmation,TimeSlot
import json
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from datetime import datetime


razorpay_client = razorpay.Client(
  auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# Create your views here.
@login_required(login_url="signin")
def turf_details(request):
    
    turf_area = request.POST['area']
    turf_catogary = request.POST['catogary']
    
    items = TurfDetails.objects.filter(Turf_area= turf_area,Turf_catogary = turf_catogary)
    if items is not None:
        return render (request,'turf_list.html',{'items':items})
    else:
        messages.info(request,'Turf Not Found')
        return redirect('booking')
    
@login_required(login_url="signin")
def book_slot(request):
    
    turf_id = request.POST['submit']
    Turf = TurfDetails.objects.filter(Turf_id = turf_id)
    T = TurfDetails.objects.get(Turf_id = turf_id)
    date = datetime.now()
    
    slots = TimeSlot.objects.filter(Turf = T,Date__gte = date)
    # slot = json.dumps(slots)
    context = {
        'turf':Turf,
        "slots":slots,
        "date":date,
        # "slot":slot
    }
            
    return render(request,'book_slot.html',context)

@login_required(login_url="signin")
def book_confirm(request):
    try:
        customer_name = request.POST['customer_name']
        customer_mobile = request.POST['customer_mobile']
        slotid = request.POST["timesloat"]
        slot = TimeSlot.objects.get(id = slotid) 
        confirmation = Booking_Confirmation.objects.create(slot = slot,customer_name = customer_name,customer_phone = customer_mobile)
        confirmation.cutomer = request.user
        confirmation.save()
    except:
        messages.info(request,"Slot Not Available")
        return redirect("MyBookings")
    currency = 'INR'
    amount = 800 * 100 # Rs. 200
    

  # Create a Razorpay Order Pyament Integration.....
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                          currency=currency,
                          payment_capture='0'))

  # order id of newly created order.
    razorpay_order_id = razorpay_order["id"]
    callback_url = 'paymenthandler/'

  # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url 
    context['slotid'] = confirmation.id
        
    return render(request,"makepayment.html",context)

def StatusChange(request):
    booking = Booking_Confirmation.objects.all().last()
    booking.paymet_status = True
    booking.save()
    slot = TimeSlot.objects.get(id = booking.slot.id)
    slot.Booking_status = True
    slot.save()
    
    return render(request,"booking_confirm.html")
    
    
@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

      # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = 800 * 100 # Rs. 200
                try:
                    print("working 1")
                    razorpay_client.payment.capture(payment_id, amount)
                    return redirect('StatusChange')
          # render success page on successful caputre of payment
                except:
                    print("working 2")
                    return redirect('StatusChange')
                    
                    
          # if there is an error while capturing payment.
            else:
                return render(request, 'paymentfail.html')
        # if signature verification fails.    
        except:
            return HttpResponseBadRequest()
        
      # if we don't find the required parameters in POST data
    else:
  # if other than POST request is made.
        return HttpResponseBadRequest()
        
        
        
@login_required(login_url="signin")
def manage_booking(request):
    
    bookings = Booking_Confirmation.objects.all()
    return render(request,'manage_booking.html',{'bookings':bookings})

@login_required(login_url="signin")
def cancelbooking(request,pk):
    booking = Booking_Confirmation.objects.get(id = pk)
    slotid = booking.slot.id
    slot = TimeSlot.objects.get(id = slotid)
    slot.Booking_status = False
    slot.save()
    booking.delete()
    messages.info(request,"Booking Deleted")

    return redirect("manage_booking")

@login_required(login_url="signin")
def cancelbookinguser(request,pk):
    booking = Booking_Confirmation.objects.get(id = pk)
    slotid = booking.slot.id
    slot = TimeSlot.objects.get(id = slotid)
    slot.Booking_status = False
    slot.save()
    booking.delete()
    messages.info(request,"Booking Deleted")

    return redirect("MyBookings")

@login_required(login_url="signin")
def MyBookings(request):
    
    dt = datetime.now()
    print(dt)
    dt = dt.date()
    upcomming = []
    previous = []
    today = []
    booking = Booking_Confirmation.objects.filter(cutomer = request.user)
    for i in booking:
        timeslot = i.slot
        if timeslot.Date > dt:
            upcomming.append(i)
        elif timeslot.Date == dt:
            today.append(i)
        elif  timeslot.Date < dt:
            previous.append(i)
        
    context= {
        "booking":upcomming,
        "previous":previous,
        'today':today
    }
    
    return render(request,"mybookings.html",context)




    
    
        
        
        
    
    