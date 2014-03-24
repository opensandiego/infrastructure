from django.core.management.base import BaseCommand, CommandError
from infrastructure.cip.models import Project
import requests
import json
from data.esri_geojson import *

class Command(BaseCommand):
    args = '<id>'

    def update_geo(self,project):
        """docstring for update_geo"""
        seq_nr = project.SP_SAPNO
        geojson = self.get_geojson_from_mapserver(seq_nr)
        if geojson:
            project.geometry = json.dumps(geojson)
        try:
            project.save()
        except Exception as inst:
            print type(inst)
            print inst.args
            print "Project not saved: %s" % project.SP_SPEC_NUM

    def get_geojson_from_mapserver(self, search_text):
        """docstring for get_geometry_from_mapserver"""
        response_object = self.get_data_from_mapserver(search_text)
        if response_object:
            return self.get_geojson_from_result(response_object)

    def get_data_from_mapserver(self, search_text):
        """docstring for get_data_from_mapserver"""
        results_obj = self.get_response_with_layer(search_text, "1")
        if results_obj:
            if not results_obj["results"]:
                results_obj = self.get_response_with_layer(search_text, "2")
                if not results_obj["results"]:
                    results_obj = self.get_response_with_layer(search_text, "3")

        return results_obj

    def get_response_with_layer(self,search_text, layer):
        """docstring for try_every_layer"""
        base_url = "http://maps.sandiego.gov/ArcGIS/rest/services/CIPTrackingPublic/MapServer/find?searchText={0}&contains=true&searchFields=CIP_ID&sr=&layers={1}&layerdefs=&returnGeometry=true&maxAllowableOffset=&f=JSON"
        url = base_url.format(search_text, layer)
        print url
        return self.get_json_from_map_server(url)

    def get_json_from_map_server(self, url):
        """docstring for getjson_from_map_server"""
        r = requests.get(url)
        print r.status_code
        if r.status_code is 200:
            return json.loads(r.text)

    def get_geojson_from_result(self,response_obj):
        """docstring for get_geometry_from_result"""
        if response_obj["results"]:
            result_obj = response_obj["results"][0]
            geojson = GeoJSONFeature()
            geojson.transform_from_esri(result_obj)
            return geojson.to_json()


    def handle(self,*args,**options):
        if args:
            project_id = args[0]
            if project_id:
                project = Project.objects.get(pk=int(project_id))
                self.update_geo(project)
        else:
            projects = Project.objects.all()
            for project in projects:
                self.update_geo(project)
