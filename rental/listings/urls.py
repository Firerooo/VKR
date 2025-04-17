from django.urls import path
from .views import general, apartment, reviews, api

app_name = 'listings'

urlpatterns = [
    path('', general.home, name='home'),
    path('about-us', general.about, name='about'),
    path('privacy-policy', general.privacy, name='privacy'),
    path('apartments', apartment.apartment_list, name='apartments'),
    path('apartment/<int:pk>/', apartment.apartment_detail, name='apartment-detail'),
    path('apartment/new/', apartment.create_apartment, name='apartment-create'),
    path('apartment/<int:pk>/edit/', apartment.apartment_edit, name='apartment-edit'),
    path('apartment_delete/<int:pk>/', apartment.apartment_delete, name='apartment-delete'),
    path('delete-photo/<int:photo_id>/', api.delete_photo, name='delete-photo'),
    path('get_cities/', api.get_cities, name='get_cities'),
    path('my-listings/', apartment.my_listings, name='my_listings'),
    path('reviews/', reviews.reviews_list, name='reviews_list'),
    path('add-review/', reviews.add_review, name='add_review'),
]

