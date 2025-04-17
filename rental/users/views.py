from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from listings.models import ViewHistory
from .forms import ProfileForm, UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import update_session_auth_hash

# Проверка на отсутствие авторизации
def not_logged_in(user):
    return not user.is_authenticated

@user_passes_test(not_logged_in, login_url='/')
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/') 
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {
        'form': form,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
        })

@user_passes_test(not_logged_in, login_url='/') 
def login_view(request):
    next_page = request.GET.get('next', reverse_lazy('users:profile')) 

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_page)
        else:
            messages.error(request, "Неверный логин или пароль.")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def profile(request):
    viewed_apartments = ViewHistory.objects.filter(user=request.user).select_related('apartment').order_by('-viewed_at')

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Изменения успешно сохранены!")
            return redirect('users:profile')
    else:
        profile_form = ProfileForm(instance=request.user)

    # Форма для изменения пароля
    password_form = PasswordChangeForm(user=request.user)

    return render(request, 'users/profile.html', {
        'user': request.user,
        'profile_form': profile_form,
        'password_form': password_form,
        'viewed_apartments': viewed_apartments,
    })


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Пароль успешно изменён.")
            update_session_auth_hash(request, user) 
            return redirect('users:profile')
        else:
            messages.error(request, "Не удалось изменить пароль. Проверьте, что вы правильно указали пароль.")
            profile_form = ProfileForm(instance=request.user)
            return render(request, 'users/profile.html', {
                'profile_form': profile_form,
                'password_form': form, 
            })
    return redirect('users:profile')

@login_required
def clear_history(request):
    history_qs = request.user.view_history.all()
    if history_qs.exists():
        history_qs.delete()
        messages.success(request, "История очищена!")
    else:
        messages.info(request, "История и так пуста!")
    return redirect('users:profile')