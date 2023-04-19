from django.urls import path, include
from .import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'view1', views.a00005E5B0AFfView,basename='view1'),#1 w
router.register(r'instant', views.b01005E5B00FfView,basename='view2'),#2 w
router.register(r'blockload', views.c0100630100FfView,basename='view3'),#3 w
router.register(r'dailyload', views.d0100630200FfView,basename='view4'),#4 w
router.register(r'joins', views.joins,basename='joins'),#4 w
router.register(r'join', views.join,basename='join'),#4 w

urlpatterns = [
    path('', include(router.urls)),
    path('user/', views.DataProfile.as_view(), name='user'),

    path('joined/', views.joined, name='joined'),
]