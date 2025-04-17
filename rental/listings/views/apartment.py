import json
from datetime import datetime, date, time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from listings.models import Apartment, Photo, ViewHistory
from listings.forms import ApartmentForm
from django.db.models import Sum
from .helpers import get_amenities_by_category

@login_required
def create_apartment(request):
    if request.user.role != "seller":
        messages.warning(request, "У вас нет прав на добавление объявления!")
        return redirect("listings:home")

    if request.method == "POST":
        form = ApartmentForm(request.POST, request.FILES)
        files = request.FILES.getlist('photos')

        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.owner = request.user
            apartment.save()
            form.save_m2m()

            for file in files:
                Photo.objects.create(apartment=apartment, image=file)

            messages.success(request, "Объявление успешно добавлено!")
            return redirect("listings:my_listings")
    else:
        form = ApartmentForm()

    amenities_by_category = get_amenities_by_category()
    return render(request, "listings/apartment-form.html", {
        "form": form,
        "amenities_by_category": amenities_by_category,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
    })

def apartment_list(request):
    from listings.models import Apartment
    city = request.GET.get('city', '')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    max_people = request.GET.get('max_people')
    amenities = request.GET.getlist('amenities')
    status = request.GET.get('status')
    currency = request.GET.get('currency')
    rental_period = request.GET.get('rental_period')

    apartments = Apartment.objects.all()
    if not status:
        status = "RENT"

    if city:
        apartments = apartments.filter(city__iexact=city)
    if price_min:
        apartments = apartments.filter(price__gte=price_min)
    if price_max:
        apartments = apartments.filter(price__lte=price_max)
    if max_people:
        apartments = apartments.filter(max_people__gte=max_people)
    if status:
        apartments = apartments.filter(status=status)
    if amenities:
        apartments = apartments.filter(amenities__id__in=amenities).distinct()
    if currency:
        apartments = apartments.filter(currency=currency)
    if status == "RENT" and rental_period:
        apartments = apartments.filter(rental_period=rental_period)

    paginator = Paginator(apartments, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    markers = [{
        'lat': float(a.latitude),
        'lng': float(a.longitude),
        'price': float(a.price) if a.price else None,
        'currency': a.currency,
        'status': a.status,
        'rental_period': a.rental_period,
        'id': a.id,
    } for a in page_obj if a.latitude and a.longitude]

    apartment_photos = {apt.id: apt.photos.first() for apt in page_obj}
    amenities_by_category = get_amenities_by_category()

    return render(request, 'listings/apartments.html', {
        'page_obj': page_obj,
        'apartment_photos': apartment_photos,
        'city': city,
        'amenities_by_category': amenities_by_category,
        'selected_amenities': [str(a) for a in amenities],
        'selected_status': status,
        'selected_currency': currency,
        'selected_rental_period': rental_period,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'markers_json': json.dumps(markers),
        'MAP_ID': settings.MAP_ID,
    })

def apartment_detail(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    photos = apartment.photos.all()
    user = request.user
    amenities_by_category = get_amenities_by_category(apartment, True)

    today_start = datetime.combine(date.today(), time.min)
    today_end = datetime.combine(date.today(), time.max)
    
    if user.is_authenticated:
        was_viewed_today = ViewHistory.objects.filter(
            user=user,
            apartment=apartment,
            viewed_at__range=(today_start, today_end)
        ).exists()
    else:
        was_viewed_today = False
    
    if user.is_authenticated and apartment.owner != user and not was_viewed_today:
        ViewHistory.objects.get_or_create(user=user, apartment=apartment)
        apartment.total_views += 1
        apartment.save(update_fields=['total_views'])

    is_owner = user.is_authenticated and apartment.owner == user
    marker = [{
        'lat': float(apartment.latitude),
        'lng': float(apartment.longitude),
        'price': float(apartment.price) if apartment.price else None,
    }]
    return render(request, 'listings/apartment-detail.html', {
        'apartment': apartment,
        'photos': photos,
        'amenities_by_category': amenities_by_category,
        'is_owner': is_owner,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'markers_json': json.dumps(marker),
        'MAP_ID': settings.MAP_ID,
    })

@login_required
def apartment_edit(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)

    if request.user != apartment.owner:
        messages.error(request, "У вас нет прав для редактирования этого объявления.")
        return redirect('listings:apartment-detail', pk=apartment.pk)

    if request.method == "POST":
        post_data = request.POST.copy()
        for field in ['latitude', 'longitude']:
            if post_data.get(field):
                post_data[field] = post_data[field].replace(',', '.')

        form = ApartmentForm(post_data, request.FILES, instance=apartment)

        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.save()
            selected_amenity_ids = request.POST.getlist('amenities')
            apartment.amenities.set(selected_amenity_ids)
            for uploaded_file in request.FILES.getlist("photos"):
                Photo.objects.create(apartment=apartment, image=uploaded_file)

            messages.success(request, "Изменения успешно сохранены!")
            return redirect('listings:apartment-detail', pk=apartment.pk)
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = ApartmentForm(instance=apartment)

    return render(request, "listings/apartment-form.html", {
        'form': form,
        'apartment': apartment,  
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'amenities_by_category': get_amenities_by_category(apartment),
    })


@login_required
def apartment_delete(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    if request.user != apartment.owner:
        messages.error(request, "У вас нет прав для удаления этого объявления.")
        return redirect('listings:apartment-detail', pk=apartment.pk)
    
    if request.method == "POST":
        apartment.delete()
        messages.success(request, "Объявление успешно удалено!")
        return redirect('listings:apartments')
    return redirect('listings:apartment-detail', pk=apartment.pk)

@login_required
def my_listings(request):
    listings = Apartment.objects.filter(owner=request.user)
    total_views = listings.aggregate(total=Sum('total_views'))['total'] or 0
    return render(request, 'listings/my-listings.html', {
        'listings': listings,
        'total_views': total_views
    })
