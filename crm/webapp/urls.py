from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import RoadNetworkViewSet




router = DefaultRouter()
router.register(r'roadnetworks', RoadNetworkViewSet)


urlpatterns = [
    path('', views.home, name=''),
    # path('us_cities_list/', views.us_cities_list, name='us_cities_list'),
    path('kandra_road_network', views.kandra_road_network, name='kandra_road_network'),
    path('visualize-road-network/', views.visualize_road_network, name='visualize_road_network'),
    path('centerslocationapi', views.centerslocationapi, name='centerslocationapi'),
    path('centersapi', views.centersapi, name='centersapi'),
    path('nyc-streets', views.nyc_streets, name='nyc_streets'),
    path('nyc-neighborhoods', views.nyc_neighborhoods, name='nyc_neighborhoods')
]