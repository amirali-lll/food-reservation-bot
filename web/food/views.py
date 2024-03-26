import datetime
import logging
from django.db import models
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import DailyMenu,Order,Company
from .serializers import DailyMenuSerializer,OrderSerializer,MakeOrderSerializer

logger = logging.getLogger(__name__)



class DailyMenuViewSet(ReadOnlyModelViewSet):
    lookup_field = 'day'

    def get_queryset(self):
        company = self.request.company
        return DailyMenu.objects.select_related('company').filter(company__name=company)
    
    serializer_class = DailyMenuSerializer
    
    
class OrderViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        company = self.request.company
        return Order.objects\
            .select_related('company','food','dessert','beverage','participant')\
            .filter(company__name=company)
    # queryset = Order.objects.all()
    
    serializer_class = OrderSerializer
    
    @action(detail=False, methods=['get'])
    def today_export(self, request):
        # return the each food or dessert and beverage with count of orders
        company_name = request.company
        company = get_object_or_404(Company,name=company_name)
        today      = datetime.date.today()
        orders    = Order.objects.filter(created_at__date=today,company=company)
        foods     = orders.values('food__name').annotate(count=models.Count('food'))
        desserts  = orders.values('dessert__name').annotate(count=models.Count('dessert'))
        beverages = orders.values('beverage__name').annotate(count=models.Count('beverage'))
        rice_count = orders.filter(rice=True).count()
        # dont return if count is zero
        foods     = [food for food in foods if food['count'] != 0]
        desserts  = [dessert for dessert in desserts if dessert['count'] != 0]
        beverages = [beverage for beverage in beverages if beverage['count'] != 0]
        return Response({'foods':foods,'desserts':desserts,'beverages':beverages,'rice_count':rice_count}, status=status.HTTP_200_OK)
    

        
        
    @action(detail=False, methods=['get'])
    def today(self, request):
        # return the all orders of company with today date
        company_name = request.company
        company = get_object_or_404(Company,name=company_name)
        today = datetime.date.today()
        orders = Order.objects.filter(created_at__date=today,company=company)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        
    @action(detail=False, methods=['post','delete'])
    def order(self, request):
        logger.info(request.data)
        logger.info(request.method)
        logger.info(f"order for user {request.data['telegram_id']}...")
        # if the order with this telegram_id and today exists, update it otherwise create a new one
        serializer = MakeOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company_name = request.company
        company = get_object_or_404(Company,name=company_name)
        telegram_id = serializer.validated_data['telegram_id']
        order = Order\
            .objects\
            .filter(
                company=company,
                participant__user__telegram_id=telegram_id,
                created_at__date=datetime.date.today())\
                .first()
        if request.method == 'DELETE':
            if order:
                order.delete()
                return Response(status=status.HTTP_204_NO_CONTENT,data={'message':'سفارشت پاک شد🥲'})
            else:
                return Response(status=status.HTTP_404_NOT_FOUND, data={'error':'سفارشت رو پیدا نکردیم🥲'})
        try:
            logger.info(f"order for user {telegram_id}%%%...")
            if order:
                logger.info(f"update order for user {telegram_id}%%%...")
                serializer = MakeOrderSerializer(order, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(company=company)
        except Exception as e:
            print(e)
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    
    
