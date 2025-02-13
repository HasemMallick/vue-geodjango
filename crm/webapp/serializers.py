from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import RoadNetwork, NYCStreets, NYCNeighborhoods, GeoJSONData, Entity
from django.contrib.gis.geos import fromstr
from rest_framework import serializers



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

# post API serializer
class GeoJSONDataSerializer(serializers.ModelSerializer):
    geom = serializers.CharField()  # GeoJSON data will be passed as a string

    class Meta:
        model = GeoJSONData
        fields = ['name', 'geom', 'description']

    def create(self, validated_data):
        # Convert the GeoJSON string into a geometry object
        geom_str = validated_data['geom']
        validated_data['geom'] = fromstr(geom_str)  # fromstr converts the string to geometry
        
        # Create and return the object
        return GeoJSONData.objects.create(**validated_data)

#  post point api
class EntitySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Entity
        fields = ('id', 'address', 'entity_type', 'location')
        geo_field = 'location'

# point get api (json response)
# class EntitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Entity
#         fields = ['id', 'address', 'entity_type', 'latitude', 'longitude', 'location']

# get point pai geojson response
class EntityGeoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Entity
        fields = ['id', 'address', 'entity_type', 'latitude', 'longitude', 'location']
        geo_field = 'location'  # This tells DRF to treat 'location' as the geometry field