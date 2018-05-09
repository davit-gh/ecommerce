from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.conf import settings
from cartridge.shop.models import Product, ProductOption, Category
from django.test import TestCase
from django.urls import reverse


class MainTests(TestCase):
    """Main views testing class."""

    def setUp(self):
        """
        Set up test data.

        Initialize siteconfig, category, product and options.
        """
        # Create test product options
        for option_type in settings.SHOP_OPTION_TYPE_CHOICES:
            for i in range(10):
                name = "test%s" % i
                ProductOption.objects.create(type=option_type[0], name=name)
        self._options = ProductOption.objects.all()
        self._published1 = {"title": "test1", "status": CONTENT_STATUS_PUBLISHED}
        self._published2 = {"title": "test2", "status": CONTENT_STATUS_PUBLISHED}
        self._category1 = Category.objects.create(**self._published1)
        self._category2 = Category.objects.create(**self._published2)
        self._category1.options = self._options[:2]
        self._category2.options = self._options[2:4]
        self._product1 = Product.objects.create(**self._published1)
        self._product2 = Product.objects.create(**self._published2)
        self._product1.categories.add(self._category1)
        self._product2.categories.add(self._category2)

    def _filter_by_options(self, ids, result):
        data = {u'checkboxes': ids}
        response = self.client.post(reverse('filter_by_options'), data=data)
        self.assertQuerysetEqual(
            list(response.context['products']),
            result
        )

    def _recent_products(self):
        # Recently viewed
        response = self.client.get(reverse('recently_viewed'))
        self.assertFalse(response.context['products'])

        self.client.get(reverse('shop_product', args=['test1']))
        self.client.get(reverse('shop_product', args=['test2']))
        response = self.client.get(reverse('recently_viewed'))
        self.assertQuerysetEqual(
            list(response.context['products']),
            ['<Product: test1>', '<Product: test2>']
        )

    def test_views(self):
        """Test 'main' app views for errors."""
        # Product option checkboxes
        self._filter_by_options(
            [u'2', u'3'],
            ['<Product: test1>', '<Product: test2>']
        )

        self._filter_by_options(
            [u'5', u'6'],
            []
        )

        self._recent_products()
