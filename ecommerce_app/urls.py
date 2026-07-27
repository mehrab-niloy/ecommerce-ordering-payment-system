from django.urls import path

from ecommerce_app.views import RegisterView,LoginView,Create_Display_categoryView,Retrieve_Update_Destroy_categoryView,create_display_productView,Retrieve_Update_Destroy_productView,OrderCreateAPIView,CreatePaymentAPIView
from .webhooks import stripe_webhook

urlpatterns = [
    
    path('register/',RegisterView.as_view(),name='regsiter'),
    path('login/',LoginView.as_view(),name='login'),

    path('add-display-main-category/',Create_Display_categoryView.as_view(),name='add-display-main-category'),
    path('main-category/<int:pk>/',Retrieve_Update_Destroy_categoryView.as_view(),name='category-detail'),
    path('add-display-product/',create_display_productView.as_view(),name='add-display-product'),
    path('product/<int:pk>/',Retrieve_Update_Destroy_productView.as_view(),name='product-detail'),
    path('order/',OrderCreateAPIView.as_view(),name='order'),
     path(
        "create/",
        CreatePaymentAPIView.as_view(),
        name="create-payment",
    ),
     path(
        "webhook/stripe/",
        stripe_webhook,
        name="stripe-webhook",
    ),
]