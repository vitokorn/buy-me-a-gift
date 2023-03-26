from django.test import TestCase
from product.models import Product, ProductCategory, WishList
from users.models import User


class CategoryTestCase(TestCase):
    def test_create_oroduct_category(self):
        category = ProductCategory.objects.create(name="Water")
        self.assertEqual(category.name, "Water")


class ProductTestCase(TestCase):
    def test_create_product(self):
        # create category
        category_1 = ProductCategory.objects.create(name="Water")
        self.assertEqual(category_1.name, "Water")

        product = Product.objects.create(
            name="Bonaqua", price=1.00, rank=1, category=category_1
        )

        self.assertEqual(product.name, "Bonaqua")
        self.assertEqual(product.price, 1.00)
        self.assertEqual(product.rank, 1)
        self.assertEqual(product.category, category_1)


class WishListTestCase(TestCase):
    def test_create_wishlist(self):
        category_1 = ProductCategory.objects.create(name="Water")
        self.assertEqual(category_1.name, "Water")
        category_2 = ProductCategory.objects.create(name="Sparkling water")
        self.assertEqual(category_2.name, "Sparkling water")

        first = Product.objects.create(
            name="Bonaqua", price=1.00, rank=1, category=category_1
        )
        second = Product.objects.create(
            name="Cola", price=1.20, rank=2, category=category_2
        )

        self.assertEqual(first.name, "Bonaqua")
        self.assertEqual(first.price, 1.00)
        self.assertEqual(first.rank, 1)
        self.assertEqual(first.category, category_1)

        self.assertEqual(second.name, "Cola")
        self.assertEqual(second.price, 1.20)
        self.assertEqual(second.rank, 2)
        self.assertEqual(second.category, category_2)

        user = User.objects.create(email="a@example.com", password="example24")

        wishlist = WishList.objects.create(user=user)
        wishlist.products.add(first, second)
        self.assertQuerysetEqual(
            wishlist.products.all().order_by("id"), [first, second]
        )
