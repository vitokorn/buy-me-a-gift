from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from product.models import ProductCategory, Product
from users.models import User


class MainTest(APITestCase):
    def auth(self):
        user, created = User.objects.get_or_create(
            email="b@example.com", password="example24"
        )
        self.user = user
        refresh = RefreshToken.for_user(user)
        return self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(refresh.access_token)
        )


class AccountTests(MainTest):
    def test_singup(self):
        url = reverse("api:auth-signup")
        response = self.client.post(
            url, {"email": "b@example.com", "password": "example24"}
        )
        res = response.json()
        self.assertEqual(res["email"], "b@example.com")

    def test_singin(self):
        url = reverse("api:auth-login")
        response = self.client.post(
            url, {"email": "b@example.com", "password": "example24"}
        )
        self.assertTrue(response.status_code, 201)

    def test_reset_password(self):
        self.auth()
        url = reverse("api:auth-reset-password")
        self.client.post(
            url, {"old_password": "example24", "new_password": "example25"}
        )
        self.assertTrue(self.user.password, self.user.check_password("example25"))

    def test_refresh_token(self):
        user, created = User.objects.get_or_create(
            email="b@example.com", password="example24"
        )
        self.user = user
        refresh = RefreshToken.for_user(self.user)
        url = reverse("api:auth-refresh")
        response = self.client.post(url, {"refresh": str(refresh)})
        self.assertTrue(response.status_code, 201)


class ProductsTests(MainTest):
    def setUp(self):
        self.auth()
        self.category = ProductCategory.objects.create(name="Sparkling water")

        self.product = Product.objects.create(
            name="Sprite", price=1.15, rank=3, category=self.category
        )

    def test_product_create(self):
        url = reverse("api:product-create")
        # wrong category test
        response = self.client.post(
            url, {"name": "Bonaqua", "price": 1.00, "rank": 1, "category": 2}
        )
        self.assertEqual(response.status_code, 400)
        # right category test
        response = self.client.post(
            url, {"name": "Bonaqua", "price": 1.00, "rank": 1, "category": 1}
        )
        self.assertEqual(response.status_code, 201)

    def test_products_list(self):
        self.test_product_create()
        url = reverse("api:products-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"{url}?price_gt=1")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f"{url}?price_lt=1.10")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f"{url}?sorting=rank")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f"{url}?sorting=created_time")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f"{url}?sorting=created_tim")
        self.assertEqual(response.status_code, 400)

    def test_product_get(self):
        url = reverse("api:product-get", {self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_update(self):
        url = reverse("api:product-update", {self.product.id})
        # partial update
        response = self.client.patch(
            url, {"name": "Sprite diet", "category": self.category.id}
        )
        self.assertEqual(response.status_code, 200)
        # partial update
        response = self.client.put(
            url,
            {
                "name": "Sprite",
                "price": "1.20",
                "rank": 4,
                "category": self.category.id,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_product_delete(self):
        url = reverse("api:product-delete", {self.product.id})
        response = self.client.post(
            url, {"email": "b@example.com", "password": "example24"}
        )


class CategoryTests(MainTest):
    def setUp(self):
        self.auth()
        self.category = ProductCategory.objects.create(name="Sparkling water")

    def test_category_create(self):
        url = reverse("api:category-create")
        response = self.client.post(url, {"name": "Water"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"name": "Water"})

    def test_product_delete(self):
        url = reverse("api:category-remove", {self.category.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


class WishlistTests(MainTest):
    def setUp(self):
        self.auth()
        self.category = ProductCategory.objects.create(name="Sparkling water")
        self.category2 = ProductCategory.objects.create(name="Water")
        self.product = Product.objects.create(
            name="Sprite", price=1.15, rank=3, category=self.category
        )
        self.product2 = Product.objects.create(
            name="Cola", price=1.0, rank=2, category=self.category
        )
        self.product3 = Product.objects.create(
            name="Bonaqua", price=0.9, rank=1, category=self.category2
        )

    def test_wishlist_create(self):
        url = reverse("api:wishlist-create")
        response = self.client.post(
            url, {"products": [self.product.id, self.product3.id]}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 1, "user": 1, "products": [1, 3]})
        self.wishlist = response.json()["id"]

    def test_wishlist_create_error(self):
        url = reverse("api:wishlist-create")
        response = self.client.post(
            url, {"products": [self.product.id, self.product2.id, self.product3.id]}
        )
        self.assertEqual(response.status_code, 400)

    def test_wishlist_delete(self):
        self.test_wishlist_create()
        url = reverse("api:wishlist-delete", {self.wishlist})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_wishlist_id(self):
        self.test_wishlist_create()
        url = reverse("api:wishlist-id", {self.wishlist})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"user": "b@example.com", "products": [1, 3]})
