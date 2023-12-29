from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    # path('onecity/<id>', views.onecity)
]
