# from django.contrib.auth import get_user_model
# import tempfile
# import os
# from PIL import Image
# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
# from core.models import Food
# from food.serializers import FoodSerializer


# FOOD_URL = reverse('food:food-list')


# def detail_url(food_id):
#     """Food detail url"""
#     return reverse('food:food-detail', args=[food_id])


# def sample_food(**params):
#     """Create and return a sample food"""
#     defaults = {
#         'name': 'sample food',
#         'time_order_minutes': 10,
#         'price': 5.00
#     }
#     defaults.update(params)
#     return Food.objects.create(**defaults)


# class PublicFoodApiTests(TestCase):
#     """Test unauthenticated food API access"""

#     status_without_permissions = status.HTTP_401_UNAUTHORIZED

#     def setUp(self):
#         self.client = APIClient()

#     def test_auth_not_require_for_get(self):
#         """Test that authentication is not required for read"""
#         response = self.client.get(FOOD_URL)
#         # print(self.status_without_permissions)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_auth_not_require_for_detail(self):
#         """Test that authentication is not required for detail"""
#         food = sample_food()
#         url = detail_url(food.id)
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_auth_permissions_require_for_create(self):
#         """
#         Test super user permissions is required for create
#         Without authentication but with the browser open
#         """
#         payload = {
#             'name': 'sandwich',
#             'time_order_minutes': 20,
#             'price': 5.0
#         }
#         response = self.client.post(FOOD_URL, payload)
#         self.assertEqual(
#             response.status_code,
#             self.status_without_permissions
#         )

#     def test_auth_permissions_require_for_update(self):
#         """Test super user permissions is required for update"""
#         food = sample_food()
#         payload = {
#             'name': 'pizza',
#             'time_order_minutes': 50,
#             'price': 10.0
#         }
#         url = detail_url(food.id)
#         response = self.client.put(url, payload)
#         self.assertEqual(
#             response.status_code,
#             self.status_without_permissions
#         )

#     def test_auth_permissions_require_for_patch(self):
#         """Test super user permissions is required for patch"""
#         food = sample_food()
#         payload = {'time_order_minutes': 11}
#         url = detail_url(food.id)
#         response = self.client.patch(url, payload)
#         self.assertEqual(
#             response.status_code,
#             self.status_without_permissions
#         )


# class CommonUserFoodApiTests(PublicFoodApiTests):
#     """Test Common User authenticated Food API access"""

#     status_without_permissions = status.HTTP_403_FORBIDDEN

#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             email='test@testapi.com',
#             password='test12345'
#         )
#         self.client.force_authenticate(self.user)


# class SuperUserFoodApiTests(TestCase):
#     """Test Super User food API access"""

#     def setUp(self):
#         self.client = APIClient()
#         self.superuser = get_user_model().objects.create_superuser(
#             email='supertest@test.com',
#             password='supertestpass'
#         )
#         self.client.force_authenticate(self.superuser)

#     def test_retrieve_foods(self):
#         """Test retrieving a list of foods"""
#         sample_food()
#         sample_food(name='sample food 2')
#         response = self.client.get(FOOD_URL)
#         foods = Food.objects.all().order_by('id')
#         serializer = FoodSerializer(foods, many=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, serializer.data)

#     def test_view_food_detail(self):
#         """Test viewing a food detail"""
#         food = sample_food()
#         url = detail_url(food.id)
#         response = self.client.get(url)
#         serializer = FoodSerializer(food)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_food_create(self):
#         """Test creating food"""
#         payload = {
#             'name': 'burguer',
#             'time_order_minutes': 60,
#             'price': 7.0
#         }
#         response = self.client.post(FOOD_URL, payload)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         food = Food.objects.get(id=response.data['id'])
#         for key in payload.keys():
#             self.assertEqual(payload[key], getattr(food, key))

#     def test_create_food_invalid(self):
#         """Test creating invalid food fails"""
#         payload = {'name': ''}
#         response = self.client.post(FOOD_URL, payload)
#         foods = Food.objects.all()
#         self.assertEqual(len(foods), 0)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_full_update_food(self):
#         """Test updating a food with put"""
#         food = sample_food()
#         payload = {
#             'name': 'torta fria',
#             'time_order_minutes': 9,
#             'price': 2.0
#         }
#         url = detail_url(food.id)
#         response = self.client.put(url, payload)
#         food.refresh_from_db()
#         self.assertEqual(food.name, payload['name'])
#         self.assertEqual(food.time_order_minutes,
#                          payload['time_order_minutes'])
#         self.assertEqual(food.price, payload['price'])
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         payload = {
#             'name': 'torta fria',
#             'time_order_minutes': 9
#         }
#         response = self.client.put(url, payload)
#         error = "{'price': [ErrorDetail(string='This field is required.', "
#         error += "code='required')]}"
#         self.assertEqual(error, str(response.data))
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_partial_update_food(self):
#         """Test updating a food with patch"""
#         food = sample_food()
#         payload = {
#             'name': 'torta caliente',
#             'time_order_minutes': 30,
#         }
#         url = detail_url(food.id)
#         response = self.client.patch(url, payload)
#         food.refresh_from_db()
#         self.assertEqual(food.name, payload['name'])
#         self.assertEqual(food.time_order_minutes,
#                          payload['time_order_minutes'])
#         self.assertEqual(float(response.data['price']), food.price)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_upload_food_with_image(self):
#         """Test uploading food with image"""
#         payload = {
#             'name': 'torta fria',
#             'time_order_minutes': 9,
#             'price': 2.0
#         }
#         with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
#             img = Image.new('RGB', (10, 10,))
#             img.save(ntf, format='JPEG')
#             ntf.seek(0)
#             payload['image'] = ntf
#             response = self.client.post(FOOD_URL, payload,
#                                         format='multipart')
#         food = Food.objects.first()
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertIn('image', response.data)
#         self.assertTrue(os.path.exists(food.image.path))
#         food.image.delete()

#     def test_upload_image_bad_request(self):
#         """Test uploading food with invalid image"""
#         payload = {
#             'name': 'torta fria',
#             'time_order_minutes': 9,
#             'price': 2.0,
#             'image': 'notimage'
#         }
#         response = self.client.post(FOOD_URL, payload,
#                                     format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
