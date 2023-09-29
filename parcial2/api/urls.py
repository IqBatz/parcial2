from django.urls import path
from .views import *

urlpatterns = [
    path('ordenes/', OrdenesView.as_view(), name='get_ordenes'),
    path('ordenes/<int:id>', OrdenesView.as_view(), name='ordenes_id')
]
