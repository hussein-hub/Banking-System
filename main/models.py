from django.db import models
from django.utils import timezone

# Create your models here.
class customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    balance = models.FloatField()
    dateCreated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class transactions(models.Model):
    # id = models.AutoField(default=0, primary_key=True)
    amount = models.FloatField()
    date = models.DateField(default=timezone.now)
    fromUser = models.CharField(max_length=100)
    toUser = models.ForeignKey(customer, max_length=100, on_delete=models.CASCADE, related_name="toUser")
    def __str__(self):
        return self.fromUser + " -> " + str(self.toUser)