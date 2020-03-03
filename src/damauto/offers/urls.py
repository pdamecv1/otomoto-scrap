from django.urls import path
from offers import views

urlpatterns = [
    path('offers/', views.OfferList.as_view()),
    path('offers/<int:pk>/', views.OfferDetail.as_view()),
]
