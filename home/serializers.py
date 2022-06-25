
from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = '__all__'

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OrderItem
        fields = ['quantity']