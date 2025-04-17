from ..models import Amenity, AmenityCategory

def get_amenities_by_category(apartment=None, delete=False):
    categories = {
        "Основные": AmenityCategory.MAIN,
        "Кухня": AmenityCategory.KITCHEN,
        "Спальня": AmenityCategory.BEDROOM,
        "Ванная комната": AmenityCategory.BATHROOM,
        "Другое": AmenityCategory.OTHER,
    }
    result = {}

    if apartment is None:
        for label, cat_code in categories.items():
            result[label] = Amenity.objects.filter(category=cat_code)
    else:
        selected_ids = set(apartment.amenities.all().values_list('id', flat=True))
        for label, cat_code in categories.items():
            qs = Amenity.objects.filter(category=cat_code)
            if delete:
                qs = qs.filter(id__in=selected_ids)
                amenities = [{'amenity': amenity, 'selected': True} for amenity in qs]
                if amenities:
                    result[label] = amenities
            else:
                amenities = [{'amenity': amenity, 'selected': amenity.id in selected_ids} for amenity in qs]
                result[label] = amenities
    return result
