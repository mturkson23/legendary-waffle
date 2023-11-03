from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from events.models import Event


class EventTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            password="testpassword"
        )
        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            organizer=self.user,
            date_time="2021-01-01 00:00:00",
            total_tickets=100,
            available_tickets=100,
            price=10.00
        )

    def test_event_str(self):
        self.assertEqual(str(self.event), "Test Event")

    def test_event_list_view(self):
        response = self.client.get(reverse("events"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event")
        self.assertTemplateUsed(response, "events/events.html")
    
    def test_event_detail_view(self):
        response = self.client.get(reverse("event", kwargs={"pk": self.event.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event")
        self.assertTemplateUsed(response, "events/event.html")

    def test_event_update_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("event_update", kwargs={"pk": self.event.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/update.html")

    def test_event_update_view_permission_denied(self):
        self.client.force_login(User.objects.create_user(username="testuser2", password="testpassword"))
        response = self.client.get(reverse("event_update", kwargs={"pk": self.event.pk}))
        self.assertEqual(response.status_code, 403)

    def test_event_update_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("event_update", kwargs={"pk": self.event.pk}), {
            "title": "Test Event Updated",
            "description": "Test Description Updated",
            "date_time": "2021-01-01 00:00:00",
            "location": "Test Location Updated",
            "total_tickets": 100,
            "price": 10.00
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.get(pk=self.event.pk).title, "Test Event Updated")

    def test_event_create_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("event_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/create.html")

    def test_event_create_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("event_create"), {
            "title": "Test Event Created",
            "description": "Test Description Created",
            "date_time": "2021-01-01 00:00:00",
            "location": "Test Location Created",
            "total_tickets": 100,
            "price": 10.00
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.get(title="Test Event Created").description, "Test Description Created")

    def test_event_delete_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("event_delete", kwargs={"pk": self.event.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/delete.html")

    def test_event_delete_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("event_delete", kwargs={"pk": self.event.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 0)
