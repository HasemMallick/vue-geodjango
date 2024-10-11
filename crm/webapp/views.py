from django.shortcuts import render
from .models import  RoadNetwork, NYCStreets, NYCNeighborhoods
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import RoadNetworkSerializer, NYCStreetsSerializer, NYCNeighborhoodsSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser


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
