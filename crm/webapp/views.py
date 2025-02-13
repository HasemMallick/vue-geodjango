from django.shortcuts import render
from .models import  RoadNetwork, NYCStreets, NYCNeighborhoods, Entity
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import RoadNetworkSerializer, NYCStreetsSerializer, NYCNeighborhoodsSerializer, GeoJSONDataSerializer, EntitySerializer, EntityGeoSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.gis.geos import Point

# imports from post api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


# Create your views here.

def home(request):
    # return HttpResponse('Hello World')

    return render(request, 'webapp/index.html')

# def us_cities_list(request):
#     cities = USCity.objects.all()  # Fetch all data from the us_cities table
#     for i in cities:
#         print(i)
#     print(cities)
#     return render(request, 'webapp/us_cities_list.html', {'cities': cities})

def kandra_road_network(request):
    road_network = RoadNetwork.objects.all()
    return render(request, 'webapp/kandra_road_network.html', {'road_network': road_network})


def visualize_road_network(request):
    roads = RoadNetwork.objects.all()
    road_data = []

    # Extract the coordinates from the geometry field (geom)
    for road in roads:
        road_data.append({
            'osmid': road.osmid,
            'highway': road.highway,
            'coordinates': list(road.geom.coords),  # Extract coordinates from LineString
        })

    return render(request, 'visualize_road_network.html', {'road_data': road_data})



class RoadNetworkViewSet(viewsets.ReadOnlyModelViewSet):  # Use ReadOnlyModelViewSet if you only want to fetch data
    queryset = RoadNetwork.objects.all()
    serializer_class = RoadNetworkSerializer

# class NYCStreetsViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = NYCStreets.objects.all()
#     serializer_class = NYCStreetsSerializer

@csrf_exempt
def nyc_streets(request):
    if request.method == 'GET':
        try:
            snippets = NYCStreets.objects.all()[:100]
            serializer = NYCStreetsSerializer(snippets, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            return JsonResponse({'error' : str(e)})

@csrf_exempt
def nyc_neighborhoods(request):
    if request.method == 'GET':
        try:
            neighborhoods = NYCNeighborhoods.objects.all()[:100]
            serializer = NYCNeighborhoodsSerializer(neighborhoods, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            return JsonResponse({'error' : str(e)})

@csrf_exempt
def centerslocationapi(request):
    if request.method == 'GET':
        try:
            snippets = RoadNetwork.objects.all()
            # print("This is snippets:", snippets)  # Debugging output
            serializer = RoadNetworkSerializer(snippets, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RoadNetworkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def centersapi(request):
    if request.method == 'GET':
        snippets = RoadNetwork.objects.all()
        serializer = RoadNetworkSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RoadNetworkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class EntityList(APIView):
    def get(self, request, format=None):
        # Get all the entities from the database
        entities = Entity.objects.all()
        # Serialize the data using the GeoJSON serializer
        serializer = EntityGeoSerializer(entities, many=True)
        # Return the response with GeoJSON renderer
        return Response(serializer.data, content_type='application/geo+json', status=status.HTTP_200_OK)       


# post api
class GeoJSONUploadView(APIView):
    def post(self, request, *args, **kwargs):
        # Deserialize the data
        serializer = GeoJSONDataSerializer(data=request.data)
        if serializer.is_valid():
            # Save the validated data to the database
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# point post api
@api_view(['POST'])
def create_entity(request):
    if request.method == 'POST':
        # Extract the data from the request
        address = request.data.get('address')
        entity_type = request.data.get('entityType')
        lat = request.data.get('lat')
        lon = request.data.get('long')

        # Create a Point object using the provided lat and long
        location = Point(lon, lat)

        # Create the entity and save it
        entity = Entity.objects.create(
            address=address,
            entity_type=entity_type,
            location=location
        )

        # Serialize and return the response
        serializer = EntitySerializer(entity)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# # get point api
# class EntityList(APIView):
#     def get(self, request, format=None):
#         # Get all the entities from the database
#         entities = Entity.objects.all()
#         # Serialize the data
#         serializer = EntitySerializer(entities, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)