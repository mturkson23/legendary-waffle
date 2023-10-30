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
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "date_time": forms.DateTimeInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "total_tickets": forms.NumberInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
        }
