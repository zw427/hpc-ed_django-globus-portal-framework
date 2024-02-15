from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.views import debug
import sys

@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = open(settings.STATIC_ROOT + '/img/favicon.ico', 'rb')
    return FileResponse(file)

def Debug_Details(request, format=None, **kwargs):
    return debug.technical_500_response(request, *sys.exc_info(), status_code=400)
