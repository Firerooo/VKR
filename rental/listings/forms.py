from django import forms
from .models import Review, Apartment

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Напишите ваш отзыв...'})
        }

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = [
            "title", "description", "price", "city", "address", "latitude", "longitude", 
            "rooms", "square_meters", "max_people", "status", "amenities", "currency", "rental_period"
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.01"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "rooms": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "1"}),
            "square_meters": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.1"}),
            "max_people": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "1"}),
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
            "status": forms.Select(attrs={"class": "form-control"}),
            "amenities": forms.CheckboxSelectMultiple(),
            "currency": forms.Select(attrs={"class": "form-control"}),
            "rental_period": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_square_meters(self):
        square_meters = self.cleaned_data.get("square_meters")
        if square_meters is not None and square_meters < 0:
            raise forms.ValidationError("Квадратные метры не могут быть отрицательными.")
        return square_meters

    def clean_rooms(self):
        rooms = self.cleaned_data.get("rooms")
        if rooms is not None and rooms < 0:
            raise forms.ValidationError("Количество комнат не может быть отрицательным.")
        return rooms

    def clean_max_people(self):
        max_people = self.cleaned_data.get("max_people")
        if max_people is not None and max_people < 0:
            raise forms.ValidationError("Максимальное количество людей не может быть отрицательным.")
        return max_people