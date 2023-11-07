from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic.edit import CreateView
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
import validators
from urllib.parse import urlparse

from .forms import CustomUserCreationForm, CustomUserEditForm, CustomPasswordChangeForm
from .models import CustomUser
from services.models import Link


# Create your views here.


class MainView(TemplateView):

    template_name = 'main.html'

    def post(self, request):
        url = request.POST.get("url")
        title = request.POST.get("title")
        if not title or not validators.url(url):
            messages.warning(self.request, 'Wrong data!')

        elif not self.request.user.is_authenticated:
            messages.warning(self.request, 'User have to be authenticated!')

        elif Link.objects.filter(user = self.request.user, user_site_name=title):
            messages.warning(self.request, 'You already have the same adress!')

        else:
            parsed_url = urlparse(url)
            query = parsed_url.path
            if parsed_url.query:
                query += '?' + parsed_url.query
            link_obj = Link.objects.create(original_url=url, user_site_name=title, user=self.request.user, site_attrs=query[1::])
            messages.success(self.request, 'Vpn adress was succesfully created!')
            return HttpResponseRedirect(reverse('services:links'))

        return HttpResponseRedirect(reverse('users:main'))


class LoginInterfaceView(LoginView):
    template_name = 'login.html'
    next_page = '/'
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main')
        return super().get(request, *args, **kwargs)
    

class LogoutInterfaceView(LogoutView):
    next_page = '/'


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main')
        return super().get(request, *args, **kwargs)
    

class ProfileView(UpdateView):
    model = CustomUser
    form_class = CustomUserEditForm
    template_name = 'profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been successfully updated.')
        return super().form_valid(form)
    

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('users:profile')
    template_name = 'change_password.html'
