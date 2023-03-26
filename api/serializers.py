from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.utils import validate_email_address
from product.models import Product, WishList, ProductCategory
from users.models import User


class SignInSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        """
        Get token from rest_framework_simplejwt
        :param user:
        :return:
        """
        token = super(SignInSerializer, cls).get_token(user)
        return token

    def validate(self, attrs):
        """
        Token validation with lifetime field
        :param attrs:
        :return:
        """
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["lifetime"] = int(refresh.access_token.lifetime.total_seconds())
        return data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "email", "password"]

    def create(self, validated_data):
        """
        Creating user account and check it is email for validation and duplicates
        :param validated_data:
        :return:
        """
        email = validated_data["email"]
        valid = validate_email_address(email)
        if not valid:
            raise serializers.ValidationError({"error": "Incorrect email"})
        check_user = User.objects.filter(email=email).first()
        if check_user:
            raise serializers.ValidationError({"error": "This email already used"})
        user = User.objects.create(
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["old_password", "new_password"]


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    rank = serializers.IntegerField()
    category = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all()
    )
    created_time = serializers.DateTimeField(required=False)

    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "price",
            "rank",
        ]

    def create(self, validated_data):
        """
        Create and return a new `Product` instance, given the validated data.
        """
        return Product.objects.create(**validated_data)


class ProductUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    rank = serializers.IntegerField(required=False)
    category = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all()
    )
    created_time = serializers.DateTimeField(required=False)

    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "price",
            "rank",
        ]

    def update(self, instance, validated_data):
        """
        Update and return an updated `ProductCategory` instance
        """
        instance.category = validated_data.get("category", instance.category)
        instance.name = validated_data.get("name", instance.name)
        instance.price = validated_data.get("price", instance.price)
        instance.rank = validated_data.get("rank", instance.rank)
        instance.save()
        return instance


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField()

    class Meta:
        model = ProductCategory
        fields = [
            "name",
        ]

    def create(self, validated_data):
        """
        Create and return a new `ProductCategory` instance, given the validated data.
        """
        name = validated_data.get("name")
        return ProductCategory.objects.create(name=name)


class WishlistSerializer(serializers.Serializer):
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True
    )

    class Meta:
        model = WishList
        fields = ["user", "products"]

    def filter_products(self, products):
        """
        Used to filter products, if two products contains same category, raises validation error
        :param products:
        :return: list of product_ids
        """
        product_ids = []
        categories_ids = []
        for product in products:
            if product.category in categories_ids:
                raise serializers.ValidationError(
                    ({"error": "This category already in list"})
                )
            categories_ids.append(product.category)
            product_ids.append(product.pk)
        return product_ids

    def create(self, validated_data):
        """
        create function
        :param validated_data:
        :return: wishlist object
        """
        products = validated_data.pop("products", [])
        wl = WishList.objects.create(**validated_data)
        wl.products.set(self.filter_products(products))
        return wl


class WishlistRetrieveSerializer(serializers.Serializer):
    user = serializers.CharField()
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True
    )

    class Meta:
        model = WishList
        fields = ["user", "products"]
