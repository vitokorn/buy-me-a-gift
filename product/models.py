from django.db import models


# Create your models here.
class Product(models.Model):
    """
    Stores a single product entry, related to :model:`product.ProductCategory`.
    """

    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    rank = models.IntegerField()
    category = models.ForeignKey("product.ProductCategory", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class ProductCategory(models.Model):
    """
    Stores a single product category entry
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)


class WishList(models.Model):
    """
    Stores a single wishlist entry, related to :model:`users.User` and multiple
    :model:`product.Product` values.
    """

    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    products = models.ManyToManyField("product.Product")
