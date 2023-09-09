from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(...):
    ...


class UserReadSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated and
                obj.followings.filter(user=request.user).exists()
                and not request.user.is_anonymous)


class ChangePasswordSerializer(serializers.Serializer):
    ...


class FollowSerializer(serializers.ModelSerializer):
    ...


class FollowAuthorSerializer(serializers.ModelSerializer):
    ...


class TagSerializer(serializers.ModelSerializer):
    ...


class IngredientSerializer(serializers.ModelSerializer):
    ...


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ...


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    ...


class RecipeSerializer(serializers.ModelSerializer):
    ...


class RecipeReadSerializer(serializers.ModelSerializer):
    ...


class RecipeCreateSerialzier(serializers.ModelSerializer):
    ...
