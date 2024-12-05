from datetime import datetime

from django import forms
from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from .forms import ContactForm, StyleFormMixin
from .models import (Description, HistoryRestaurant, MissionsRestaurant,
                     Restaurant, Services, StaffRestaurant, upload,
                     upload_for_bg, upload_for_restaurant)


class RestaurantTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Хороший ресторан",
                                                    city="Москва",
                                                    tables_count=5,
                                                    street="Улица хорошая",
                                                    house_number="12")

    def test_restaurant_create(self):
        rest = self.restaurant
        self.assertEqual(rest.name, "Хороший ресторан")
        self.assertEqual(rest.city, "Москва")
        self.assertEqual(rest.tables_count, 5)
        self.assertEqual(rest.street, "Улица хорошая")
        self.assertEqual(rest.house_number, "12")
        self.assertEqual(rest.__str__(), "Хороший ресторан - Москва")

    def test_none_fields(self):
        restaurant = Restaurant.objects.create(
            id=50,
            name="Московский",
            city="Москва",
            tables_count=4,
            scheme_tables=f'{upload_for_restaurant(self, "photo.jpg")}'
        )
        self.assertEqual(restaurant.scheme_tables, 'restaurant/photo.jpg')
        self.assertIsNone(restaurant.street)

    def tearDown(self):
        self.restaurant.delete()


class StaffRestaurantTestCase(TestCase):
    def setUp(self):
        self.staff = StaffRestaurant.objects.create(first_name="Гриша",
                                                    last_name="Гришев",
                                                    position="Сантехник",
                                                    date_employment=datetime(
                                                        2020, 12, 30))

    @freeze_time("2024-12-04")
    def test_created(self):
        staff = self.staff
        self.assertEqual(staff.__str__(), "Гриша Гришев")
        self.assertEqual(staff.date_employment.strftime("%d.%m.%Y %H:%M"),
                         '30.12.2020 00:00')
        self.assertEqual(staff.experience.days, 4)
        self.assertEqual(staff.experience.months, 11)
        self.assertEqual(staff.experience.years, 3)
        self.assertEqual(staff.naming_day, 'дня')
        self.assertEqual(staff.naming_month, 'месяцев')
        self.assertEqual(staff.naming_year, 'года')

        staff_2 = StaffRestaurant.objects.create(
            first_name="Олег",
            last_name="Олегов",
            position="Работник",
            photo=f'{upload(self.staff, "photo_staff.jpg")}')
        self.assertEqual(staff_2.photo, 'staff/Гришев Гриша/photo_staff.jpg')

    def test_null_field(self):
        staff = self.staff
        self.assertEqual(staff.is_published, True)
        self.assertEqual(staff.photo, 'non_avatar.png')

    @freeze_time("2024-12-04")
    def test_naming(self):
        staff_3 = StaffRestaurant.objects.create(first_name="Ольга",
                                                 last_name="Ольгова",
                                                 position="Работник",
                                                 date_employment=datetime(
                                                     2018, 7, 14))
        self.assertEqual(staff_3.experience.days, 20)
        self.assertEqual(staff_3.experience.months, 4)
        self.assertEqual(staff_3.experience.years, 6)
        self.assertEqual(staff_3.naming_day, 'дней')
        self.assertEqual(staff_3.naming_month, 'месяца')
        self.assertEqual(staff_3.naming_year, 'лет')

        staff_4 = StaffRestaurant.objects.create(first_name="Роман",
                                                 last_name="Романов",
                                                 position="Робот",
                                                 date_employment=datetime(
                                                     2022, 12, 13))

        self.assertEqual(staff_4.experience.days, 21)
        self.assertEqual(staff_4.experience.months, 11)
        self.assertEqual(staff_4.experience.years, 1)
        self.assertEqual(staff_4.naming_day, 'день')
        self.assertEqual(staff_4.naming_month, 'месяцев')
        self.assertEqual(staff_4.naming_year, 'год')

    def tearDown(self):
        self.staff.delete()


class MissionsRestaurantTestCase(TestCase):
    def setUp(self):
        self.mission = MissionsRestaurant.objects.create(
            mission="Миссия1",
            description="Добрая",
            serial_number=1)

    def test_created(self):
        mission = self.mission
        self.assertEqual(mission.mission, "Миссия1")
        self.assertEqual(mission.serial_number, 1)
        self.assertEqual(mission.__str__(), "Миссия1")


class HistoryRestaurantTestCase(TestCase):
    def setUp(self):
        self.history = HistoryRestaurant.objects.create(
            year="2024",
            activity="Событие")

    def test_created(self):
        history = self.history
        self.assertEqual(history.year, "2024")
        self.assertEqual(history.activity, "Событие")
        self.assertEqual(history.__str__(), "Событие")


class DescriptionTestCase(TestCase):
    def setUp(self):
        self.description = Description.objects.create(
            description="Описание",
            background=f'{upload_for_bg(self, "bg.jpg")}')

    def test_created(self):
        description = self.description
        self.assertEqual(description.description, "Описание")
        self.assertEqual(self.description.background, 'bg/bg.jpg')
        self.assertEqual(description.__str__(), "Описание")


class ServicesTestCase(TestCase):
    def setUp(self):
        self.services = Services.objects.create(
            service="Готовим")

    def test_created(self):
        services = self.services
        self.assertEqual(services.service, "Готовим")
        self.assertEqual(services.is_published, True)
        self.assertEqual(services.__str__(), "Готовим")


class TestStyleFormMixin(StyleFormMixin, forms.Form):
    test_field = forms.CharField()


class ContactFormTest(TestCase):
    def test_contact_form_fields(self):
        form = ContactForm()
        self.assertTrue(form.fields['email'].required)
        self.assertTrue(form.fields['phone'].required)
        self.assertTrue(form.fields['message'].required)

    def test_contact_form_valid_data(self):
        valid_data = {
            'email': 'test@yandex.com',
            'phone': '1234567890',
            'message': 'Привет!'
        }
        form = ContactForm(data=valid_data)
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid_data(self):
        invalid_data = {
            'email': 'test@yandex',
            'phone': '',
            'message': 'Привет'
        }
        form = ContactForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertIn('email', form.errors)


class IndexViewTest(TestCase):
    def setUp(self):
        self.url = reverse('restaurant:index')

    def test_get_request_renders_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/index.html')

    def test_form_submission_success(self):
        valid_data = {
            'email': 'test@yandex.com',
            'phone': '1234567890',
            'message': 'привет'
        }
        response = self.client.post(self.url, data=valid_data)
        self.assertRedirects(response, reverse('restaurant:index'))

    def test_form_submission_invalid(self):
        invalid_data = {
            'email': 'invalid-email',
            'phone': '',
            'message': 'привет'
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/index.html')
        self.assertIn('email', response.context['form'].errors)


class AboutViewTest(TestCase):
    def setUp(self):
        self.history_item = HistoryRestaurant.objects.create(
            year=2020, activity="Открылись")
        self.history_item2 = HistoryRestaurant.objects.create(
            year=2021, activity="Закрылись")
        self.mission_item = MissionsRestaurant.objects.create(
            serial_number=1, description="Миссия 1")
        self.mission_item2 = MissionsRestaurant.objects.create(
            serial_number=2, description="Миссия 2")

        self.staff_item = StaffRestaurant.objects.create(
            first_name="Игорь", position="Шеф", is_published=True)
        self.staff_item2 = StaffRestaurant.objects.create(
            first_name="Олег", position="СуШеф", is_published=False)
        self.url = reverse('restaurant:about')

    def test_get_request_renders_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/about.html')

    def test_context_data(self):
        response = self.client.get(self.url)
        self.assertIn('history', response.context)
        self.assertIn('missions', response.context)
        self.assertIn('staff', response.context)
        self.assertEqual(len(response.context['history']), 2)
        self.assertEqual(len(response.context['missions']), 2)
        self.assertEqual(len(response.context['staff']), 1)
        self.assertEqual(response.context['title'], 'О ресторане')
        self.assertEqual(response.context['history'][0], self.history_item2)
