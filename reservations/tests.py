from datetime import datetime

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from reservations.models import HistoryReservations, Reservation, Table
from reservations.validators import check_amount, phone_number
from reservations.views import ReservationUpdateView
from restaurant.models import Restaurant
from users.models import User


class ReservationsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.restaurant = Restaurant.objects.create(name="Московский",
                                                    city="МСК",
                                                    scheme_tables='non.jpg')
        self.restaurant_2 = Restaurant.objects.create(name="Питерский",
                                                      city="СПб",
                                                      scheme_tables='non.jpg')
        self.table = Table.objects.create(id=1,
                                          number=1,
                                          restaurant=self.restaurant,
                                          places="5",
                                          is_datetime=timezone.make_aware(
                                              datetime(2024,
                                                       12,
                                                       1,
                                                       hour=16)))
        self.table_2 = Table.objects.create(id=2,
                                            number=5,
                                            restaurant=self.restaurant,
                                            places="5",
                                            is_datetime=timezone.make_aware(
                                                datetime(2024,
                                                         12,
                                                         1,
                                                         hour=18)))
        self.user = User.objects.create(email='test@test.ru',
                                        password='wersdfxcv',
                                        is_active=True,
                                        is_superuser=True)
        self.user_2 = User.objects.create(email='test_2@test.ru',
                                          password='wersdfxcv',
                                          is_active=True)
        self.reservation = Reservation.objects.create(table=self.table,
                                                      user=self.user,
                                                      phone='+79876543210',
                                                      old_table=1)
        self.reservation_2 = Reservation.objects.create(table=self.table_2,
                                                        user=self.user_2,
                                                        phone='+79876543215',
                                                        old_table=2)
        self.history = HistoryReservations.objects.create(user=self.user,
                                                          status='Создали')
        self.view = ReservationUpdateView()
        self.view.request = self.factory.get('/')
        self.view.request.user = self.user
        self.view.object = self.reservation

    def test_str(self):
        self.assertEqual(self.restaurant.__str__(), 'Московский - МСК')
        self.assertEqual(
            self.table.__str__(),
            'Московский - МСК - Стол №1 2024-12-01 19:00:00')
        self.assertEqual(
            self.reservation.__str__(),
            'test@test.ru - Московский - МСК - Стол №1 2024-12-01 19:00:00')
        self.assertEqual(self.history.__str__(), 'Создали')
        self.reservation.table = self.table_2
        self.reservation.save()
        self.assertEqual(self.reservation.table, self.table_2)
        self.reservation.delete()

    def test_list_view_as_superuser(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('reservations:list_reservations'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.reservation.phone)
        self.assertContains(response, self.reservation_2.phone)

    def test_list_view_as_regular_user(self):
        self.client.force_login(self.user_2)
        response = self.client.get(reverse('reservations:list_reservations'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.reservation.phone)
        self.assertContains(response, self.reservation_2.phone)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('reservations:list_reservations'))
        self.assertRedirects(
            response,
            f'/users/?next={reverse("reservations:list_reservations")}')

    def test_update_reservation_as_owner(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse('reservations:update_reservations',
                    args=[self.reservation.pk]),
            {'phone': '+79876543211',
             'amount': 600,
             })
        self.reservation.refresh_from_db()

    def test_update_reservation_as_non_owner(self):
        self.client.force_login(self.user_2)
        self.client.get(reverse('reservations:update_reservations',
                                args=[self.reservation.pk]))

    def test_update_reservation_as_superuser(self):
        self.client.force_login(self.user)
        self.client.post(reverse('reservations:update_reservations',
                                 args=[self.reservation_2.pk]),
                         {
                             'phone': '+79876543212',
                             'amount': 600,
                         })
        self.reservation_2.refresh_from_db()

    def test_cache(self):
        cache.set('scheme_tables', [self.restaurant, self.restaurant_2])
        context = self.view.get_context_data()
        self.assertIn("scheme_tables", context)
        self.assertEqual(len(context["scheme_tables"]), 2)
        self.assertEqual(context["scheme_tables"][0].name, "Московский")
        self.assertEqual(context["scheme_tables"][1].name, "Питерский")

    def test_create_reservation(self):
        self.client.force_login(self.user)
        self.client.post(reverse('reservations:create_reservations'),
                         {
                             'table': self.table.id,
                             'phone': '+79876543210',
                             'old_table': 1
                         })
        reservation_exists = (Reservation.objects.
                              filter(phone='+79876543210').exists())
        self.assertTrue(reservation_exists)

    def test_delete_reservations_raise(self):
        self.client.force_login(self.user_2)
        response = self.client.post(reverse('reservations:delete_reservations',
                                            args=[self.reservation.pk]))
        self.assertEqual(response.status_code, 403)

    def test_delete_reservations_superuser(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('reservations:delete_reservations',
                                            args=[self.reservation_2.pk]))
        self.assertEqual(response.status_code, 302)


class CheckValidatorsTestCase(TestCase):

    def test_check_amount_valid(self):
        self.assertEqual(check_amount(500), 500)
        self.assertEqual(check_amount(7500), 7500)
        self.assertEqual(check_amount(10000), 10000)

    def test_check_amount_low(self):
        with self.assertRaises(ValidationError):
            check_amount(400)

    def test_check_amount_high(self):
        with self.assertRaises(ValidationError):
            check_amount(15000)

    def test_phone_number_valid(self):
        self.assertEqual(phone_number("+7 912 123-45-67"), "+7 912 123-45-67")
        self.assertEqual(phone_number("89121234567"), "89121234567")

    def test_phone_number_invalid(self):
        with self.assertRaises(ValidationError):
            phone_number("123")
        with self.assertRaises(ValidationError):
            phone_number("abcdefgh")
        with self.assertRaises(ValidationError):
            phone_number("+1 234 567 89")
