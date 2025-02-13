# models.py
from django.db import models
from django.contrib.gis.db import models  # Import GIS models if using spatial data
from django.contrib.gis.geos import Point


# class USCity(models.Model):
#     sid = models.IntegerField()  # Assuming 'sid' is a unique identifier
#     # name = models.CharField(max_length=100)
#     # state = models.CharField(max_length=100)
#     # population = models.IntegerField()
#     # Add any other fields from the us_cities table

#     class Meta:
#         managed = False  # Django won't attempt to create or modify this table
#         db_table = 'us_cities'  # Explicitly reference the existing table name

#     def __str__(self):
#         return f"City with SID: {self.sid}"


# # models.py
# class RoadNetwork(models.Model):
#     osmid = models.IntegerField()  # Assuming 'sid' is a unique identifier
#     highway = models.IntegerField()  # If 'id' is another identifier, otherwise remove it
#     length = models.IntegerField()  # Assuming geom is a geometry field (change to MultiPolygonField, etc. if needed)

class RoadNetwork(models.Model):
    osmid = models.CharField(primary_key=True)  # Assuming osmid is an identifier (change if necessary)
    highway = models.CharField(max_length=100)  # Changed to CharField to accommodate both text and numbers
    length = models.FloatField()  # If length is a decimal, use FloatField, otherwise IntegerField
    geometry = models.LineStringField(srid=4326, null=True, blank=True)

    

    class Meta:
        managed = False  # Django won't attempt to create or modify this table
        db_table = 'kandra_road_network'  # Explicitly reference the existing table name
        indexes = [
            models.Index(fields=['geometry'], name='geometry_idx'),
        ]

    def __str__(self):
        return f"Road OSMID: {self.osmid}, Highway: {self.highway}, Length: {self.length}, Geom: {self.geometry}"

class NYCStreets(models.Model):
    id = models.IntegerField(primary_key=True)
    # geom = models.LineStringField()
    geom = models.MultiLineStringField()

    class Meta:
        managed = False
        db_table = 'nyc_streets'
        indexes = [
            models.Index(fields=['geom'], name='nyc_streets_geom_idx'),
        ]
    
    def __str__(self):
        return self.id

class NYCNeighborhoods(models.Model):
    id = models.IntegerField(primary_key=True)
    geom = models.MultiPolygonField()

    class Meta:
        managed = False
        db_table = 'nyc_neighborhoods'
        indexes = [
            models.Index(fields=['geom'], name='nyc_neighborhoods_geom_idx'),
        ]

    def __str__(self):
        return self.id

# create a POST api
class GeoJSONData(models.Model):
    name = models.CharField(max_length=255)
    geom = models.GeometryField()  # This will store the geometry in the PostGIS database
    description = models.TextField()

    def __str__(self):
        return self.name

# point address 
class Entity(models.Model):
    address = models.CharField(max_length=255)
    entity_type = models.CharField(max_length=50)
    location = models.PointField() 

    def __str__(self):
        return f"{self.entity_type} at {self.address}"


