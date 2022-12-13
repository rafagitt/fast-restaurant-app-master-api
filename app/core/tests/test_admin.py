# from django.test import TestCase, Client
# from django.contrib.auth import get_user_model
# from django.urls import reverse


# class AdminSiteTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.admin_user = get_user_model().objects.create_superuser(
#             email='admin1@admin1.com',
#             password='passwordadmin'
#         )
#         self.client.force_login(self.admin_user)
#         self.user = get_user_model().objects.create_user(
#             email='testuser@gmail.com',
#             password='password',
#             name='Test user name'
#         )

#     def test_users_listed(self):
#         """Test that users are listed on user apge"""
#         url = reverse('admin:core_user_changelist')
#         response = self.client.get(url)
#         # print(response.content)
#         self.assertContains(response, self.user.name)
#         self.assertContains(response, self.user.email)

#     def test_user_page(self):
#         """Test that user edit page works"""
#         url = reverse('admin:core_user_change', args={self.user.id})
#         # admin/core/user/1
#         # print(url)
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)

#     def test_create_user_page(self):
#         """Test that the create user works"""
#         url = reverse('admin:core_user_add')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
