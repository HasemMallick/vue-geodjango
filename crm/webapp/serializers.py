from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import RoadNetwork, NYCStreets, NYCNeighborhoods



class RoadNetworkSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = RoadNetwork
        geo_field = 'geometry'
        # fields = ('osmid', 'highway', 'length', 'geometry')
        fields = '__all__'

class NYCStreetsSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = NYCStreets
        geo_field = 'geom'
        fields = '__all__'

class NYCNeighborhoodsSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = NYCNeighborhoods
        geo_field = 'geom'
        fields = '__all__'