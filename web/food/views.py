import datetime
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import DailyMenu,Order,Company
from .serializers import DailyMenuSerializer,OrderSerializer,MakeOrderSerializer





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
    
    # def perform_create(self, serializer):
    #     serializer.save(participant=self.request.user.participant,company=self.request.company)
    
    # def perform_update(self, serializer):
    #     serializer.save(participant=self.request.user.participant,company=self.request.company)
    
    # def perform_destroy(self, instance):
    #     instance.delete()
        
        
    @action(detail=False, methods=['get'])
    def today(self, request):
        # return the all orders of company with today date
        company_name = request.company
        company = get_object_or_404(Company,name=company_name)
        today = datetime.date.today()
        orders = Order.objects.filter(created_at__date=today,company=company)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        
    @action(detail=False, methods=['post'])
    def order(self, request):
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
        if order:
            serializer = MakeOrderSerializer(order, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        try:
            serializer.save(company=company)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    
    
