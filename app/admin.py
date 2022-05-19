#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from app.models import *


# Register your models here.


class TicketAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = []
    list_display = (
        "id", "price_per_adult", "total_price_per_adult", "taxes", "final_total_price", "hour_leave", "hour_arrive",
        "stops", "durations", "url", "data_trip", "origin", "destination")


admin.site.register(Ticket, TicketAdmin)


class ImagePackInline(admin.TabularInline):
    model = ImagePack


class PackAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = [ImagePackInline]
    list_display = ("id", "name_hotel", "address", "score", "flight_info", "price_total", "price_adult", "leave_date", "arrive_date")


admin.site.register(Pack, PackAdmin)


class ImagePackAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = []
    list_display = ("id", "url", "pack")


admin.site.register(ImagePack, ImagePackAdmin)


class ThreadAdmin(admin.ModelAdmin):
    list_filter = []
    search_fields = (
        'id',
    )
    inlines = []
    list_display = ("id", "title", "description", "type_tempo", "time_tempo", "user", "origin", "destination", "start_date", "end_date")

admin.site.register(Thread, ThreadAdmin)
