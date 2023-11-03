from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from .models import Event, Ticket
from .forms import EventForm


# Create your views here.
class UserEventMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.organizer != self.request.user:
            raise PermissionDenied
        return obj
class EventListView(ListView):
    model = Event
    template_name = "events/events.html"
    context_object_name = "events"
    ordering = ["-date_time"]

class EventDetailView(DetailView):
    model = Event
    template_name = "events/event.html"
    context_object_name = "event"


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = "events/create.html"
    form_class = EventForm

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        form.instance.available_tickets = form.instance.total_tickets
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("event", kwargs={"pk": self.object.pk})
    
class EventDeleteView(UserEventMixin, LoginRequiredMixin, DeleteView):
    model = Event
    template_name = "events/delete.html"
    success_url = "/events/"

class EventUpdateView(UserEventMixin, LoginRequiredMixin, UpdateView):
    model = Event
    template_name = "events/update.html"
    form_class = EventForm

    def get_success_url(self):
        return reverse("event", kwargs={"pk": self.object.pk})
    

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = "events/ticket_create.html"
    fields = []
    
    def post(self, request, *args, **kwargs):
        number_of_tickets = int(request.POST["number_of_tickets"])
        event = Event.objects.get(pk=kwargs["pk"])
        if number_of_tickets > event.available_tickets:
            return HttpResponse("Not enough tickets available.")
        for i in range(number_of_tickets):
            ticket = Ticket.objects.create(event=event, owner=request.user)
            ticket.save()
        event.available_tickets -= number_of_tickets
        event.save()
        return HttpResponse(f"Successfully purchased {number_of_tickets} tickets.")
    