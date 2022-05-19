import time

from celery import shared_task
from requests import request
import requests

from app.models import Thread, Ticket
from app.views.ticket import process_search_voos
from .celery import app

"""
This module defines various Celery.
"""

# get your api_id, api_hash, token
# from telegram as described above
API_ID = '9274986'
API_HASH = '997678b9dbb3636a5905a6c253c00c32'
TOKEN = '5257269681:AAFJxn4iKUXDcBck8L74HUxVKEp3Hz7kyDM'
MESSAGE = "🔥 {} \n\n R$ {}  \n\n Saindo dia: {} as {} \n Chegando as: {} \n \n Stops: {} \n Durations: {} URL:{}"
PHONE = '+5583991773034'
CHAT_ID = '451429199'
URI = 'https://api.telegram.org/bot{}/sendMessage'


@shared_task()
def run_threads():
    for thread in Thread.objects.all():
        print('----- Starting Thread: {} - {}'.format(thread.id, thread.title))
        start = thread.start_date
        end = thread.end_date
        origin = thread.origin
        destination = thread.destination
        process_search_voos(start, end, origin, destination, thread=thread)
        best_tickets = filter_best_price()
        if best_tickets:
            telegram_alert(best_tickets)
            delete_tickets(thread)
        # email_alert(best_tickets)
        print('----- Finishing Thread: {} - {}'.format(thread.id, thread.title))


def delete_tickets(thread):
    """
    Delete tickets.
    :param thread:
    :return:
    """
    print('----- Deleting tickets')
    for ticket in thread.ticket_set.all():
        ticket.delete()
    print('----- Tickets deleted')

def filter_best_price():
    """
    Filter the best price.
    :return:
    """
    tickets = []
    for thread in Thread.objects.all():
        for ticket in thread.ticket_set.all().order_by('final_total_price')[:3]:
            tickets.append(ticket)
        for ticket in thread.ticket_set.filter(origin=thread.origin).order_by('final_total_price')[:3]:
            tickets.append(ticket)
        for ticket in thread.ticket_set.filter(origin=thread.destination).order_by('final_total_price')[:3]:
            tickets.append(ticket)
    return tickets

def telegram_alert(best_tickets):
    """
    Send a Telegram alert.
    :param best_tickets:
    :return:
    """

    print('----- Sending Telegram alert')
    for ticket in best_tickets:
        url = ticket.url
        price = ticket.final_total_price
        price_per_adult = ticket.total_price_per_adult
        hour_leave = ticket.hour_leave
        hour_arrive = ticket.hour_arrive
        data_trip = ticket.data_trip
        message = MESSAGE.format(ticket, price, data_trip,
                                 hour_leave, hour_arrive, ticket.stops, ticket.durations, url)
        print(message)
        uri = URI.format(TOKEN)
        print('sending ... ', uri)
        params = {
        "chat_id": CHAT_ID,
        "text": message,
        }

        req = requests.get(uri, headers={'Content-Type': 'application/json'}, params=params)
        if req.status_code == 200:
            print('----- Message sent')
        else:
            print('----- Message not sent')
    print('----- Telegram alert sent')


def email_alert(best_tickets):
    """
    Send an email alert.
    :param best_tickets:
    :return:
    """
    print('----- Sending Email alert')

    print('----- Email alert sent')
