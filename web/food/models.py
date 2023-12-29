from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError



class Participant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participants')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='participants')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if Participant.objects.filter(user=self.user, company=self.company).exists():
            raise ValidationError('User is already a participant of this company.')
        super(Participant, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
    
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.company.name}"
    
    
class Order(models.Model):
    food = models.ForeignKey('Food', on_delete=models.CASCADE, null=True, blank=True)
    dessert = models.ForeignKey('Dessert', on_delete=models.CASCADE, null=True, blank=True)
    beverage = models.ForeignKey('Beverage', on_delete=models.CASCADE, null=True, blank=True)
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name='orders')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='orders')
    rice = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
        
        
    def get_price(self):
        price = 0
        if self.food:
            price += self.food.price
            if self.rice:
                price += self.food.rice_price
        if self.dessert:
            price += self.dessert.price
        if self.beverage:
            price += self.beverage.price
        return price

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
    
    class Meta :
        verbose_name = 'منوی روزانه'
        verbose_name_plural = 'منوهای روزانه'
        unique_together = ('company', 'day', 'meal')
    
     
    
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
    
    class Meta :
        verbose_name = 'شرکت'
        verbose_name_plural = 'شرکت ها'
    


class Food(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام')
    description = models.TextField(blank=True,verbose_name='توضیحات')
    have_rice = models.BooleanField(default=False,verbose_name='برنج دارد')
    price = models.PositiveIntegerField(default=0,verbose_name='قیمت')
    rice_price = models.PositiveIntegerField(default=settings.RICE_PRICE,verbose_name='قیمت برنج')
    restaurant = models.CharField(max_length=100,verbose_name='رستوران',blank=True,null=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='foods',verbose_name='شرکت')
    def __str__(self):
        
        return f"{self.name} - {self.restaurant}"
    
    class Meta:
        verbose_name = 'غذا'
        verbose_name_plural = 'غذاها'
        unique_together = ('name', 'company')
    
class Dessert(models.Model):
    name = models.CharField(max_length=100, unique=True,verbose_name='نام')
    description = models.TextField(blank=True,verbose_name='توضیحات')
    price = models.PositiveIntegerField(default=0,verbose_name='قیمت')
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'دسر'
        verbose_name_plural = 'دسرها'
    
class Beverage(models.Model):
    name = models.CharField(max_length=100, unique=True,verbose_name='نام')
    description = models.TextField(blank=True,verbose_name='توضیحات')
    price = models.PositiveIntegerField(default=0,verbose_name='قیمت')
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'نوشیدنی'
        verbose_name_plural = 'نوشیدنی ها'

