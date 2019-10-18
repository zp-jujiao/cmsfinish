from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home),
    path('detail/',views.detail),
    path('subpage/',views.subpage),
    path('subajax/',views.subajax),
    path('subpage1/',views.subpage1),
    path('subpage2/',views.subpage2),
    path('detailajax/',views.detailajax),
    path('homeajax/',views.homeajax),
    # path('left/',views.left),
]