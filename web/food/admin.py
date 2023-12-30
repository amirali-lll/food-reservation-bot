from django.contrib import admin
from .models import Participant, Order, DailyMenu, Company, Food, Dessert, Beverage


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_select_related = ('user', 'company')
    list_display = ('id', 'user', 'company')
    search_fields = ('user__username','user__first_name','user__last_name', 'company__name')
    autocomplete_fields = ('user', 'company')
    
    



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_select_related = ('food', 'dessert', 'beverage', 'participant', 'company','participant__user')
    list_display = ('id', 'food', 'dessert', 'beverage', 'participant', 'company')
    search_fields = ('participant__user__username','participant__user__first_name','participant__user__last_name', 'company__name')
    autocomplete_fields = ('food', 'dessert', 'beverage', 'participant', 'company')
    

@admin.register(DailyMenu)
class DailyMenuAdmin(admin.ModelAdmin):
    list_select_related = ('company',)
    list_display = ('id', 'company', 'day', 'meal')
    search_fields = ('company__name', 'day', 'meal')
    filter_horizontal = ('foods', 'desserts', 'beverages')
    autocomplete_fields = ('foods', 'company')
    filter_horizontal = ('beverages', 'desserts',)
    
    
    
    
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    
    
    
@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    autocomplete_fields = ('company',)
    list_select_related = ('company',)
    
@admin.register(Dessert)
class DessertAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Beverage)
class BeverageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    

    
    