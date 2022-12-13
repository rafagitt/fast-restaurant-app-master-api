# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from core import models
# from unittest.mock import patch


# def sample_user(email='testuser@test.com', password='testuserpass'):
#     """Create a sample user"""
#     return get_user_model().objects.create_user(email, password)


# class ModelTests(TestCase):
#     def test_create_user_with_email_successful(self):
#         """Test creating a new user with an email is successful."""
#         email = 'testemail@gmail.com'
#         password = '12345'
#         user = get_user_model().objects.create_user(
#             email=email,
#             password=password
#         )
#         self.assertEqual(user.email, email, "email is not {0}".format(email))

#     def test_new_user_email_normalized(self):
#         """Test the email for a new user is normalized"""
#         email = 'testemail@Test.com'
#         user = get_user_model().objects.create_user(email, 'testemail123')
#         self.assertEqual(user.email, email.lower())

#     def test_new_user_invalid_email(self):
#         """Test creating user with no email error"""
#         with self.assertRaises(ValueError):
#             get_user_model().objects.create_user(None, 'test123')

#     def test_create_new_superuser(self):
#         """Test creating a new super user"""
#         user = get_user_model().objects.create_superuser(
#             'test@test.com',
#             'test123'
#         )
#         self.assertTrue(user.is_superuser)
#         self.assertTrue(user.is_staff)

#     def test_food_str(self):
#         """Test the food string representation"""
#         food = models.Food.objects.create(
#             name='Enchiladas Suizas',
#             time_order_minutes=25,
#             price=9.00
#         )
#         self.assertEqual(str(food), food.name)

#     def test_order_str(self):
#         """Test the order string representation"""
#         food = models.Food.objects.create(
#             name='Sushi',
#             time_order_minutes=35,
#             price=20.00
#         )
#         order = models.Order.objects.create(
#             user=sample_user(),
#             food=food,
#         )
#         order_string = f'Food Order: {order.food}, Client: {order.user}'
#         self.assertEqual(str(order), order_string)

#     @patch('uuid.uuid4')
#     def test_food_file_name_uuid(self, mock_uuid):
#         """Test that image is saved in the correct location"""
#         uuid = 'test-uuid'
#         mock_uuid.return_value = uuid
#         file_path = models.food_image_file_path(None, 'myimage.jpg')
#         exp_path = f'uploads/food/{uuid}.jpg'
#         self.assertEqual(file_path, exp_path)
