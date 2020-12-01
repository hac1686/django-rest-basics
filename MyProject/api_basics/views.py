from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

#class for generic views
class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin,mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id' 
    #authentication_classes =[SessionAuthentication, BasicAuthentication] #checks for session auth first
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]#

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else: 
            return self.list(request)
    
    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


# class for API views/ class views
class ArticleAPIView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True) #many=true is to serialize the query set
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# to update and delete data - GET, PUT, DELETE
# Article details class will contain all the functions using APIViews
class ArticleDetails(APIView):

    def get_object(self,id):
       try:
           return Article.objects.get(id=id) #try to return the individual article

       except Article.DoesNotExist:
           return HttpResponse(status=status.HTTP_404_NOT_FOUND) # if id not found, return error

    def get(self, request, id):
        article = self.get_object(id) # get the article object by id and assign to article
        serializer = ArticleSerializer(article)  #assign to serializer
        return Response(serializer.data) # return the rest response

    def put(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @csrf_exempt  -removing, no longer need this
# function based views
@api_view(['GET', 'POST'])
def article_list(request):

    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        #data = JSONParser().parse(request) --no longer need to parse the data with Response import
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt -- changing this to api_view
@api_view(['GET','PUT','DELETE'])
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk) #try to assign the individual article

    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND) # if id not found, return error

    if request.method == 'GET':
        serializer = ArticleSerializer(article)  #if GET, serialize the individual article
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


