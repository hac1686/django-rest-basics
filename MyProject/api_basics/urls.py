from django.urls import path
from .views import article_list, article_detail # import all the functions

urlpatterns = [
    path('article/', article_list),
    path('detail/<int:pk>', article_detail),
        
]
