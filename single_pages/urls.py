from django.urls import path
from . import views

urlpatterns = [ # IP주소/
    path('', views.landing),            # IP 주소/
    path('about_us/', views.about_us)   # IP 주소/about_us/
]