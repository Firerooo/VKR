from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
 path('recommendations/', views.recommendations_view, name='recommendations'),
]

