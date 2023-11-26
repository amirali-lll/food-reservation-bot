import datetime,logging
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import DailyMenu,Order ,Participant,Company,Food,Dessert,Beverage

logger = logging.getLogger(__name__)

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Food
        fields = ('id','name')

class DessertSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Dessert
        fields = ('id','name')

class BeverageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Beverage
        fields = ('id','name')


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model  = settings.AUTH_USER_MODEL
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class DailyMenuSerializer(serializers.ModelSerializer):
    foods     = FoodSerializer(many=True)
    desserts  = DessertSerializer(many=True)
    beverages = BeverageSerializer(many=True)
    
       
    class Meta:
        model  = DailyMenu
        fields = ('id','day', 'meal', 'foods', 'desserts', 'beverages', 'created_at', 'updated_at')
        


# TODO  we have unknown error here
class ParticipantSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    user    = UserGetSerializer()
    class Meta:
        model  = Participant
        fields = ('id','user', 'company', 'created_at', 'updated_at')
        


class OrderSerializer(serializers.ModelSerializer):
    user        = serializers.StringRelatedField(read_only=True,source='participant.user.first_name')
    food        = FoodSerializer(required=False)
    dessert     = DessertSerializer(required=False)
    beverage    = BeverageSerializer(required=False)
    company     = serializers.StringRelatedField(required=False)

    class Meta:
        model  = Order
        fields = ('id','food','user', 'dessert', 'beverage', 'company', 'created_at', 'updated_at')
                


class MakeOrderSerializer(OrderSerializer):
    telegram_id = serializers.IntegerField(required=False,write_only=True)
    username    = serializers.CharField(required=False,write_only=True)
    user_first_name = serializers.CharField(required=False,write_only=True)
    order_type  = serializers.CharField(required=False,write_only=True)
    item_id = serializers.IntegerField(required=False,write_only=True)
    rice = serializers.BooleanField(required=False,write_only=True)
    
    
    class Meta:
        model  = Order
        fields = ('id','item_id','company', 'created_at', 'updated_at','telegram_id','username','user_first_name','order_type')
    
    
    
    def create(self, validated_data):
        company = validated_data['company']
        telegram_id = validated_data['telegram_id']
        username = validated_data['username']
        user_first_name = validated_data['user_first_name']
        item_id = validated_data['item_id']
        order_type = validated_data['order_type']
        if order_type == 'food':
            food_id = item_id
        else:
            raise ValueError('ابتدا غذا را انتخاب کنید')
        user = get_user_model().objects.get_or_create(username=username,telegram_id=telegram_id,first_name=user_first_name)[0]
        food = Food.objects.get(id=food_id)
        rice = food.have_rice
        order = Order.objects.create(food_id=food_id,participant=user.get_participant(company),company=company,rice=rice)
        return order

    
    def update(self, instance, validated_data):
        order_type = validated_data['order_type']
        if order_type == 'food':
            instance.food_id = validated_data['item_id']
        elif order_type == 'dessert':
            if  instance.food.have_dessert or (instance.food.have_rice and instance.order.rice==False):
                instance.dessert_id = validated_data['item_id']
            else :
                raise ValueError('نمیتوانید دسر را برای این غذا انتخاب کنید')
        elif order_type == 'beverage':
            if not instance.food.have_beverage:
                raise ValueError('این غذا نوشیدنی ندارد')
            instance.beverage_id = validated_data['item_id']
        elif order_type == 'rice':
            if not instance.food.have_rice:
                raise ValueError('برای این غذا برنج تعریف نشده است')
            instance.rice = validated_data['rice']
        else:
            raise ValueError('نوع سفارش مشخص نیست')
        instance.save()
        return instance