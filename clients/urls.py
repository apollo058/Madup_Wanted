from django.urls import path
from clients.views import ClientsListView, ClientsDetailView


urlpatterns = [
    path('clients/<int:pk>', ClientsDetailView.as_view()),
    path('clients', ClientsListView.as_view()),
    ]
