from rest_framework import serializers
from .models import Item,OrderItem,Order,Category
from core.serializers import registrationserializer
from core.models import Location,School

class ItemSerializer(serializers.ModelSerializer):
    vendor = registrationserializer(read_only=True)
    class Meta:
        model=Item
        fields=["id","vendor","title","price","delivery_fee","different_location_fee","delivery_date"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=["id","title"]

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model=School
        fields=["id","name"]

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Location
        fields=["id","name"]


class HomeSerializer(serializers.Serializer):
    categories = CategorySerializer(many=True)
    items = ItemSerializer(many=True)


class itemserializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields=["id","title","price","delivery_fee","different_location_fee","delivery_date"]

class OrderItemSerializer(serializers.ModelSerializer):
    item=itemserializer(read_only=True)
    vendor = registrationserializer(read_only=True)
    user = registrationserializer(read_only=True)

    class Meta:
        model=OrderItem
        fields=["id","item","vendor","user","is_ordered","is_removed","quantity","delivery_location"]

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(read_only=True,many=True)
    class Meta:
        model=Order
        fields=["id","items","is_ordered"]
