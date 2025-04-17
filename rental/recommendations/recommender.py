import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from listings.models import Apartment, ViewHistory
import pandas as pd

def get_recommendations(user, top_n=5):
    # История просмотров пользователя
    viewed = ViewHistory.objects.filter(user=user).values_list('apartment_id', flat=True)

    if not viewed:
        return []

    # Получаем все квартиры
    all_apartments = Apartment.objects.all().prefetch_related('amenities')
    df = []

    for apt in all_apartments:
        amenities = ', '.join([a.name for a in apt.amenities.all()])
        features = f"{apt.city} {apt.rooms} {apt.square_meters} {apt.price} {amenities}"
        df.append({
            'id': apt.id,
            'features': features,
            'apartment': apt
        })

    df = pd.DataFrame(df)

    if df.empty:
        return []

    # Векторизация
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['features'])

    # Средний вектор интересов пользователя
    user_indices = df[df['id'].isin(viewed)].index
    if not user_indices.any():
        return []

    user_vector = np.asarray(tfidf_matrix[user_indices].mean(axis=0))

    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()

    df['score'] = similarities
    df = df[~df['id'].isin(viewed)]
    df = df.sort_values(by='score', ascending=False)

    return [row['apartment'] for _, row in df.head(top_n).iterrows()]
