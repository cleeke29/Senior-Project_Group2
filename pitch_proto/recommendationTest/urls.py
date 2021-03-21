from django.urls import path
from . import views

urlpatterns = [
path('test/', views.RecPageOneView , name ='test'),
path('test2/', views.RecPageTwoView, name = 'test2'),
path('test3/', views.RecPageThreeView, name = 'test3'),
path('result/', views.ResultPageView, name = 'result'),
path('recommendations/', views.RecFinal, name = 'final')
]