from django.db import models
from django.contrib.auth.models import AbstractUser
from food.models import Participant


class User(AbstractUser):
    # participants FK is added to the Participant model
    telegram_id = models.PositiveBigIntegerField(null=True,blank=True,unique=True)
    
    def get_participant(self,company):
        if self.participants.first():
            return self.participants.first()
        else:
            participant = Participant.objects.create(user=self,company=company)
            return participant
        # TODO temporary solution, should be replaced with a more robust one
        # that allows for multiple participants per user
        