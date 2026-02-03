from rest_framework import serializers
from main.models import User, Article

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'nick', 'email', 'bio', 'created_at']

    

class ArticleSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'user', 'created_at']