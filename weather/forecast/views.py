from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, F
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views import generic
from rest_framework import generics

from .forms import SearchForm
from .models import City, QueryHistory
from .serializers import CountCityToQuerySerializer


class SearchWeatherCity(LoginRequiredMixin, generic.FormView):
    form_class = SearchForm
    template_name = 'forecast/search.html'
    extra_context = {'title': 'Погода'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Находим историю запросов пользователя
        history = (QueryHistory.objects.filter(user_id=user).
                   select_related('city_id').order_by('-created_date')[:1])
        if history:
            context['history'] = history[0]
        return context


class ViewWeatherCity(LoginRequiredMixin, generic.TemplateView):
    template_name = 'forecast/weather_city.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            city_id = self.request.GET.get('name')
        except TypeError:
            raise Http404
        city = get_object_or_404(City, pk=city_id)
        context['title'] = city.name
        context['data_weather'] = city.get_weather_forecast()
        user = self.request.user
        # Сохраняем историю запросов
        history = QueryHistory(user_id=user, city_id=city)
        history.save()
        return context


class CountCityToQueryView(generics.ListAPIView):
    """View для обработки запроса для  api"""
    serializer_class = CountCityToQuerySerializer
    queryset = City.objects.annotate(count=Count('history'))
