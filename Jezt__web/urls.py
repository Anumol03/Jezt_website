"""Jezt__web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

from myapp import views 
from myapp.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.index,name='index'),
    # path('about-us/',views.about_us,name='about-us'),
   
    path('ai/<str:email>/', views.Ai, name='ai'),
    path('clear-chat-history/', views.clear_chat_history, name='clear_chat_history'),
    path('email_request', views.email_approval, name='email_approval'),
    path('admin-approval/', views.admin_approval, name='admin_approval'),

    path('contact-us/',views.request_callback, name='contact-us'),
    path('csv/', views.download_csv, name='download_csv'),
    path('try',views.trial, name='trial'),
    path('team/',views.team_view,name='team'),

    path('tryus/', Tryus.as_view(), name='tryus'),
    path('calculate_similarity/', views.similarity_score_view, name='calculate_similarity'),

    # path('add_member/', views.add_member, name='add-member'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                        document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                       document_root=settings.MEDIA_ROOT)
