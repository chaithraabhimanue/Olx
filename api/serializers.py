from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Userprofile
from api.models import Products,Questions,Answers

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","email","password","first_name","last_name",]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    user=Userserializer(read_only=True,many=False)
    class Meta:
        model=Userprofile
        # fields=["profile_pic","address","place","contact_number"]
        fields=["address","place","contact_number","profile_pic","user"]
    
class ProductSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    is_active=serializers.BooleanField(read_only=True)
    class Meta:
        model=Products
        fields="__all__"  

class QuestionSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    created_date=serializers.DateTimeField(read_only=True)
    class Meta:
        model=Questions
        fields=["id","user","created_date","product_name","description"]

class AnswerSerializers(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    created_date=serializers.DateField(read_only=True)

    class Meta:
        model=Answers
        fields=["id","questions","answer","user","created_date"]
