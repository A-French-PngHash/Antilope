# Tell python how to transform model into json data we want to use

from django import forms
from rest_framework import serializers
from .models import User, Activity

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    surname = serializers.CharField()
    
    def create(self, validated_data):
        name, surname = validated_data["name"], validated_data["surname"]
        user = User(name = validated_data["name"], surname = validated_data["surname"], username = username)
        user.save()
        username = f"{surname}.{name}"
        groups = [username]
        user.add_groups(groups)
        user.save()
        return user
    
    class Meta:
        model = User
        fields = ('name', 'surname')

class TileDataRequestSerializer(serializers.Serializer):
    topleft = serializers.ListField(child= serializers.IntegerField(), min_length = 2, max_length= 2)
    bottomright = serializers.ListField(child= serializers.IntegerField(), min_length = 2, max_length= 2)
    group = serializers.CharField()

class UploadActivityForm(forms.Form):
    title = forms.CharField(max_length=50)
    gpx_file = forms.FileField()