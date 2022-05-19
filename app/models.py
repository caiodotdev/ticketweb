from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Thread(Timestamp):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type_tempo = models.CharField(
        max_length=255, blank=True, null=True, default='hour')
    time_tempo = models.IntegerField(blank=True, null=True, default=4)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    origin = models.CharField(max_length=255, blank=True, null=True)
    destination = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Ticket(Timestamp):
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, blank=True, null=True)
    price_per_adult = models.DecimalField(max_digits=9, decimal_places=2)
    total_price_per_adult = models.DecimalField(max_digits=9, decimal_places=2)
    taxes = models.DecimalField(max_digits=9, decimal_places=2)
    final_total_price = models.DecimalField(max_digits=9, decimal_places=2)
    hour_leave = models.CharField(max_length=255)
    hour_arrive = models.CharField(max_length=255)
    stops = models.CharField(max_length=255)
    durations = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    data_trip = models.DateField(blank=True, null=True)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)

    def __str__(self):
        return '{} -> {} em {} por {}'.format(self.origin, self.destination, str(self.data_trip),
                                              str(self.final_total_price))


class Airline(Timestamp):
    logo_url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=255)
    ticket = models.ForeignKey(
        Ticket, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return "%s" % self.name


class Pack(Timestamp):
    leave_date = models.DateField()
    arrive_date = models.DateField()
    name_hotel = models.CharField(max_length=255)
    diarias = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    flight_info = models.CharField(max_length=255)
    price_total = models.DecimalField(max_digits=9, decimal_places=2)
    price_adult = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return '{} por {}'.format(self.name_hotel, str(self.price_total))


class ImagePack(Timestamp):
    url = models.URLField(blank=True, null=True)
    pack = models.ForeignKey(
        Pack, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.url
