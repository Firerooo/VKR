from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from listings.models import Apartment, Photo
from django.db.models import Count

def get_cities(request):
    query = request.GET.get("q", "").strip()
    cities = Apartment.objects.values_list("city", flat=True).annotate(count=Count("id")).filter(count__gt=0).distinct()
    
    if query:
        cities = [city for city in cities if query.lower() in city.lower()]

    return JsonResponse({"cities": list(cities)})

@require_POST
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    if request.user != photo.apartment.owner:
        return HttpResponseForbidden("У вас нет прав")
    photo.delete()
    return JsonResponse({"status": "ok"})
