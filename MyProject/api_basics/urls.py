from django.urls import path
from .views import article_list, article_detail, ArticleAPIView, ArticleDetails # import all the functions and classes from views

urlpatterns = [
    #path('article/', article_list), # the old one from def article list function
    path('article/', ArticleAPIView.as_view()), #new one using Class-based Views instead of one function
    #path('detail/<int:pk>', article_detail),
    path('detail/<int:id>', ArticleDetails.as_view()), #using the class view instead of function views
        
]
