import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from math import sin, cos, sqrt, atan2, radians


def haversine(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


class FoodTruckView(APIView):
    def get(self, request):
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")
        rad = request.query_params.get("rad", 100)
        if not lat or not lon:
            return Response(
                "Please provide lat and lon", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            lat = float(lat)
            lon = float(lon)
            rad = float(rad)
            foodtruck_data = []
            with open(
                "/Users/nikhilagarwal/MyCodes/TheProvenClub/server/crux/foodtruckapp/updated_food_truck_data.csv",
                "r",
            ) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if (
                        row["Status"] == "APPROVED"
                        and row["Latitude"]
                        and row["Longitude"]
                        and row["Applicant"]
                    ):
                        truck_lat = float(row["Latitude"])
                        truck_lon = float(row["Longitude"])
                        distance = haversine(lat, lon, truck_lat, truck_lon)
                        if distance <= rad:
                            foodtruck_data.append(
                                {
                                    "id": row["locationid"],
                                    "name": row["Applicant"],
                                    "fooditems": row["FoodItems"],
                                    "address": row["Address"],
                                    "distance": round(distance, 2),
                                }
                            )
            return Response(foodtruck_data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                "Invalid lat, lon or rad", status=status.HTTP_400_BAD_REQUEST
            )
