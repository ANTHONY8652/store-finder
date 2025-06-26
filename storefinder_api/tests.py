from django.test import TestCase
from django.urls import reverse

class NearestStoreTestCase(TestCase):

    def test_missing_coordinates(self):
        response = self.client.get("/nearest-stores/")
        self.assertEqual(response.status_code, 400)
    
    def test_invalid_coordinates(self):
        response = self.client.get("/nearest-stores/?latitude=abc&longitude=def")
        self.assertEqual(response.status_code, 400)
    
    def test_invalid_product(self):
        response = self.client.get("/nearest-stores/?latitude=abc&longitude=def&product=ghijk") 
        self.assertEqual(response.status_code, 400)
    
    def test_valid_coordinates_and_product(self):
        response = self.client.get("/nearest-stores/?latitude=1.23&longitude=36.57&product=bread")
        self.assertIn(response.status_code, [200, 204]) #"Should return 200 OK or 204 No content for valid request")
    
    def test_valid_coordinates(self):
        response = self.client.get("/nearest-stores/?latitude=1.23&longitude=36.78")
        self.assertIn(response.status_code, [200, 204])
    
    def test_valid_product(self):
        response = self.client.get("/nearest-stores/?latitude=1.23&longitude=35.67&product=milk")
        self.assertIn(response.status_code, [200, 204])

# Create your tests here.
