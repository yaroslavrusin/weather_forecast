from django import forms
from django_select2 import forms as s2forms

from .models import City


class MyWidget(s2forms.ModelSelect2Widget):
    """Класс виджета для формы с автодополнением"""
    search_fields = [
        'name__istartswith',
    ]
    queryset = City.objects.all()


class SearchForm(forms.Form):
    """Форма для поиска нужного города"""
    name = forms.CharField(widget=MyWidget, label='Выберите город')
