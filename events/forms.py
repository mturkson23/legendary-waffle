from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "date_time",
            "location",
            "total_tickets",
            "price",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Event Title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Event Description"}),
            "date_time": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local", "placeholder": "Event Date & Time"}),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "Event Location"}),
            "total_tickets": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Total Tickets"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Ticket Price"}),
        }
