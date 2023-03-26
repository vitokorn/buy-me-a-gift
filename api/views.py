from typing import Any
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from product.filters import PriceFilterSet
from product.models import Product, WishList, ProductCategory
from api.serializers import (
    ProductSerializer,
    SignInSerializer,
    ResetPasswordSerializer,
    WishlistSerializer,
    RegisterSerializer,
    CategorySerializer,
    WishlistRetrieveSerializer,
    ProductUpdateSerializer,
)
from users.models import User


class RegisterView(CreateAPIView):
    """
    Used for creating user account with email and password
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class SignInView(TokenObtainPairView):
    """
    Used for login into user account
    """

    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer


class ResetPasswordUpdateAPIView(UpdateAPIView):
    """
    Authorization required
    Used for password resetting
    """

    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer

    def update(self, request, *args, **kwargs):
        """
        Update function for ResetPasswordUpdateAPIView
        :param request: contains data from json body
        :param args:
        :param kwargs:
        :return: Response with data field
        """
        obj = self.request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")
            response = {"message": "Password updated successfully"}
            if not obj.check_password(old_password):
                response = {"error": "Old password is wrong"}
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
            if obj.check_password(new_password):
                response = {"error": "Both passwords are the same"}
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
            obj.set_password(new_password)
            obj.save()
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"error": "Data not valid"})


class ProductListView(ListAPIView):
    """
    Returns a list of all products.
    """

    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = PriceFilterSet
    filter_backends = (filters.DjangoFilterBackend,)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)

        ordered_queryset = filtered_queryset.order_by("-price")

        if not ordered_queryset:
            return Response(status=404)
        return self.list(request, *args, **kwargs)


class ProductRetrieveView(RetrieveAPIView):
    """
    Returns a single product by its id.
    """

    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        wl = get_object_or_404(Product, pk=kwargs["pk"])
        serializer = ProductSerializer(wl)
        return Response(serializer.data)


class ProductCreateView(CreateAPIView):
    """
    Authorization required
    Creates a single product.
    :returns created product
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ProductUpdateView(UpdateAPIView):
    """
    Authorization required
    Put method makes a complete update
    Patch method makes a partial update
    Category is a required field for partial update
    :returns updated product
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ProductUpdateSerializer
    queryset = Product.objects.all()

    def patch(self, request, *args: Any, **kwargs: Any) -> Response:
        return self.partial_update(request, *args, **kwargs)


class ProductDeleteView(DestroyAPIView):
    """
    Authorization required
    Deletes a single product
    :returns 204 status code and empty response body
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CategoryCreateView(CreateAPIView):
    """
    Authorization required
    Creates a single category
    :returns 201 status code and empty response body
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = ProductCategory.objects.all()


class CategoryDestroyView(DestroyAPIView):
    """
    Authorization required
    Deletes a single product
    :returns 204 status code and empty response body
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = ProductCategory.objects.all()


class WishListCreateView(CreateAPIView):
    """
    Authorization required
    Creates a single wishlist entity
    :returns 201 status code and response body with products list
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = WishlistSerializer
    queryset = WishList.objects.all()

    def create(self, request, *args, **kwargs):
        if WishList.objects.filter(user=request.user.id):
            return Response(
                {"error": "This user already got wishlist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        request = serializer.context["request"]
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(id=request.user.id)
        obj = serializer.save(user=user)
        return Response(
            {
                "id": obj.id,
                "user": request.user.id,
                "products": serializer.data["products"],
            },
            status=status.HTTP_201_CREATED,
        )


class WishListDeleteView(DestroyAPIView):
    """
    Authorization required
    Deletes a single wishlist entity
    :returns 204 status code
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = WishlistSerializer
    queryset = WishList.objects.all()


class WishListUserRetrieveAPIView(RetrieveAPIView):
    """
    Returns a single wishlist by user id.
     :returns 200 status code
    """

    permission_classes = (AllowAny,)
    serializer_class = WishlistRetrieveSerializer
    queryset = WishList.objects.all()

    def get(self, request, *args, **kwargs):
        wl = get_object_or_404(WishList, user=kwargs["user_id"])
        serializer = WishlistRetrieveSerializer(wl)
        return Response(serializer.data)
