from rest_framework import serializers

from .models import Client

class ClientsSerializer(serializers.ModelSerializer):
    '''
    작성자 : 남기윤
    '''
    class Meta:
        model = Client
        fields = (
            "id","name","manager","contact","address_code","address_detail",
            "created_at","updated_at",
            )
