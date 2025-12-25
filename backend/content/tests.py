from rest_framework.test import APITestCase
from django.urls import reverse
from .models import HeroSlide, Stat

class ContentAPITest(APITestCase):
    def setUp(self):
        HeroSlide.objects.create(title='Slide 1', subtitle='Sub 1', image='hero/1.jpg', order=1)
        HeroSlide.objects.create(title='Slide 2', subtitle='Sub 2', image='hero/2.jpg', order=2)
        Stat.objects.create(number='100', label='Students', order=1)

    def test_hero_slides_list(self):
        url = '/api/content/hero-slides/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_stats_list(self):
        url = '/api/content/stats/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

