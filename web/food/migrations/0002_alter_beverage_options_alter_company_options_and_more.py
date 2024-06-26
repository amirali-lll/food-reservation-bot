# Generated by Django 4.2.7 on 2023-11-22 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beverage',
            options={'verbose_name': 'نوشیدنی', 'verbose_name_plural': 'نوشیدنی ها'},
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'شرکت', 'verbose_name_plural': 'شرکت ها'},
        ),
        migrations.AlterModelOptions(
            name='dailymenu',
            options={'verbose_name': 'منوی روزانه', 'verbose_name_plural': 'منوهای روزانه'},
        ),
        migrations.AlterModelOptions(
            name='dessert',
            options={'verbose_name': 'دسر', 'verbose_name_plural': 'دسرها'},
        ),
        migrations.AlterModelOptions(
            name='food',
            options={'verbose_name': 'غذا', 'verbose_name_plural': 'غذاها'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'سفارش', 'verbose_name_plural': 'سفارشات'},
        ),
        migrations.AlterModelOptions(
            name='participant',
            options={'verbose_name': 'کاربر', 'verbose_name_plural': 'کاربران'},
        ),
        migrations.AlterField(
            model_name='beverage',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='dessert',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='dailymenu',
            unique_together={('company', 'day', 'meal')},
        ),
        migrations.AlterUniqueTogether(
            name='food',
            unique_together={('name', 'company')},
        ),
    ]
