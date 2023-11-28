import datetime,logging
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError
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
        company = validated_data['company']
        telegram_id = validated_data['telegram_id']
        username = validated_data['username']
        user_first_name = validated_data['user_first_name']
        user_last_name = validated_data.get('user_last_name','')
        if not user_last_name:
            user_last_name = ' '
        item_id = validated_data['item_id']
        order_type = validated_data['order_type']
        if order_type == 'food':
            food_id = item_id
        else:
            raise ValidationError('ابتدا غذا را انتخاب کنید')
        user = get_user_model().objects.get_or_create(username=str(telegram_id),telegram_id=telegram_id)[0]
        user.first_name = user_first_name
        user.last_name = user_last_name
        user.save()
        food = Food.objects.get(id=food_id)
        rice = food.have_rice
        order = Order.objects.create(food_id=food_id,participant=user.get_participant(company),company=company,rice=rice)
        return order

    
    def update(self, instance, validated_data):
        order_type = validated_data['order_type']
        if order_type == 'food':
            food = Food.objects.get(id=validated_data['item_id'])
            instance.food = food
            instance.rice = food.have_rice
        else :
            MAX_DESSERT_OR_BEVERAGE = int(instance.food.have_dessert) + int(instance.food.have_beverage) + int(instance.food.have_rice)
            current_dessert_or_beverage = int(instance.dessert!=None) + int(instance.beverage!=None) + int(instance.rice)
            if order_type == 'dessert':
                if  current_dessert_or_beverage < MAX_DESSERT_OR_BEVERAGE:
                    dessert_id = validated_data['item_id']
                    instance.dessert_id = dessert_id if dessert_id else None
                else :
                    raise ValidationError('نمیتوانید دسر را برای این غذا انتخاب کنید')
            elif order_type == 'beverage':
                if  current_dessert_or_beverage < MAX_DESSERT_OR_BEVERAGE:
                    beverage_id = validated_data['item_id']
                    instance.beverage_id = beverage_id if beverage_id else None
                else :
                    raise ValidationError('نمیتوانید نوشیدنی را برای این غذا انتخاب کنید')
            elif order_type == 'rice':
                if not instance.food.have_rice:
                    raise ValidationError('برای این غذا برنج تعریف نشده است')
                instance.rice = validated_data['rice']
            else:
                raise ValidationError('نوع سفارش مشخص نیست')
        MAX_DESSERT_OR_BEVERAGE = int(instance.food.have_dessert) + int(instance.food.have_beverage) + int(instance.food.have_rice)
        current_dessert_or_beverage = int(instance.dessert!=None) + int(instance.beverage!=None) + int(instance.rice)
        if MAX_DESSERT_OR_BEVERAGE-current_dessert_or_beverage >0:
            instance.dessert = None
            instance.beverage = None 
        instance.save()
        return instance