from django.urls import path, include
from .views import article_list, article_detail, ArticleAPIView, ArticleDetails, GenericAPIView, ArticleViewSet # import all the functions and classes from views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('article',ArticleViewSet, basename='article')#

urlpatterns = [
    path('viewset/', include(router.urls)), #http://127.0.0.1:8000/viewset/article/
    path('viewset/<int:pk>', include(router.urls)),
    #path('article/', article_list), # the old one from def article list function
    path('article/', ArticleAPIView.as_view()), #new one using Class-based Views instead of one function
    #path('detail/<int:pk>', article_detail),
    path('detail/<int:id>', ArticleDetails.as_view()), #using the class view instead of function views
    path('generic/article/', GenericAPIView.as_view()), # to view without id but not good because it has the operations available that need id 
    path('generic/article/<int:id>', GenericAPIView.as_view()),
        
]
