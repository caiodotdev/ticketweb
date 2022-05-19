from app.models import Thread
from app.models import ImagePack
from app.models import Pack
from rest_framework import serializers

from app.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id", "price_per_adult", "total_price_per_adult", "taxes", "final_total_price", "hour_leave", "hour_arrive",
            "stops", "durations", "url", "data_trip", "origin", "destination")


class PackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pack
        fields = ("id", "name_hotel", "address", "score",
                  "flight_info", "price_total", "price_adult")


class ImagePackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePack
        fields = ("id", "url", "pack")


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ("id", "title", "description", "type_tempo", "time_tempo",
                  "user", "origin", "destination", "start_date", "end_date")
