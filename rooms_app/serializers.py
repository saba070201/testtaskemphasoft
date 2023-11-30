from rest_framework.fields import empty
from .models import Booking, Room
from django.db.models import fields
from rest_framework import serializers
from django.db import models
from django.contrib.auth.models import User


class GetFreeRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("title", "price")


class AddBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("user", "room", "start_booking", "end_booking")

    def get_validation(self, user):
        if self.validated_data["start_booking"] >= self.validated_data[
                "end_booking"]:
            raise serializers.ValidationError()
        if self.Meta.model.objects.filter(
            (models.Q(start_booking__lte=self.validated_data["start_booking"])
             and
             models.Q(end_booking__gt=self.validated_data["start_booking"])) or
                models.Q(end_booking__gte=self.validated_data["end_booking"])
                and
                models.Q(start_booking__lt=self.validated_data["end_booking"]
                         ).filter(room=self.validated_data["room"])).exists():
            raise serializers.ValidationError()
        if (not user.is_staff or not user.is_superuser) and User.objects.get(
                username=self.validated_data["user"]).id != user.id:
            raise serializers.ValidationError()
        return True


class DeleteBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("id", "user")

    def get_validation(self, user):
        if (not user.is_staff or not user.is_superuser) and User.objects.get(
                username=self.validated_data["user"]).id != user.id:
            raise serializers.ValidationError()
        return True
