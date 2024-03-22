from django.urls import path, re_path
from .views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path('v1/', Provider_v1_List.as_view(), name='provider-v1'),
]

