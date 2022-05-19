#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, DeleteView, UpdateView
)
from django.views.generic.list import ListView
from django_datatables_view.base_datatable_view import BaseDatatableView


from django.urls import reverse_lazy

from app.models import Thread
from app.forms import ThreadForm
from app.mixins import ThreadMixin
from app.conf import THREAD_DETAIL_URL_NAME, THREAD_LIST_URL_NAME


class ThreadFormSetManagement(object):
    formsets = []

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
            self.object = form.save()
            for Formset in self.formsets:
                formset = context["{}set".format(str(Formset.model.__name__).lower())]
                if formset.is_valid():
                    formset.instance = self.object
                    formset.save()
        return super(ThreadFormSetManagement, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(ThreadFormSetManagement, self).get_context_data(**kwargs)
        for Formset in self.formsets:
            if self.request.POST:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(self.request.POST,
                                                                                    self.request.FILES,
                                                                                    instance=self.object)
            else:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(instance=self.object)
        return data



class List(LoginRequiredMixin, ThreadMixin, ListView):
    """
    List all Threads
    """
    login_url = '/admin/login/'
    template_name = 'thread/list.html'
    model = Thread
    context_object_name = 'threads'
    paginate_by = 1


class Create(LoginRequiredMixin, ThreadMixin, PermissionRequiredMixin, ThreadFormSetManagement, CreateView):
    """
    Create a Thread
    """
    login_url = '/admin/login/'
    model = Thread
    permission_required = (
        'app.add_thread'
    )
    form_class = ThreadForm
    template_name = 'thread/create.html'
    context_object_name = 'thread'

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy(THREAD_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_initial(self):
        data = super(Create, self).get_initial()
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Thread criado com sucesso')
        return super(Create, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Create, self).form_invalid(form)


class Detail(LoginRequiredMixin, ThreadMixin, DetailView):
    """
    Detail of a Thread
    """
    login_url = '/admin/login/'
    model = Thread
    template_name = 'thread/detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        return context


class Update(LoginRequiredMixin, ThreadMixin, PermissionRequiredMixin, ThreadFormSetManagement, UpdateView):
    """
    Update a Thread
    """
    login_url = '/admin/login/'
    model = Thread
    template_name = 'thread/update.html'
    context_object_name = 'thread'
    form_class = ThreadForm
    permission_required = (
        'app.change_thread'
    )

    def get_initial(self):
        data = super(Update, self).get_initial()
        return data

    def get_success_url(self):
        return reverse_lazy(THREAD_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_context_data(self, **kwargs):
        data = super(Update, self).get_context_data(**kwargs)
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Thread atualizado com sucesso')
        return super(Update, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Update, self).form_invalid(form)


class Delete(LoginRequiredMixin, ThreadMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete a Thread
    """
    login_url = '/admin/login/'
    model = Thread
    permission_required = (
        'app.delete_thread'
    )
    template_name = 'thread/delete.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super(Delete, self).get_context_data(**kwargs)
        collector = NestedObjects(using='default')
        collector.collect([self.get_object()])
        context['deleted_objects'] = collector.nested()
        return context

    def __init__(self):
        super(Delete, self).__init__()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Thread removido com sucesso')
        return super(Delete, self).delete(self.request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(THREAD_LIST_URL_NAME)


class ThreadListJson(BaseDatatableView):
    model = Thread
    columns = ("id", "title", "description", "type_tempo", "time_tempo", "user", "origin", "destination", "start_date", "end_date")
    order_columns = ("id", "title", "description", "type_tempo", "time_tempo", "user", "origin", "destination", "start_date", "end_date")
    max_display_length = 500
