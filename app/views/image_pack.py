#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import FieldDoesNotExist
from django.db import transaction
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, DeleteView, UpdateView
)
from django.views.generic.list import ListView


try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy, reverse

from app.models import ImagePack
from app.forms import ImagePackForm
from app.mixins import ImagePackMixin
from app.conf import IMAGEPACK_DETAIL_URL_NAME, IMAGEPACK_LIST_URL_NAME

from django_datatables_view.base_datatable_view import BaseDatatableView

class ImagePackFormSetManagement(object):
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
        return super(ImagePackFormSetManagement, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(ImagePackFormSetManagement, self).get_context_data(**kwargs)
        for Formset in self.formsets:
            if self.request.POST:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(self.request.POST,
                                                                                    self.request.FILES,
                                                                                    instance=self.object)
            else:
                data["{}set".format(str(Formset.model.__name__).lower())] = Formset(instance=self.object)
        return data



class List(LoginRequiredMixin, ImagePackMixin, ListView):
    """
    List all ImagePacks
    """
    login_url = '/admin/login/'
    template_name = 'imagepack/list.html'
    model = ImagePack
    context_object_name = 'imagepacks'
    paginate_by = 1


class Create(LoginRequiredMixin, ImagePackMixin, PermissionRequiredMixin, ImagePackFormSetManagement, CreateView):
    """
    Create a ImagePack
    """
    login_url = '/admin/login/'
    model = ImagePack
    permission_required = (
        'app.add_imagepack'
    )
    form_class = ImagePackForm
    template_name = 'imagepack/create.html'
    context_object_name = 'imagepack'

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy(IMAGEPACK_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_initial(self):
        data = super(Create, self).get_initial()
        return data

    def form_valid(self, form):
        messages.success(self.request, 'ImagePack criado com sucesso')
        return super(Create, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Create, self).form_invalid(form)


class Detail(LoginRequiredMixin, ImagePackMixin, DetailView):
    """
    Detail of a ImagePack
    """
    login_url = '/admin/login/'
    model = ImagePack
    template_name = 'imagepack/detail.html'
    context_object_name = 'imagepack'

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        return context


class Update(LoginRequiredMixin, ImagePackMixin, PermissionRequiredMixin, ImagePackFormSetManagement, UpdateView):
    """
    Update a ImagePack
    """
    login_url = '/admin/login/'
    model = ImagePack
    template_name = 'imagepack/update.html'
    context_object_name = 'imagepack'
    form_class = ImagePackForm
    permission_required = (
        'app.change_imagepack'
    )

    def get_initial(self):
        data = super(Update, self).get_initial()
        return data

    def get_success_url(self):
        return reverse_lazy(IMAGEPACK_DETAIL_URL_NAME, kwargs=self.kwargs_for_reverse_url())

    def get_context_data(self, **kwargs):
        data = super(Update, self).get_context_data(**kwargs)
        return data

    def form_valid(self, form):
        messages.success(self.request, 'ImagePack atualizado com sucesso')
        return super(Update, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve algum erro, tente novamente')
        return super(Update, self).form_invalid(form)


class Delete(LoginRequiredMixin, ImagePackMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete a ImagePack
    """
    login_url = '/admin/login/'
    model = ImagePack
    permission_required = (
        'app.delete_imagepack'
    )
    template_name = 'imagepack/delete.html'
    context_object_name = 'imagepack'

    def get_context_data(self, **kwargs):
        context = super(Delete, self).get_context_data(**kwargs)
        collector = NestedObjects(using='default')
        collector.collect([self.get_object()])
        context['deleted_objects'] = collector.nested()
        return context

    def __init__(self):
        super(Delete, self).__init__()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'ImagePack removido com sucesso')
        return super(Delete, self).delete(self.request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(IMAGEPACK_LIST_URL_NAME)


class ImagePackListJson(BaseDatatableView):
    model = ImagePack
    columns = ("id", "url", "pack")
    order_columns = ("id", "url", "pack")
    max_display_length = 500
