from django_filters import rest_framework as filters

from product.models import Product


class PriceFilterSet(filters.FilterSet):
    """
    Used for filtering results based on price_gt and price_lt. Includes sorting by rank and created_time
    """

    price_gt = filters.NumberFilter(field_name="price", lookup_expr="gt")
    price_lt = filters.NumberFilter(field_name="price", lookup_expr="lt")

    sorting = filters.OrderingFilter(
        fields=(
            ("rank", "rank"),
            ("created_time", "created_time"),
        )
    )

    class Meta:
        model = Product
        fields = ["price_gt", "price_lt"]
