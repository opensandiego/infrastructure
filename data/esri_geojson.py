class GeoJSONFeature():
    type = "Feature"
    geometry = {"type":"","coordinates": []}
    properties = {}
    crs = ""

    def to_json(self):
        """docstring for to_json"""
        return { "type": self.type, "geometry": self.geometry, "properties": self.properties, "crs": self.crs}
    def transform_from_esri(self,esri_json):
        """docstring for transform"""
        geometry_method = "geojson_%s" % esri_json["geometryType"]
        self.geometry["type"] = getattr(self,geometry_method)()
        coordinates_method = "esri_coordinates_%s" % self.geometry["type"]
        self.geometry["coordinates"] = getattr(self,coordinates_method)(esri_json["geometry"])
        if esri_json["geometry"].has_key("spatialReference"):
            self.crs = { "type": "name", "properties": { "name": "EPSG:{0}".format(esri_json["geometry"]["spatialReference"]["wkid"]) } }

    def geojson_esriGeometryPoint(self):
        """docstring for fname"""
        return "Point"
    def geojson_esriGeometryMultiPoint(self):
        """docstring for fname"""
        return "MulitPoint"
    def geojson_esriGeometryPolyline(self):
        """docstring for fname"""
        return "LineString"
    def geojson_esriGeometryPolygon(self):
        """docstring for fname"""
        return "Polygon"

    def esri_coordinates_Point(self, geometry):
        """docstring for esri_coordinates_Point"""
        return [ geometry["x"], geometry["y"] ]

    def esri_coordinates_MultiPoint(self, geometry):
        """docstring for esri-coordinates_MultiPoint"""
        return geometry["points"]

    def esri_coordinates_LineString(self, geom):
        """docstring for esri_coordinates_LineString"""
        if len(geom["paths"]) > 1:
            self.geometry["type"] = "MultiLineString"
            return geom["paths"][0]
        else:
            return geom["paths"][0]

    def esri_coordinates_Polygon(self, geometry):
        """docstring for esri_coordinates_Polygon"""
        return geometry["rings"]

