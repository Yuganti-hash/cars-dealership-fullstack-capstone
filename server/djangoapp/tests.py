import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import analyze_review_sentiments

class DealershipFullStackTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        initiate()
        self.user = User.objects.create_user(
            username='unit_tester',
            password='TestPassword123!',
            first_name='Unit',
            last_name='Tester',
            email='unit.tester@example.com'
        )

    def test_car_models_and_makes(self):
        """Test CarMake and CarModel database persistence and query"""
        audi = CarMake.objects.get(name='Audi')
        self.assertEqual(audi.name, 'Audi')
        models = CarModel.objects.filter(car_make=audi)
        self.assertTrue(models.exists())
        self.assertTrue(any(m.name == 'Q5' for m in models))

    def test_get_cars_endpoint(self):
        """Test Task 14/15: /djangoapp/get_cars"""
        response = self.client.get('/djangoapp/get_cars')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('CarModels', data)
        self.assertGreater(len(data['CarModels']), 0)

    def test_get_dealers_endpoint(self):
        """Test Task 9: /djangoapp/get_dealers"""
        response = self.client.get('/djangoapp/get_dealers')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('dealers', data)
        self.assertGreater(len(data['dealers']), 0)

    def test_kansas_dealers_endpoint(self):
        """Test Task 11: /djangoapp/get_dealers/Kansas"""
        response = self.client.get('/djangoapp/get_dealers/Kansas')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        dealers = data['dealers']
        self.assertTrue(len(dealers) >= 3)
        for d in dealers:
            self.assertIn(d['state'].lower(), ['kansas', 'ks'])

    def test_dealer_by_id_endpoint(self):
        """Test Task 10: /djangoapp/dealer/1"""
        response = self.client.get('/djangoapp/dealer/1')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('dealer', data)
        self.assertEqual(data['dealer'][0]['id'], 1)

    def test_sentiment_analysis(self):
        """Test Task 16: Sentiment analysis of 'Fantastic services'"""
        sentiment = analyze_review_sentiments("Fantastic services")
        self.assertEqual(sentiment, "positive")

        response = self.client.get('/djangoapp/analyze/Fantastic%20services')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['sentiment'], 'positive')

    def test_user_authentication_flow(self):
        """Test Tasks 5 & 6: Login and Logout API"""
        # Login
        login_resp = self.client.post(
            '/djangoapp/login',
            data=json.dumps({"userName": "unit_tester", "password": "TestPassword123!"}),
            content_type='application/json'
        )
        self.assertEqual(login_resp.status_code, 200)
        self.assertEqual(login_resp.json()['status'], 'Authenticated')

        # Logout
        logout_resp = self.client.get('/djangoapp/logout')
        self.assertEqual(logout_resp.status_code, 200)
        self.assertEqual(logout_resp.json()['userName'], '')

    def test_user_registration(self):
        """Test Task 7: User registration endpoint"""
        reg_resp = self.client.post(
            '/djangoapp/register',
            data=json.dumps({
                "userName": "newuser_99",
                "password": "Password123!",
                "firstName": "New",
                "lastName": "User",
                "email": "newuser@example.com"
            }),
            content_type='application/json'
        )
        self.assertEqual(reg_resp.status_code, 200)
        self.assertEqual(reg_resp.json()['status'], 'Authenticated')
        self.assertTrue(User.objects.filter(username="newuser_99").exists())

    def test_add_and_get_reviews(self):
        """Test Tasks 8 & 22: Add and retrieve reviews"""
        add_resp = self.client.post(
            '/djangoapp/add_review',
            data=json.dumps({
                "dealership": 1,
                "name": "Unit Tester",
                "review": "Fantastic services and very courteous staff.",
                "purchase": True,
                "purchase_date": "2026-10-27",
                "car_make": "Audi",
                "car_model": "Q5",
                "car_year": 2024
            }),
            content_type='application/json'
        )
        self.assertEqual(add_resp.status_code, 200)

        get_resp = self.client.get('/djangoapp/get_reviews/1')
        self.assertEqual(get_resp.status_code, 200)
        reviews = get_resp.json()['reviews']
        self.assertTrue(len(reviews) > 0)
        self.assertTrue(any(r.get('name') == 'Unit Tester' for r in reviews))
