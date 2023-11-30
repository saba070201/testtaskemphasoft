from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
import datetime


class FreeRoomsManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()

    def get_free_fooms(self, **dates):
        free_rooms_pk = []
        start_date = dates["start_booking"].split("-")
        end_date = dates["end_booking"].split("-")
        start_booking = datetime.date(
            year=int(start_date[0]),
            month=int(start_date[1]),
            day=int(start_date[2]),
        )

        end_booking = datetime.date(
            year=int(end_date[0]),
            month=int(end_date[1]),
            day=int(end_date[2]),
        )
        for i in self.get_queryset().all():
            data = i.bookings.filter(
                (models.Q(start_booking__lte=start_booking)
                 and models.Q(end_booking__gt=start_booking))
                or models.Q(end_booking__gte=end_booking)
                and models.Q(start_booking__lt=end_booking))
            if not data.exists():
                i.price = i.price * self.get_days_count(
                    start_booking=start_booking, end_booking=end_booking)
                free_rooms_pk.append(i.id)
        return self.get_queryset().filter(pk__in=free_rooms_pk)

    def get_days_count(self, **dates):
        return (dates["end_booking"] - dates["start_booking"]).days


class Room(models.Model):
    title = models.CharField(blank=False, null=False)
    price = models.PositiveBigIntegerField(blank=False, null=False)
    count_of_slots = models.SmallIntegerField(blank=False, null=False)
    free_rooms = FreeRoomsManager()

    def get_price(self, **dates):
        return (dates["end_bookng"] - dates["start_booking"]).days * self.price


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    start_booking = models.DateField(null=True, blank=False)
    end_booking = models.DateField(null=True, blank=False)

    @property
    def get_days(self):
        return (self.end_booking - self.start_booking).days

    def can_set_booking_or_not(self, **dates):
        if (self.start_booking >= dates["start_booking"]
                and self.end_booking <= dates["end_booking"]):
            return False
        return True

    @property
    def get_total_price(self):
        return self.get_days * self.room.price


# Create your models here.
