from django.urls import path, re_path
from api.views import (
    SignInView,
    RegisterView,
    ResetPasswordUpdateAPIView,
    ProductListView,
    CategoryCreateView,
    CategoryDestroyView,
    ProductRetrieveView,
    ProductUpdateView,
    ProductDeleteView,
    ProductCreateView,
    WishListCreateView,
    WishListDeleteView,
    WishListUserRetrieveAPIView,
)
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "api"

urlpatterns = [
    # auth
    path("auth/signup/", RegisterView.as_view(), name="auth-signup"),
    path("auth/login/", SignInView.as_view(), name="auth-login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
    path(
        "auth/reset_password/",
        ResetPasswordUpdateAPIView.as_view(),
        name="auth-reset-password",
    ),
    # product
    path("products/", ProductListView.as_view(), name="products-list"),
    path("product/create/", ProductCreateView.as_view(), name="product-create"),
    path("product/get/<int:pk>/", ProductRetrieveView.as_view(), name="product-get"),
    path(
        "product/update/<int:pk>/", ProductUpdateView.as_view(), name="product-update"
    ),
    path(
        "product/delete/<int:pk>/", ProductDeleteView.as_view(), name="product-delete"
    ),
    # category
    path("category/create/", CategoryCreateView.as_view(), name="category-create"),
    path(
        "category/remove/<int:pk>/",
        CategoryDestroyView.as_view(),
        name="category-remove",
    ),
    # wishlist
    path("wishlist/create/", WishListCreateView.as_view(), name="wishlist-create"),
    path(
        "wishlist/delete/<int:pk>/",
        WishListDeleteView.as_view(),
        name="wishlist-delete",
    ),
    path(
        "wishlist/<int:user_id>/",
        WishListUserRetrieveAPIView.as_view(),
        name="wishlist-id",
    ),
]
