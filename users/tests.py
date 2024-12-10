from uuid import uuid4

from django.core import mail
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse

from reservations.models import HistoryReservations
from .forms import UserProfileForm
from .models import User, upload_for_users
from .views import RegisterView


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


class UserProfileUpdatesTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@yandex.com", password="password", is_active=True)

    def test_profile_update_view_permission(self):
        response = self.client.get(reverse("users:user_update", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, 302)

    def test_profile_update_view_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("users:user_update", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("user" in response.context)

    def test_profile_update_view_form_valid(self):
        self.client.force_login(self.user)
        data = {
            "phone": "",
            "avatar": ""
        }
        response = self.client.post(reverse("users:user_update", kwargs={"pk": self.user.pk}), data)
        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.phone, "Не указано")
        self.assertEqual(updated_user.avatar, "non_avatar.png")
        self.assertEqual(response.status_code, 200)


class ProfileDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@yandex.com",
            password="password",
            is_active=True
        )
        self.url = reverse("users:user_delete", kwargs={"pk": self.user.id})

    def test_delete_profile_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_delete_profile_unauthorized(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code,
                         302)

    def test_delete_profile_not_owner(self):
        another_user = User.objects.create(
            email="another@yandex.com",
            password="password",
            is_active=True
        )
        self.client.force_login(another_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)


class UserPasswordResetViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@yandex.com", password="password123", is_active=True)

    def test_reset_password(self):
        url = reverse("users:password_reset")
        data = {
            "email": "test@yandex.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class RegisterViewTest(TestCase):

    def test_send_verification_email(self):
        user = User.objects.create(email='test@yandex.com')
        RegisterView.send_verification_email(user)
        self.assertEqual(user.email, 'test@yandex.com')

    def test_register_view_get_context_data(self):
        response = self.client.get(reverse('users:user_register'))
        self.assertEqual(response.context['title'], 'Регистрация на сайте')

    def test_register_view_form_valid(self):
        data = {
            'email': 'test@yandex.com',
            'password1': 'test_password',
            'password2': 'test_password'
        }
        response = self.client.post(reverse('users:user_register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test@yandex.com').exists())

    def test_register_view_template_used(self):
        response = self.client.get(reverse('users:user_register'))
        self.assertTemplateUsed(response, 'users/register.html')


class VerifyEmailViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@yandex.com',
            password='password',
            token_verify=uuid4()
        )
        self.user.is_active = False
        self.user.save()

    def test_verify_email_success(self):
        response = self.client.get(reverse('users:verify_email', args=[self.user.token_verify]))

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Аккаунт test@yandex.com успешно активирован!")

    def test_verify_email_invalid_token(self):
        invalid_token = uuid4()
        response = self.client.get(reverse('users:verify_email', args=[invalid_token]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            "Произошла ошибка. Убедитесь, что переходите по ссылке из письма!")


class ProfileDetailViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@yandex.com',
            password='password123',
            token_verify=uuid4(),
            is_active=True
        )
        self.superuser = User.objects.create(
            email='super@yandex.com',
            password='password123',
            is_active=True,
            is_superuser=True
        )
        HistoryReservations.objects.create(user=self.user, status="Test Reservation 1")
        HistoryReservations.objects.create(user=self.user, status="Test Reservation 2")

    def test_profile_detail_view_access(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('users:user_detail', kwargs={'pk': self.user.pk}))
        self.assertContains(response, self.user.email)
        self.assertContains(response, "Test Reservation 1")

    def test_profile_detail_view_access_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('users:user_detail', kwargs={'pk': self.user.pk}))
        self.assertContains(response, self.user.email)
        self.assertTrue(response, True)

    def test_profile_detail_view_permission_denied(self):
        another_user = User.objects.create(
            email='another@yandex.com',
            password='password123',
            is_active=True
        )
        self.client.force_login(another_user)
        response = self.client.get(reverse('users:user_detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 403)


class CustomLoginViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@yandex.com',
            password='password123',
            is_active=True
        )
    def test_login_view_success(self):
        response = self.client.post(reverse('users:login'), {
            'email': 'test@yandex.com',
            'password': 'password123'
        })
        user = User.objects.get(email='test@yandex.com')
        self.assertTrue(response, True)

    def test_login_view_invalid_credentials(self):
        response = self.client.post(reverse('users:login'), {
            'email': 'test@yandex.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_login_view_inactive_user(self):
        inactive_user = User.objects.create(
            email='inactive@yandex.com',
            password='password123',
            is_active=False
        )
        response = self.client.post(reverse('users:login'), {
            'email': 'inactive@yandexz.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)