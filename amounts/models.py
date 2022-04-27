from django.db import models

from clients.models import Client


class Amount(models.Model):
    advertiser = models.ForeignKey(Client, on_delete=models.CASCADE)
    uid        = models.CharField(max_length=100)
    media      = models.CharField(max_length=50)
    date       = models.DateField()
    cost       = models.IntegerField(default=0)
    impression = models.IntegerField(default=0)
    click      = models.IntegerField(default=0)
    conversion = models.IntegerField(default=0)
    cv         = models.IntegerField(default=0)

    class Meta:
        db_table = 'amounts'
        indexes = [
            models.Index(fields=('date',),  name='date_idx')
        ]