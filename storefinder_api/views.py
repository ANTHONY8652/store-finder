from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, filters
from .permissions import IsAdminOrReadOnly
from .mock_data import stores
from rest_framework.decorators import action
import math 
from math import  radians, cos, sin, asin, sqrt
from .serializers import StoreSerializer
from .models import Store
import logging


logger = logging.getLogger(__name__)


"""
class NearestStoresView(APIView):
    #A simple endpoint that is supposed to accept latitude and longitude query parameters and returns mock store data

    def get(self, request):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if not latitude or not longitude:
            return Response(
                {"error": "Please provide 'latitude' and 'longitude' query parameters in order to easily identify stores near you"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        #Mock data simulating nearby stores

        stores = [
            {"name": "Naivas Mountain View","Address": "Mountain View Waiyaki Way", "latitude": latitude, "lon": longitude, "source": "MockData"},
            {"name": "Quickmart Kangemi", "Address": "Kangemi Market Waiyaki Way", "lat": latitude, "lon": longitude, "source": "MockData"},
        ]
        
        return Response ({"stores": stores})
"""


def calculate_distance(latitude1, longitude1, latitude2, longitude2):
    #Haversine Formula
    R = 6371
    d_latitude = math.radians(latitude2 - latitude1)
    d_longitude = math.radians(longitude2 - longitude1)

    a = math.sin(d_latitude/2)**2 + math.cos(math.radians(latitude1)) * math.cos(math.radians(latitude2)) * math.sin(d_longitude/2) **2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

class NearestStoresView(APIView):
    permission_classes =[permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        logger.info(f"User requested coordinates: latitude={latitude}, longitude={longitude}")
        try:
            user_latitude = float(request.GET.get("latitude", "0").replace("'", ""))
            user_longitude = float(request.GET.get("longitude", "0").replace("'", ""))
            product = request.GET.get("product").lower()
        
        except(ValueError, TypeError):
            return JsonResponse({"error": "Invalid or missing co-ordinates"}, status=status.HTTP_400_BAD_REQUEST)

        if not (-90 <= user_latitude <=90 and -180 <= user_longitude <= 180):
            return JsonResponse({"error": "Co-ordinates out of range"}, status=status.HTTP_400_BAD_REQUEST)

        results = []

        for store in stores:
            for item in store["products"]:
                if item["name"].lower() == product:
                    distance = calculate_distance(user_latitude, user_longitude, store["latitude"], store["longitude"])

                    results.append({
                        "store": store["name"],
                        "price": item["price"],
                        "distance_km": round(distance, 2),
                    })

        sorted_results = sorted(results, key=lambda x: (x["price"], x["distance_km"]))

        return Response(sorted_results)

class ProductSearchView(APIView):
    def get(self, request):
        ##DUmmy data for the time being

        data = [
            {"store": "Naivas Mountain View Mall", "product": "Milk", "price": 120, "distance_km": 0.6},
            {"store": "Quickmart Kangemi", "product": "Milk", "price": 115, "distance_km": 1.2},
        ]

        return Response(data)

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Store.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        try:
            user_latitude = float(request.query_params.get("latitude"))
            user_longitude = float(request.query_params.get("longitude"))
        
        except (TypeError, ValueError):
            return Response({"error": "Latitude and longitude are required as valid floats"}, status=status.HTTP_400_BAD_REQUEST)
        
        def haversine(latitude1, longitude1, latitude2, longitude2):
            #Convert decimal degrees to radians
            latitude1, longitude1, latitude2, longitude2 = map(radians, [latitude1, longitude1, latitude2, longitude2])
            dlongitude = longitude2 - longitude1
            dlatitude = latitude2 - latitude1
            a = sin(dlatitude / 2) ** 2 + cos(latitude1) * cos(latitude2) * sin(dlongitude / 2) ** 2
            c = 2 * asin(sqrt(a))
            r = 6371 #Radius of the earth in Kolometas
            return r * c
        
        stores_with_distance = []
        for store in self.get_queryset():
            distance = haversine(user_latitude, user_longitude, store.latitude, store.longitude)
            stores_with_distance.append((distance, store))

        stores_with_distance.sort(key=lambda x: x[0])
        sorted_stores = [s[1] for s in stores_with_distance]
        serializer = self.get_serializer(sorted_stores, many=True)

        return Response(serializer.data)

# Create your views here.
