from django import forms
from .models import TurfDetails, TimeSlot

class TurfDetailsForm(forms.ModelForm):
    
    class Meta:
        model = TurfDetails
        fields = '__all__'
        
class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ["TimeSlot","Turf","Date"]
        
        widgets = {
            "Date": forms.TextInput(attrs={"type":"date"})
        }