from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from decimal import Decimal

from django.db import transaction
from .serializers import (RegisterSerializer,LoginSerializer,ProductMainCategorySerializer,ProductSerializer,OrderItemSerializer,OrderSerializer)
from .models import (Profile,ProductMainCategory,Product,Order,OrderItem)
from .permissions import IsAdminOrReadOnly

# Create your views here.


class RegisterView(generics.CreateAPIView):
    """User registration view."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


def get_tokens_for_user(user):
    """Helper to get JWT tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.validated_data['email']
        password=serializer.validated_data['password']

        try:
         user = User.objects.get(email=email)
        except User.DoesNotExist:
         return Response(
            {"error": "Invalid email or password"},
            status=status.HTTP_400_BAD_REQUEST
        )
        if not user.check_password(password):
            return Response({'error:invalid phone or password'},status=status.HTTP_400_BAD_REQUEST)
        
        tokens = get_tokens_for_user(user)
        return Response({
             'message': 'Login successful',
            'user_id': user.id,
            'username': user.username,
            'tokens': tokens

        })

class Create_Display_categoryView(generics.ListCreateAPIView):
   queryset=ProductMainCategory.objects.all()
   serializer_class=ProductMainCategorySerializer
   permission_classes = [IsAdminOrReadOnly]

class Retrieve_Update_Destroy_categoryView(generics.RetrieveUpdateDestroyAPIView):
   queryset=ProductMainCategory.objects.all()
   serializer_class=ProductMainCategorySerializer
   permission_classes = [IsAdminOrReadOnly]

class create_display_productView(generics.ListCreateAPIView):
   queryset=Product.objects.all()
   serializer_class=ProductSerializer
   permission_classes = [IsAdminOrReadOnly]

class Retrieve_Update_Destroy_productView(generics.RetrieveUpdateDestroyAPIView):
   queryset=Product.objects.all()
   serializer_class=ProductSerializer
   permission_classes = [IsAdminOrReadOnly]



class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        items = serializer.validated_data["items"]

        with transaction.atomic():

            order = Order.objects.create(
                user=request.user,
                status="pending"
            )

            total_amount = Decimal("0.00")

            for item in items:

                product = item["product"]

                quantity = item["quantity"]

                if quantity > product.stock:
                    return Response(
                        {
                            "error": f"{product.product_name} is out of stock."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                subtotal = product.price * quantity

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                    subtotal=subtotal
                )

                total_amount += subtotal

            order.total_amount = total_amount
            order.save()

        return Response(
            {
                "message": "Order created successfully",
                "order_id": order.id,
                "total_amount": order.total_amount,
                "status": order.status
            },
            status=status.HTTP_201_CREATED
        )





from ecommerce_app.models import Order
from .serializers import CreatePaymentSerializer
from .strategy import StripeStrategy, BkashStrategy


class CreatePaymentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = CreatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data["order_id"]
        provider = serializer.validated_data["provider"]

        try:
            order = Order.objects.get(
                id=order_id,
                user=request.user
            )
        except Order.DoesNotExist:
            return Response(
                {
                    "error": "Order not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if order.status == "paid":
            return Response(
                {
                    "error": "Order already paid."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if provider == "stripe":
            strategy = StripeStrategy()

        elif provider == "bkash":
            strategy = BkashStrategy()

        else:
            return Response(
                {
                    "error": "Invalid payment provider."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        payment = strategy.create_payment(order)

        return Response(
            {
                "message": "Payment initiated successfully.",
                "client_secret": payment["client_secret"],
                "payment_intent_id": payment["payment_intent_id"]
            },
            status=status.HTTP_200_OK
        )

