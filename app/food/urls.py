from django.urls import path, include
from rest_framework.routers import DefaultRouter
from food import views

# Generate routes through a viewset
router = DefaultRouter()
router.register('orders', views.OrderViewSet, basename='orders')
router.register(
    'admin-orders',
    views.OrderAdminViewSet,
    basename='admin-orders'
)
router.register('admin-foods', views.FoodAdminViewSet, basename='admin-foods')

app_name = 'food'

urlpatterns = [
    path('', include(router.urls)),
    path('foods/', views.FoodView.as_view(), name='foods')
]
