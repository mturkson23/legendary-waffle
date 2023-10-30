from django.urls import path

from events import views

urlpatterns = [
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('events/<int:pk>/ticket/', views.TicketCreateView.as_view(), name='get_ticket'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
]