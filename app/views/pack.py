#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from threading import Thread

from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, DeleteView, UpdateView
)
from django.views.generic.list import ListView

from engine.decolar.decolar_pack import DecolarPackModel

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy, reverse

from app.models import Pack, ImagePack
from app.forms import PackForm, ImagePackPackFormSet
from app.mixins import PackMixin
from app.conf import PACK_DETAIL_URL_NAME, PACK_LIST_URL_NAME

from django_datatables_view.base_datatable_view import BaseDatatableView


class PackFormSetManagement(object):
    formsets = [ImagePackPackFormSet]

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
            self.object = form.save()
            for Formset in self.formsets:
                formset = context["{}set".format(str(Formset.model.__name__).lower())]
                if formset.is_valid():
                    formset.instance = self.object
                    formset.save()
        return super(PackFormSetManagement, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(PackFormSetManagement, self).get_context_data(**kwargs)
        for Formset in self.formsets:
            if self.request.POST:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(self.request.POST,
                                                                                    self.request.FILES,
                                                                                    instance=self.object)
            else:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(instance=self.object)
        return data


class List(LoginRequiredMixin, PackMixin, ListView):
    """
    List all Packs
    """
    login_url = '/admin/login/'
    template_name = 'pack/list.html'
    model = Pack
    context_object_name = 'packs'
    paginate_by = 1


class Create(LoginRequiredMixin, PackMixin, PermissionRequiredMixin, PackFormSetManagement, CreateView):
    """
    Create a Pack
    """
    login_url = '/admin/login/'
    model = Pack
    permission_required = (
        'app.add_pack'
    )
    form_class = PackForm
    template_name = 'pack/create.html'
    context_object_name = 'pack'

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy(PACK_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_initial(self):
        data = super(Create, self).get_initial()
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Pack criado com sucesso')
        return super(Create, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Create, self).form_invalid(form)


class Detail(LoginRequiredMixin, PackMixin, DetailView):
    """
    Detail of a Pack
    """
    login_url = '/admin/login/'
    model = Pack
    template_name = 'pack/detail.html'
    context_object_name = 'pack'

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        return context


class Update(LoginRequiredMixin, PackMixin, PermissionRequiredMixin, PackFormSetManagement, UpdateView):
    """
    Update a Pack
    """
    login_url = '/admin/login/'
    model = Pack
    template_name = 'pack/update.html'
    context_object_name = 'pack'
    form_class = PackForm
    permission_required = (
        'app.change_pack'
    )

    def get_initial(self):
        data = super(Update, self).get_initial()
        return data

    def get_success_url(self):
        return reverse_lazy(PACK_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_context_data(self, **kwargs):
        data = super(Update, self).get_context_data(**kwargs)
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Pack atualizado com sucesso')
        return super(Update, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Update, self).form_invalid(form)


class Delete(LoginRequiredMixin, PackMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete a Pack
    """
    login_url = '/admin/login/'
    model = Pack
    permission_required = (
        'app.delete_pack'
    )
    template_name = 'pack/delete.html'
    context_object_name = 'pack'

    def get_context_data(self, **kwargs):
        context = super(Delete, self).get_context_data(**kwargs)
        collector = NestedObjects(using='default')
        collector.collect([self.get_object()])
        context['deleted_objects'] = collector.nested()
        return context

    def __init__(self):
        super(Delete, self).__init__()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Pack removido com sucesso')
        return super(Delete, self).delete(self.request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(PACK_LIST_URL_NAME)


class PackListJson(BaseDatatableView):
    model = Pack
    columns = ("id", "diarias", "leave_date", "arrive_date", "name_hotel", "score", "price_total", "price_adult")
    max_display_length = 500


class DeleteAllPack(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        Pack.objects.all().delete()
        ImagePack.objects.all().delete()
        return reverse_lazy('PACK_list')


def get_packs(request):
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
        decolarPack = DecolarPackModel(start_date, end_date, 10, origin, destination)
        p = Thread(target=decolarPack.get_info, args=(start_date,), kwargs={'start_date': start_date})
        p.start()
        p.join()
        messages.success(request, 'Start Thread for get infos.')
    return redirect('/')
