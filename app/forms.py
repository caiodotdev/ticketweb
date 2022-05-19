from django import forms
from django.forms import ModelForm, inlineformset_factory

from app.utils import generate_bootstrap_widgets_for_all_fields
from . import (
    models
)


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # field.widget.attrs['class'] = 'form-control'
            if field_name == 'phone' or field_name == 'telefone':
                field.widget.attrs['class'] = 'form-control telefone phone'
            if field_name == 'cep' or field_name == 'postalcode':
                field.widget.attrs['class'] = 'form-control cep'


class TicketForm(BaseForm, ModelForm):
    class Meta:
        model = models.Ticket
        fields = (
            "id", "price_per_adult", "total_price_per_adult", "taxes", "final_total_price", "hour_leave", "hour_arrive",
            "stops", "durations", "url", "data_trip", "origin", "destination")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Ticket)

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)


class PackForm(BaseForm, ModelForm):
    class Meta:
        model = models.Pack
        fields = ("id","leave_date", "arrive_date", "name_hotel", "address", "score", "flight_info", "price_total", "price_adult")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Pack)

    def __init__(self, *args, **kwargs):
        super(PackForm, self).__init__(*args, **kwargs)


class ImagePackForm(BaseForm, ModelForm):
    class Meta:
        model = models.ImagePack
        fields = ("id", "url", "pack")
        widgets = generate_bootstrap_widgets_for_all_fields(models.ImagePack)

    def __init__(self, *args, **kwargs):
        super(ImagePackForm, self).__init__(*args, **kwargs)


ImagePackPackFormSet = inlineformset_factory(models.Pack, models.ImagePack, form=ImagePackForm, extra=1)


class ThreadForm(BaseForm, ModelForm):
    class Meta:
        model = models.Thread
        fields = ("id", "title", "description", "type_tempo", "time_tempo", "user", "origin", "destination", "start_date", "end_date")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Thread)

    def __init__(self, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
