from django.urls import path
from . import views

urlpatterns = [
path('test/', views.RecPageOneView , name ='test'),
path('test2/', views.RecPageTwoView, name = 'test2'),
path('test3/', views.RecPageThreeView, name = 'test3'),
path('test4/', views.RecPageFourView , name ='test4'),
path('test5/', views.RecPageFiveView, name = 'test5'),
path('test6/', views.RecPageSixView, name = 'test6'),
path('test7/', views.RecPageSevenView , name ='test7'),
path('test8/', views.RecPageEightView, name = 'test8'),
path('test9/', views.RecPageNineView, name = 'test9'),
path('result/', views.ResultPageView, name = 'result'),
path('recommendations/', views.RecFinal, name = 'final')
]
