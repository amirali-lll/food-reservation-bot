import datetime,logging
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import DailyMenu,Order ,Participant,Company,Food,Dessert,Beverage
from .validators import validate_order_price

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
        fields = ('id', 'username', 'first_name', 'last_name')


class DailyMenuSerializer(serializers.ModelSerializer):
    foods     = FoodSerializer(many=True)
    desserts  = DessertSerializer(many=True)
    beverages = BeverageSerializer(many=True)
    
       
    class Meta:
        model  = DailyMenu
        fields = ('id','day', 'meal', 'foods', 'desserts', 'beverages', 'created_at', 'updated_at')
        


# TODO  we have unknown error here
class ParticipantSerializer(serializers.ModelSerializer):
    # company = serializers.StringRelatedField(source='company.name')
    user    = serializers.StringRelatedField(source='user.first_name')
    class Meta:
        model  = Participant
        fields = ('id','user','created_at', 'updated_at')
        


class OrderSerializer(serializers.ModelSerializer):
    user        = serializers.SerializerMethodField(method_name="get_user")
    food        = FoodSerializer(required=False)
    dessert     = DessertSerializer(required=False)
    beverage    = BeverageSerializer(required=False)
    company     = serializers.StringRelatedField(required=False)

    class Meta:
        model  = Order
        fields = ('id','food','user', 'dessert', 'beverage','rice', 'company', 'created_at', 'updated_at')
        
    def get_user(self, obj):
        return f"{obj.participant.user.first_name} {obj.participant.user.last_name}"
                


class MakeOrderSerializer(OrderSerializer):
    telegram_id = serializers.IntegerField(required=False,write_only=True)
    username = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    user_first_name = serializers.CharField(required=False,write_only=True)
    user_last_name = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    order_type  = serializers.CharField(required=False,write_only=True)
    item_id = serializers.IntegerField(required=False,write_only=True)
    

    class Meta:
        model  = Order
        fields = ('id','item_id','company','rice', 'created_at', 'updated_at','telegram_id','username','user_first_name','user_last_name','order_type')
    
    
    
    def create(self, validated_data):
        logger.info(f"create order for user {validated_data['telegram_id']}...")
        company = validated_data['company']
        telegram_id = validated_data['telegram_id']
        username = validated_data['username']
        user_first_name = validated_data['user_first_name']
        user_last_name = validated_data.get('user_last_name','')
        if not user_last_name:
            user_last_name = ' '
        user = get_user_model().objects.get_or_create(username=str(telegram_id),telegram_id=telegram_id)[0]
        user.first_name = user_first_name
        user.last_name = user_last_name
        user.save()
        item_id = validated_data['item_id']
        order_type = validated_data['order_type']
        # set item order, it may be food or dessert or beverage
        order = None
        item_price = 0
        if order_type == 'food':
            food = Food.objects.get(id=item_id)
            item_price = food.price
            rice = food.have_rice
            if rice:
                item_price += food.rice_price
            validate_order_price(order,item_price)
            order = Order.objects.create(food=food,rice=rice,company=company,participant=user.get_participant(company))
        elif order_type == 'dessert':
            item_price = Dessert.objects.get(id=item_id).price
            validate_order_price(order,item_price)
            order = Order.objects.create(dessert_id=item_id,company=company,participant=user.get_participant(company))
        elif order_type == 'beverage':
            item_price = Beverage.objects.get(id=item_id).price
            validate_order_price(order,item_price)
            order = Order.objects.create(beverage_id=item_id,company=company,participant=user.get_participant(company))
        else:
            raise ValidationError('ابتدا غذا را انتخاب کنید')
            
        logger.info(f"order {order_type}:{item_id} for user {user.id}:{user.username}|{user.first_name} is successful")
        return order

    
    def update(self, instance, validated_data):
        logger.info(f"update order {instance.id} for user {instance.participant.user.id}:{instance.participant.user.username}|{instance.participant.user.first_name} is successful")
        order_type = validated_data['order_type']
        item_id = validated_data.get('item_id',0)
        if order_type == 'food':
            if item_id==0:
                instance.food = None
                instance.rice = False
            else :
                food = Food.objects.get(id=item_id)
                instance.food = food
                instance.rice = food.have_rice
        elif order_type == 'dessert':
            if item_id==0:
                instance.dessert = None
            else:
                dessert = Dessert.objects.get(id=item_id)
                instance.dessert = dessert
        elif order_type == 'beverage':
            if item_id==0:
                instance.beverage = None
            else:
                beverage = Beverage.objects.get(id=item_id)
                instance.beverage = beverage
        elif order_type == 'rice':
            if not instance.food:
                raise ValidationError('😕ابتدا غذا را انتخاب کنید')
            if not instance.food.have_rice:
                raise ValidationError('🥲برای این غذا برنج نداریم')
            wanna_rice = validated_data['rice']
            instance.rice = wanna_rice
        else:
            raise ValidationError('نوع سفارش را انتخاب کنید')
        validate_order_price(instance,0)
        instance.save()
        return instance