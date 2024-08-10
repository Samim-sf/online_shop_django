from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from store import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet,basename='product')
router.register('collection', views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]
