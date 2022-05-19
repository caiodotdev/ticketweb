#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import multiprocessing
from threading import Thread

from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.utils.html import escape
from django.views.generic import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, DeleteView, UpdateView
)
from django.views.generic.list import ListView
from app.views import thread

from engine.decolar.decolar import DecolarModel

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy, reverse

from app.models import Ticket, Airline
from app.forms import TicketForm
from app.mixins import TicketMixin
from app.conf import TICKET_DETAIL_URL_NAME, TICKET_LIST_URL_NAME

from django_datatables_view.base_datatable_view import BaseDatatableView

import calendar


class TicketFormSetManagement(object):
    formsets = []

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
            self.object = form.save()
            for Formset in self.formsets:
                formset = context["{}set".format(
                    str(Formset.model.__name__).lower())]
                if formset.is_valid():
                    formset.instance = self.object
                    formset.save()
        return super(TicketFormSetManagement, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(TicketFormSetManagement, self).get_context_data(**kwargs)
        for Formset in self.formsets:
            if self.request.POST:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(self.request.POST,
                                                                                    self.request.FILES,
                                                                                    instance=self.object)
            else:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(
                    instance=self.object)
        return data


class List(LoginRequiredMixin, TicketMixin, ListView):
    """
    List all Tickets
    """
    login_url = '/admin/login/'
    template_name = 'ticket/list.html'
    model = Ticket
    context_object_name = 'tickets'
    paginate_by = 1


class Create(LoginRequiredMixin, TicketMixin, PermissionRequiredMixin, TicketFormSetManagement, CreateView):
    """
    Create a Ticket
    """
    login_url = '/admin/login/'
    model = Ticket
    permission_required = (
        'app.add_ticket'
    )
    form_class = TicketForm
    template_name = 'ticket/create.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy(TICKET_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_initial(self):
        data = super(Create, self).get_initial()
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Ticket criado com sucesso')
        return super(Create, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Create, self).form_invalid(form)


class Detail(LoginRequiredMixin, TicketMixin, DetailView):
    """
    Detail of a Ticket
    """
    login_url = '/admin/login/'
    model = Ticket
    template_name = 'ticket/detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        return context


class Update(LoginRequiredMixin, TicketMixin, PermissionRequiredMixin, TicketFormSetManagement, UpdateView):
    """
    Update a Ticket
    """
    login_url = '/admin/login/'
    model = Ticket
    template_name = 'ticket/update.html'
    context_object_name = 'ticket'
    form_class = TicketForm
    permission_required = (
        'app.change_ticket'
    )

    def get_initial(self):
        data = super(Update, self).get_initial()
        return data

    def get_success_url(self):
        return reverse_lazy(TICKET_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_context_data(self, **kwargs):
        data = super(Update, self).get_context_data(**kwargs)
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Ticket atualizado com sucesso')
        return super(Update, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Update, self).form_invalid(form)


class Delete(LoginRequiredMixin, TicketMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete a Ticket
    """
    login_url = '/admin/login/'
    model = Ticket
    permission_required = (
        'app.delete_ticket'
    )
    template_name = 'ticket/delete.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super(Delete, self).get_context_data(**kwargs)
        collector = NestedObjects(using='default')
        collector.collect([self.get_object()])
        context['deleted_objects'] = collector.nested()
        return context

    def __init__(self):
        super(Delete, self).__init__()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Ticket removido com sucesso')
        return super(Delete, self).delete(self.request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(TICKET_LIST_URL_NAME)


class TicketListJson(BaseDatatableView):
    model = Ticket
    columns = (
        "id", "line", "origin", "destination", "data_trip", "final_total_price", "price_per_adult", "total_price_per_adult",
        "taxes", "hour_leave", "hour_arrive",
        "stops", "durations",)
    order_columns = (
        "id", "origin", "destination", "data_trip", "final_total_price", "price_per_adult", "total_price_per_adult",
        "taxes",)
    max_display_length = 500

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'line':
            airlines = row.airline_set.all()
            html = ''
            for i in range(len(airlines)):
                if i % 2 == 0:
                    html += '<img data-toggle="tooltip" data-placement="top" src="{0}" alt="{1}" title="{1}" class="img-thumbnail logo-airline"/> ->'.format(airlines[i].logo_url,
                                                                                                                                                             airlines[i].name)
                else:
                    html += '<img data-toggle="tooltip" data-placement="top" src="{0}" alt="{1}" title="{1}" class="img-thumbnail logo-airline"/>\n &nbsp;&nbsp;'.format(airlines[i].logo_url,
                                                                                                                                                                         airlines[i].name)
            # escape HTML for security reasons
            return html
        else:
            return super(TicketListJson, self).render_column(row, column)


threads = []

def run_thread(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    origin = request.GET['origin']
    destination = request.GET['destination']
    start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    if start == end:
        messages.error(request, 'Send diff dates!')
    elif start > end:
        messages.error(request, 'Start date is bigger than End date!')
    else:
        process_search_voos(start, end, origin, destination)
        messages.success(request, 'Start Thread for get infos.')
    return redirect('/ticket')


def process_search_voos(start, end, origin, destination, thread=None):
    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')
    diarias = (end - start).days
    for i in range(0, int(diarias) + 1):
        date_filter = start + datetime.timedelta(days=i)
        date_filter = str(date_filter).split(' ')[0]
        try:
            decolar = DecolarModel(origin, destination, start_date, end_date, 20)
            decolar.get_info(date_filter, **{'date_filter': date_filter, 'thread': thread})
            decolar.dispose()
        except Exception as e:
            print(e)
            print('Nao tem voos nessa data: ', date_filter)
            continue
        try:
            decolar_volta = DecolarModel(
                destination, origin, start_date, end_date, 20)
            decolar_volta.get_info(date_filter, **{'date_filter': date_filter, 'thread': thread})
            decolar_volta.dispose()
        except Exception as e:
            print(e)
            print('Nao tem voos nessa data: ', date_filter)
            continue
    


def get_prices_in_month(origin, destination):
    now = datetime.datetime.now()
    range_days = calendar.monthrange(now.year, now.month)[1] - now.day
    for i in range(range_days):
        date_filter = now + datetime.timedelta(days=i)
        date_filter = str(date_filter).split(' ')[0]
        decolar = DecolarModel(origin, destination,
                               date_filter, date_filter, 13)
        p = Thread(target=decolar.get_info, args=(date_filter,),
                   kwargs={'date_filter': date_filter})
        threads.append(p)
        p.start()
        decolar_volta = DecolarModel(
            destination, origin, date_filter, date_filter, 13)
        p2 = Thread(target=decolar_volta.get_info, args=(
            date_filter,), kwargs={'date_filter': date_filter})
        threads.append(p2)
        p2.start()
    for thread in threads:
        thread.join()
        threads.remove(thread)


def scrap_voos():
    origins = ['CPV', 'JPA']
    destinations = ['CWB', 'SAO', 'FLN', 'POA',
                    'RIO', 'VCP', 'FOR', 'MIA', 'ORL', 'CUN']
    for origin in origins:
        for destination in destinations:
            get_prices_in_month(origin, destination)


class DeleteAll(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        Ticket.objects.all().delete()
        Airline.objects.all().delete()
        return reverse_lazy('TICKET_list')
