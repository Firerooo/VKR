from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from recommendations.recommender import get_recommendations



@login_required
def recommendations_view(request):
    apartments = get_recommendations(request.user)
    return render(request, 'recommendations/recommendations.html', {'apartments': apartments})
