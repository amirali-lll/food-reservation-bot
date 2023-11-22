from django.conf import settings
from rest_framework import serializers
from .models import DailyMenu,Order ,Participant,Company,Food,Dessert,Beverage


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model  = settings.AUTH_USER_MODEL
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class DailyMenuSerializer(serializers.ModelSerializer):
    foods     = serializers.StringRelatedField(many=True)
    desserts  = serializers.StringRelatedField(many=True)
    beverages = serializers.StringRelatedField(many=True)
    
       
    class Meta:
        model  = DailyMenu
        fields = ('id','day', 'meal', 'foods', 'desserts', 'beverages', 'created_at', 'updated_at')
        

class ParticipantSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    user    = UserGetSerializer()
    class Meta:
        model  = Participant
        fields = ('id','user', 'company', 'created_at', 'updated_at')
        


class OrderSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer()
    food        = serializers.StringRelatedField()
    dessert     = serializers.StringRelatedField()
    beverage    = serializers.StringRelatedField()
    company     = serializers.StringRelatedField()
    class Meta:
        model  = Order
        fields = ('id','food', 'dessert', 'beverage', 'participant', 'company', 'created_at', 'updated_at')