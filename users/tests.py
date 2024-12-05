from django.test import TestCase

from .forms import UserProfileForm
from .models import User, upload_for_users


class UserProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@yandex.com',
            password='password123',
            first_name='Олег',
            last_name='Олегов',
            phone='+79876543210',
            avatar=None
        )
        self.form_data = {
            'email': 'test@yandex.com',
            'first_name': 'Олег',
            'last_name': 'Олегов',
            'phone': '+79876543210',
            'avatar': None,
        }

    def test_user_profile_form_valid(self):
        form = UserProfileForm(data=self.form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_clean_first_name_invalid_empty(self):
        form = UserProfileForm(data={'first_name': ''}, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_clean_first_name_invalid_stop_word(self):
        form = UserProfileForm(data={'first_name': 'Не указано'},
                               instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_clean_last_name_invalid_empty(self):
        form = UserProfileForm(data={'last_name': ''}, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

    def test_clean_last_name_invalid_stop_word(self):
        form = UserProfileForm(data={'last_name': 'Не указано'},
                               instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

    def test_clean_phone_invalid_format(self):
        form = UserProfileForm(data={'phone': '123'}, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_clean_phone_valid(self):
        form = UserProfileForm(data={'phone': '+79876543210'},
                               instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.cleaned_data['phone'], '+79876543210')

    def test_upload_for_users(self):
        user = User(email='user@yandex.com')
        filename = 'avatar.png'
        expected_path = 'users/user@yandex.com/avatar.png'
        actual_path = upload_for_users(user, filename)
        self.assertEqual(actual_path, expected_path)
        self.assertEqual(user.__str__(), 'user@yandex.com')
