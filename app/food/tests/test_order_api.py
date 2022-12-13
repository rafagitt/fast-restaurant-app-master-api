# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
# from core.models import Food, Order
# from food.serializers import OrderDetailSerializer, OrderListSerializer


# ORDERS_URL = reverse('food:order-list')


# def detail_url(order_id):
#     """Order detail url"""
#     return reverse('food:order-detail', args=[order_id])


# def sample_food(**params):
#     """Create and return a sample food"""
#     defaults = {
#         'name': 'sample food',
#         'time_order_minutes': 10,
#         'price': 5.00
#     }
#     defaults.update(params)
#     return Food.objects.create(**defaults)


# class PublicOrdersApiTests(TestCase):
#     """Test unauthenticated Orders API access"""

#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             'user@user.com',
#             'pass1234'
#         )

#     def test_login_required(self):
#         """Test that login is required to access the endpoint"""
#         response = self.client.get(ORDERS_URL)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_login_require_for_detail(self):
#         """Test that login is required for detail"""
#         food = sample_food()
#         order = Order.objects.create(user=self.user, food=food)
#         url = detail_url(order.id)
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_login_require_for_create(self):
#         """
#         Test login is required for create
#         Without authentication but with the browser open
#         """
#         food = sample_food()
#         response = self.client.post(
#                    ORDERS_URL,
#                    {'user': self.user.id, 'food': food.id}
#                 )
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# class PrivateOrdersApiTests(TestCase):
#     """Test the private Orders API"""

#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             'user@user.com',
#             'pass1234'
#         )
#         self.client.force_authenticate(self.user)

#     def test_retrieve_orders_list(self):
#         """Test retrieving a list of orders"""

#         food_1 = sample_food()
#         food_2 = sample_food(name='sample food 2', price=11.00)
#         Order.objects.create(user=self.user, food=food_1)
#         Order.objects.create(user=self.user, food=food_2)
#         response = self.client.get(ORDERS_URL)
#         orders = Order.objects.filter(user=self.user).order_by(
#                                                      '-creation_date')
#         serializer = OrderListSerializer(orders, many=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, serializer.data)

#     def test_orders_limited_to_user(self):
#         """
#         Test that only orders for the authenticated
#         user are returned
#         """
#         food_1 = sample_food()
#         food_2 = sample_food(name='sample food 2', price=11.00)
#         user2 = get_user_model().objects.create_user(
#             'user2@user2.com',
#             'pass12345'
#         )
#         Order.objects.create(user=user2, food=food_1)
#         order = Order.objects.create(user=self.user, food=food_2)
#         response = self.client.get(ORDERS_URL)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['id'], order.id)

#     def test_view_order_detail(self):
#         """Test viewing a order detail"""
#         food = sample_food()
#         order = Order.objects.create(user=self.user, food=food)
#         url = detail_url(order.id)
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         serializer = OrderDetailSerializer(order)
#         self.assertEqual(response.data, serializer.data)

#     def test_create_order_successful(self):
#         """Test create a new order"""
#         food = sample_food()
#         response = self.client.post(ORDERS_URL, {'food': food.id})
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         exists = Order.objects.filter(user=self.user, food=food).exists()
#         self.assertTrue(exists)

#     def test_create_order_limited_per_day(self):
#         """
#         Test order that does not accept
#         more than one order per day
#         """
#         food = sample_food()
#         Order.objects.create(user=self.user, food=food)
#         response = self.client.post(ORDERS_URL, {'food': food.id})
#         error = {'error': 'You can not make more than one order per day'}
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(error, response.data)
