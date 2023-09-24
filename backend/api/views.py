from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from users.models import Follow

from .filters import RecipeFilter
from .pagination import CustomPagination
from .serializers import (CustomUserCreateSerializer, CustomUserReadSerializer,
                          FavoriteSerializer, FollowSerializer,
                          FollowToSerializer, IngredientSerializer,
                          PasswordSerializer, RecipeCreateSerializer,
                          RecipeReadSerializer, ShoppingCartSerializer,
                          TagSerializer)
from .utils import create_shopping_cart_report

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class UserViewSet(
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    filterset_fields = ('username',)
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return CustomUserReadSerializer
        return CustomUserCreateSerializer

    @action(
        methods=('get',),
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=('post',),
        detail=False,
        serializer_class=PasswordSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def set_password(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data.get('current_password')
        new_password = serializer.validated_data.get('new_password')
        if not user.check_password(old_password):
            return Response(
                {'message': 'Неверный пароль'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(new_password)
        user.save()
        return Response(
            {'message': 'Пароль успешно изменен'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        methods=('get',),
        detail=False,
        serializer_class=FollowSerializer,
        permission_classes=(IsAuthenticated,),
        pagination_class=CustomPagination
    )
    def subscriptions(self, request):
        subscriptions = request.user.follower.all()
        serializer = self.get_serializer(subscriptions)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=('post',),
        serializer_class=FollowToSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, pk=None):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request, 'id': pk}
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save(id=pk)
        return Response(
            {'message': 'Подписка успешно создана',
             'data': response_data},
            status=status.HTTP_201_CREATED
        )

    @subscribe.mapping.delete
    def delete_subscribe(self, request, pk=None):
        subscription = get_object_or_404(
            Follow, user=self.request.user,
            author=get_object_or_404(User, pk=pk)
        )
        subscription.delete()
        return Response(
            {'message': 'Успешная отписка'},
            status=status.HTTP_204_NO_CONTENT
        )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=('post',),
        detail=True,
        serializer_class=FavoriteSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk=None):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request, 'recipe_id': pk}
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save(id=pk)
        return Response(
            {
                'message': 'Рецепт успешно добавлен в избранное.',
                'data': response_data
            },
            status=status.HTTP_201_CREATED
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        get_object_or_404(
            Favorite, user=self.request.user,
            recipe=get_object_or_404(Recipe, pk=pk)).delete()
        return Response(
            {'message': 'Рецепт успешно удален из избранного'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        methods=('post',),
        detail=True,
        serializer_class=ShoppingCartSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk=None):
        # if self.request.method == 'POST':
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request, 'recipe_id': pk}
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save(id=pk)
        return Response(
            {
                'message': 'Рецепт успешно добавлен в список покупок',
                'data': response_data
            },
            status=status.HTTP_201_CREATED
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        get_object_or_404(
            ShoppingCart,
            user=self.request.user,
            recipe=get_object_or_404(Recipe, pk=pk)
        ).delete()
        return Response(
            {'message': 'Рецепт успешно удален из списка покупок'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=self.request.user)
        buy_list_text = create_shopping_cart_report(shopping_cart)
        response = HttpResponse(buy_list_text, content_type="text/plain")
        response['Content-Disposition'] = (
            'attachment; filename=shopping-cart.txt'
        )
        return response
