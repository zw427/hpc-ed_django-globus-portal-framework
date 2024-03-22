from django.http import JsonResponse
from django.views.generic.list import ListView
from .models import *

# Create your views here.
class Provider_v1_List(ListView):
    model = Provider
    '''
        All provider items
    '''
    def get(self, request, format=None, **kwargs):
        data = list(self.model.objects.values())
        return JsonResponse(data, safe = False)
