from rest_framework import serializers
from core.models import Food, Order
from user.serializers import UserSerializer


class FoodSerializer(serializers.ModelSerializer):
    """Serialize food"""
    class Meta:
        model = Food
        fields = ('id', 'name', 'time_order_minutes', 'price', 'image')
        read_only_fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for order objects"""
    class Meta:
        model = Order
        fields = (
            'id',
            'food',
            'creation_date',
            'completed',
            'subtotal',
            'discount',
            'total',
            'canceled'
        )
        read_only_fields = (
            'id',
            'creation_date',
            'completed',
            'subtotal',
            'discount',
            'total',
            'canceled'
        )


class OrderFoodSerializer(serializers.ModelSerializer):
    """Serialize food of order"""
    class Meta:
        model = Food
        fields = ('name', 'image')
        read_only_fields = ('name', 'image')


class OrderListSerializer(OrderSerializer):
    """Serializer for list order objects"""
    class Meta:
        model = Order
        fields = (
            'id',
            'food',
            'creation_date',
            'completed',
            'canceled'
        )
        read_only_fields = (
            'id',
            'food',
            'creation_date',
            'completed',
            'canceled'
        )
    food = OrderFoodSerializer(read_only=True)
    creation_date = serializers.DateTimeField(
        format="%d/%m/%Y %H:%M",
        read_only=True
    )


class OrderDetailSerializer(OrderSerializer):
    """Serialize a order detail"""
    food = FoodSerializer(read_only=True)
    creation_date = serializers.DateTimeField(
        format="%d/%m/%Y %H:%M",
        read_only=True
    )


class OrderAdminSerializer(OrderSerializer):
    """Serializer for order objects (Manage Admin)"""
    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'food',
            'creation_date',
            'canceled',
            'completed',
            'subtotal',
            'discount',
            'total'
        )
        read_only_fields = (
            'id',
            'user',
            'food',
            'creation_date',
            'canceled',
            'completed',
            'subtotal',
            'discount',
            'total'
        )
    user = UserSerializer(read_only=True)
    food = OrderFoodSerializer(read_only=True)
    creation_date = serializers.DateTimeField(
        format="%d/%m/%Y %H:%M",
        read_only=True
    )


class OrderAdminDetailSerializer(OrderAdminSerializer):
    """Serialize a food detail"""
    food = FoodSerializer(read_only=True)
