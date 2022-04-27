from django.shortcuts import get_object_or_404

from rest_framework          import status
from rest_framework.views    import APIView
from rest_framework.response import Response

from .models      import Client
from .serializers import ClientsSerializer

class ClientsListView(APIView):
    '''
    작성자 : 남기윤
    (POST) /clients
    (GET) /clients
    '''
    def post(self, request):
        data = request.data
        serializer = ClientsSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
            client_list = Client.objects.all()
            serailized_list= ClientsSerializer(client_list, many=True)
            return Response(serailized_list.data, status=200)


class ClientsDetailView(APIView):
    '''
    작성자 : 남기윤
    (GET) /clients/<int:pk>
    (PATCH) /clients/<int:pk>
    (DELETE) /clients/<int:pk>
    '''
    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        serializer = ClientsSerializer(client)
        return Response(serializer.data)

    def patch(self, request, pk):
        data = request.data
        client = Client.objects.get(pk=pk)
        serializer = ClientsSerializer(client, data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = Client.objects.get(pk=pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
