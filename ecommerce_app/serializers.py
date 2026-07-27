from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile,ProductMainCategory,Product,OrderItem,Order,Payment


class RegisterSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(required=True,write_only=True)
    first_name= serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name','last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        email = validated_data.pop('email')
        first_name = validated_data.pop('first_name')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=first_name,
            email=email,
            last_name=self.validated_data['last_name']
        )
        Profile.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class ProductMainCategorySerializer(serializers.ModelSerializer):
   

    class Meta:
        model = ProductMainCategory
        fields = [
            "id",
            "main_cat_name",
            "description",
            "created_by",
            "is_active",
        ]


class ProductSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "main_category",
            "price",
            "stock",
            "sku",
            "description",
            "created_by",
            "created_at",
            "updated_at",
            "is_active",
        ]

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            "product",
            "quantity"
        ]

class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "items"
        ]



class PaymentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Payment

        fields = "__all__"

        read_only_fields = (
            "transaction_id",
            "status",
            "raw_response",
        )


class CreatePaymentSerializer(serializers.Serializer):

    order_id = serializers.IntegerField()

    provider = serializers.ChoiceField(
        choices=[
            "stripe",
            "bkash"
        ]
    )