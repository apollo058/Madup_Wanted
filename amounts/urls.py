from django.urls import path
from amounts.views import AmountsListView


urlpatterns = [
    path('', AmountsListView.as_view()),
    ]
