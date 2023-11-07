from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic.edit import CreateView
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import TemplateView, View
import requests as r
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

from services.models import Link, RedirectHistory

# Create your views here.
class Links(LoginRequiredMixin, TemplateView):
    template_name = 'links.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_links = Link.objects.filter(user=self.request.user, is_delete=False)

        data_links = [
        {
            'name': link.user_site_name,
            'url': [reverse('vpnemulator', kwargs={"user_site_name":link.user_site_name, "original_url":link.site_attrs}) if link.site_attrs else
                     reverse('vpnemulator_name', kwargs={"user_site_name":link.user_site_name})][0] ,
            'clicks': link.link_history.count(),

            'request_bytes': link.link_history.aggregate(Sum('data_request_bytes'))['data_request_bytes__sum'] or 0,
            'response_bytes': link.link_history.aggregate(Sum('data_response_bytes'))['data_response_bytes__sum'] or 0,
        }
        for link in user_links
        ]

        context["data_links"] = data_links

        return context
    

class VPNEmulator(LoginRequiredMixin, View):
    

    def get(self, request, *args, **kwargs):
        user_site_name = kwargs.get('user_site_name')
        original_url = kwargs.get('original_url') #/document/d/1OsSWOBLObDAJPWmBmH9iN2T6OgfhT658WG6mV7UGqik/edit#heading=h.ean7wmn8q4g
        
        user_link = Link.objects.filter(user=self.request.user, is_delete=False, user_site_name=user_site_name).first()

        if user_link:

            try:
                parsed_url = urlparse(user_link.original_url)
                base_url = f'{parsed_url.scheme}://{parsed_url.netloc}' #https://docs.google.com/
                response = r.get(urljoin(base_url, original_url))

                response_headers = response.headers
                headers_response = sum(len(key) + len(value) for key, value in response_headers.items())
                total_response = len(response.content) + headers_response

                request_headers = response.request.headers
                request_headers = sum(len(key) + len(value) for key, value in request_headers.items())

                body_request = 0
                if response.request.body:
                    body_request = len(response.request.body)

                request_size = request_headers + body_request

                link_obj = RedirectHistory.objects.create(data_request_bytes=request_size, data_response_bytes=total_response, link=user_link)

            except Exception as e:
                messages.warning(self.request, f'Error occured: {e}')
                return HttpResponseRedirect(reverse('services:links'))

            soup_obj = BeautifulSoup(response.content, 'html.parser')

            for tag in soup_obj.find_all(['img', 'script', 'link'], href=True):
                href = tag.get('href')
                if href and not href.startswith(('http://', 'https://')):
                    tag['href'] = base_url + href

            for tag in soup_obj.find_all(['img', 'script', 'link'], src=True):
                src = tag.get('src')
                if src and not src.startswith(('http://', 'https://')):
                    tag['src'] = base_url + src

            for tag in soup_obj.find_all(['form'], action=True):
                action = tag.get('action')
                if action and not action.startswith(('http://', 'https://')):
                    tag['action'] = base_url + src

            for a_tag in soup_obj.find_all('a', href=True):
                href = a_tag.get('href')
                if href and not href.startswith(('http://', 'https://')):
                
                    new_href = f'/{user_site_name}{href}/v'
                    a_tag['href'] = new_href

            return HttpResponse(
                str(soup_obj),
                status=response.status_code,
                content_type=response.headers.get('Content-Type', 'text/html')
            )
        else:
            messages.warning(self.request, f'Error occured: Wrong Url')
            return HttpResponseRedirect(reverse('services:links'))