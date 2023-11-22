from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError



class Participant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participants')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='participants')
    
    
    def save(self, *args, **kwargs):
        if Participant.objects.filter(user=self.user, company=self.company).exists():
            raise ValidationError('User is already a participant of this company.')
        super(Participant, self).save(*args, **kwargs)
    
    
    
class Order(models.Model):
    food = models.ForeignKey('Food', on_delete=models.CASCADE)
    dessert = models.ForeignKey('Dessert', on_delete=models.CASCADE, null=True, blank=True)
    beverage = models.ForeignKey('Beverage', on_delete=models.CASCADE, null=True, blank=True)
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name='orders')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class DailyMenu(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='daily_menus')
    DAY_CHOICES = (
        ('SAT', 'Saturday'),        
        ('SUN', 'Sunday'),
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
    )
    # lunch or dinner
    MEAL_CHOICES = (
        ('LUN', 'Lunch'),        
        ('DIN', 'Dinner'),
    )
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    meal = models.CharField(max_length=3, choices=MEAL_CHOICES)
    foods = models.ManyToManyField('Food', related_name='daily_menus')
    desserts = models.ManyToManyField('Dessert', related_name='daily_menus')
    beverages = models.ManyToManyField('Beverage', related_name='daily_menus')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.company.name + ' ' + self.day + ' ' + self.meal
    
     
    
class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='company_images', blank=True)
    telegram_group_id = models.CharField(max_length=100,null=True,blank=True)
    telegram_group_link = models.CharField(max_length=100,null=True,blank=True)
    # participants FK is added to the Participant model
    # foods FK is added to the Food model

    

    def __str__(self):
        return self.name
    


class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    have_dessert = models.BooleanField(default=False)
    have_beverage = models.BooleanField(default=False)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='foods')
    def __str__(self):
        return self.name
    
class Dessert(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name
    
class Beverage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

