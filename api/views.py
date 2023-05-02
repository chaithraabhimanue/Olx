from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin
from rest_framework import serializers
from rest_framework.viewsets import GenericViewSet
from api.serializers import Userserializer,ProfileSerializer,ProductSerializer,QuestionSerializer,AnswerSerializers
from api.models import Userprofile,Products,Questions,Answers
from rest_framework.viewsets import ModelViewSet
from rest_framework import authentication,permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action


class Usercreation(GenericViewSet,CreateModelMixin):
    serializer_class=Userserializer
    queryset=User.objects.all()


class ProfileView(ModelViewSet):
    serializer_class=ProfileSerializer
    queryset=Userprofile.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     return UserProfile.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        prof=self.get_object()
        if prof.user!=request.user:
            raise serializers.ValidationError("not allowed to perform")
        else:

           return super().destroy(request, *args, **kwargs)
        
class ProductsView(ModelViewSet):
    serializer_class=ProductSerializer
    queryset=Products.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        qs=Products.objects.all()
        if "category" in self.request.query_params:
            cat=self.request.query_params.get("category")
            qs=qs.filter(category=cat)
        if "price_gt" in self.request.query_params:
            price=self.request.query_params.get("price_gt")
            qs=qs.filter(price__gt=price)
        if "price_lt" in self.request.query_params:
            price=self.request.query_params.get("price_lt")
            qs=qs.filter(price__lt=price)
        return qs

class ChatBoxView(ModelViewSet):
    serializer_class=QuestionSerializer
    queryset=Questions.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        qus=self.get_object()
        if qus.user!=request.user:
            raise serializers.ValidationError("not allowed to perform")
        else:
            return super().destroy(request,*args,**kwargs)
        
    @action(methods=["post"],detail=True)
    def add_reply(self,request,*args,**kwargs):
        serializer=AnswerSerializers(data=request.data)
        quest=self.get_object()
        user=request.user
        if serializer.is_valid():
            serializer.save(question=quest,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
# class AnswersView(ModelViewSet):
#     serializer_class=AnswerSerializers
#     queryset=Answers.objects.all()
#     authentication_classes=[authentication.TokenAuthentication]
#     permission_classes=[permissions.IsAuthenticated]

#     def create(self,request,*args,**kwargs):
#         raise serializers.ValidationError("method not allowed")