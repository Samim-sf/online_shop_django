from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from store import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('collection', views.CollectionViewSet)
router.register('cart', views.CartViewSet)
router.register('customers', views.CustomerViewSet)


products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
# urlpatterns = router.urls

items_router = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
items_router.register('items', views.CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(items_router.urls))
]
