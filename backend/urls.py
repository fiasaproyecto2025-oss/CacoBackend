from django.urls import path
from .views import predict_cacao

urlpatterns = [
    path('predict/', predict_cacao),
]