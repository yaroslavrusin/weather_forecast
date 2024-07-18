from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic
from django.http import Http404

from .forms import SearchForm
from .models import City, QueryHistory


class SearchWeatherCity(LoginRequiredMixin, generic.FormView):
    form_class = SearchForm
    template_name = 'forecast/search.html'
    extra_context = {'title': 'Погода'}

    def post(self, request, *args, **kwargs):
        try:
            city_id = int(request.POST.get('name'))
        except ValueError:
            raise Http404
        city = get_object_or_404(City, pk=city_id)
        user = request.User
        history = QueryHistory(user_id=user.id, city_id=city.id)
        history.save()

        return
