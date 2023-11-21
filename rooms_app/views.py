from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from .models import *
from rest_framework.response import Response
import datetime
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status
from rooms_app import serializers


class RoomsList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        print(request.query_params)
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        price_sort = request.query_params.get("price_sort")
        if start_date and end_date:
            try:
                rooms = Room.free_rooms.get_free_fooms(
                    start_booking=start_date, end_booking=end_date
                )
                print(rooms)
                if price_sort:
                    rooms = rooms.order_by(price_sort)
                serializer = serializers.GetFreeRoomsSerializer(rooms, many=True)
                return Response(serializer.data)
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class BookingCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        booking = serializers.AddBookingSerializer(data=request.data)
        if booking.is_valid():
            if booking.get_validation(request.user):
                booking.save()
                return Response(data=booking.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class BookingDelete(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,pk):
        booking=serializers.DeleteBookingSerializer(data=request.data)
        if booking.is_valid():
            if booking.get_validation(request.user):
                booking_obj=Booking.objects.get(id=pk)
                try:
                    booking_obj.delete()
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                return Response(data=booking.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
