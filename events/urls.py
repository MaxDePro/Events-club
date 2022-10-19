from django.urls import path
from.views import *

urlpatterns = [
    path('', home, name='home'),
    path('<int:year>/<str:month>/', home, name='home')
]
