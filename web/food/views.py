from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import DailyMenu
from .serializers import DailyMenuSerializer




class DailyMenuViewSet(ReadOnlyModelViewSet):
    lookup_field = 'day'

    def get_queryset(self):
        company = self.request.company
        return DailyMenu.objects.select_related('company').filter(company__name=company)
    
    serializer_class = DailyMenuSerializer
    

