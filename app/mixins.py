from django.core.exceptions import FieldDoesNotExist

from app.models import (
    Ticket
)


class TicketMixin(object):

    def kwargs_for_reverse_url(self):
        kwargs_dict = dict()
        if self.model:
            self.object = self.object if self.object is not None else self.get_object()
            try:
                self.model._meta.get_field('slug')
                kwargs_dict['slug'] = self.object.slug
            except FieldDoesNotExist:
                kwargs_dict['pk'] = self.object.id
        return kwargs_dict

    def get_context_data(self, **kwargs):
        context = super(TicketMixin, self).get_context_data(**kwargs)
        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()
        return context

    def get_ticket(self):
        return Ticket.objects.get(pk=self.kwargs.get("pk_ticket", 0))


class PackMixin(object):

    def kwargs_for_reverse_url(self):
        kwargs_dict = dict()
        if self.model:
            self.object = self.object if self.object is not None else self.get_object()
            try:
                self.model._meta.get_field('slug')
                kwargs_dict['slug'] = self.object.slug
            except FieldDoesNotExist:
                kwargs_dict['pk'] = self.object.id
        return kwargs_dict

    def get_context_data(self, **kwargs):
        context = super(PackMixin, self).get_context_data(**kwargs)
        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()
        return context

    def get_pack(self):
        return Pack.objects.get(pk=self.kwargs.get("pk_pack", 0))


class ImagePackMixin(object):

    def kwargs_for_reverse_url(self):
        kwargs_dict = dict()
        if self.model:
            self.object = self.object if self.object is not None else self.get_object()
            try:
                self.model._meta.get_field('slug')
                kwargs_dict['slug'] = self.object.slug
            except FieldDoesNotExist:
                kwargs_dict['pk'] = self.object.id
        return kwargs_dict

    def get_context_data(self, **kwargs):
        context = super(ImagePackMixin, self).get_context_data(**kwargs)
        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()
        return context

    def get_imagepack(self):
        return ImagePack.objects.get(pk=self.kwargs.get("pk_imagepack", 0))


class ThreadMixin(object):

    def kwargs_for_reverse_url(self):
        kwargs_dict = dict()
        if self.model:
            self.object = self.object if self.object is not None else self.get_object()
            try:
                self.model._meta.get_field('slug')
                kwargs_dict['slug'] = self.object.slug
            except FieldDoesNotExist:
                kwargs_dict['pk'] = self.object.id
        return kwargs_dict

    def get_context_data(self, **kwargs):
        context = super(ThreadMixin, self).get_context_data(**kwargs)
        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()
        return context

    def get_thread(self):
        return Thread.objects.get(pk=self.kwargs.get("pk_thread", 0))
