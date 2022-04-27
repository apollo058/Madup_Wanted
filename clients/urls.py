from django.urls import path
from clients.views import ClientsListView, ClientsDetailView


urlpatterns = [
    path('/<int:pk>', ClientsDetailView.as_view()),
    path('', ClientsListView.as_view()),
    ]
