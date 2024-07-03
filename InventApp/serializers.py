
from rest_framework import serializers
#from .models import User
from django.contrib.auth.models import User

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username'],
            #last_name=validated_data['last_name']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'quantity', 'price']


from rest_framework import serializers
from .models import Order, Product

class ProductOrderSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class OrderCreateSerializer(serializers.ModelSerializer):
    products = ProductOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'products', 'status', 'created_at', 'updated_at']
        read_only_fields = ('user', 'created_at', 'updated_at')

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        order.products = products_data
        order.save()
        return order
