from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=100)
    total_tickets = models.IntegerField()
    available_tickets = models.IntegerField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return self.title
    

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    purchased_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner} - {self.event}"
