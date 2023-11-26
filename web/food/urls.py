from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'daily_menus', views.DailyMenuViewSet, basename='daily_menus')
router.register(r'orders', views.OrderViewSet, basename='orders')



urlpatterns = [] + router.urls

