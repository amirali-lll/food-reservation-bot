from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # participants FK is added to the Participant model
    def get_participant(self):
        return self.participants.first()
        # TODO temporary solution, should be replaced with a more robust one
        # that allows for multiple participants per user
        