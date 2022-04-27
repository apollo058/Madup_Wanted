from django.db import models


class Client(models.Model):
    name           = models.CharField(max_length=50)
    manager        = models.CharField(max_length=50)
    contact        = models.CharField(max_length=50)
    address_code   = models.CharField(max_length=100)
    address_detail = models.TextField()
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clients'

    def __str__(self):
        return self.name