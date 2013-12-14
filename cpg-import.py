import os, sys, traceback
import csv
import xlrd
import time
from geopy import geocoders

skip_list = ['.DS_Store']

project_types = {
    'building_community':'Community support facilities and structures',
    'building_fire':'Fire facilities and structures',
    'building_library':'Libraries',
    'building_sewer':'Sewer facilities and structures (e.g., treatment plants - and pump stations)',
    'build_operations':'Operations facilities and structures (e.g., maintenance shops and offices)',
    'build_other':'Other City facilities and structures',
    'build_parks':'Park & Recreation facilities and structures',
    'build_police':'Police facilities and structures',
    'build_water':'Water facilities and structures (e.g., treatment plants, pump stations, reservoirs, dams, standpipes)',
    'drain_pipe':'Pipes',
    'drain_channel':'Channels',
    'drain_bmp':'Best Management Practices (BMPs)',
    'drain_pump_station':'Pump Stations',
    'flood_control':'Flood Control',
    'golf':'Golf Course Facilities',
    'landfill':'Landfill Facilities',
    'parks':'Park Facilities',
    'water_reclaimed':'Reclaimed Water Facilities',
    'transport_bicycle':'Bicycle Facilities (all classifications).',
    'transport_bridge':'Bridge Replacement, Retrofit, and Rehabilitation.',
    'transport_erosion':'Erosion control, slope stabilization, and retaining walls supporting transportation facilities.',
    'transport_guardrails':'Guardrails, Barrier Rails, and other structural safety enhancements.',
    'transport_roads':'New Roads, Roadway Widening, and Roadway Reconfigurations.',
    'transport_street_enhance':'Street Enhancements including medians and streetscape.',
    'transport_signals':'New Traffic Signals.',
    'transport_pedestrian_access':'Pedestrian Accessibility Improvements including curb ramps.',
    'transport_pedestrian':'Pedestrian Facilities including sidewalks but not curb ramps.',
    'transport_lighting':'Street Lighting including mid-block and intersection safety locations.',
    'transport_traffic_calming':'Traffic Calming, Flashing Beacons, and other speed abatement work.',
    'transport_signal_connection':'Traffic Signal Interconnections and other signal coordination work.',
    'transport_signal_mods':'Traffic Signal Upgrades and Modifications.'
}



def lookup_type(type_name):
    for type_key, type_value in project_types.iteritems():
        if type_name == type_value:
            return type_key
    return type_name

us = geocoders.GeocoderDotUS()
g = geocoders.GoogleV3()

csvfile = open('projects.csv', 'wb')
project_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
project_writer.writerow(["cpg", "app_date", "cd", "neighborhood", "title", "cip_num", "gen_location", "lat", "lng", "description", "purpose", "urgency", "name", "address", "email", "phone", "review_date", "scoring", "vote", "building_community", "building_fire", "building_library", "building_sewer", "build_operations", "build_other", "build_parks", "build_police", "build_water", "drain_pipe", "drain_channel", "drain_bmp", "drain_pump_station", "flood_control", "golf", "landfill", "parks", "water_reclaimed", "transport_bicycle", "transport_bridge", "transport_erosion", "transport_guardrails", "transport_roads", "transport_street_enhance", "transport_signals", "transport_pedestrian_access", "transport_pedestrian", "transport_lighting", "transport_traffic_calming", "transport_signal_connection", "transport_signal_mods"])


for file in os.listdir('./xls'):
    #print file
    if file not in skip_list or 'NoRecommendation' in file:
        wb = xlrd.open_workbook('xls/' + file)
        for sheet in wb.sheet_names():
            sh = wb.sheet_by_name(sheet)
            try:
                cpg = app_date = cd = neighborhood = title = cip_num = gen_location = description = purpose = urgency = name = building_community = building_fire = building_library = building_sewer = build_operations = build_other = build_parks = build_police = build_water = drain_pipe = drain_channel = drain_bmp = drain_pump_station = flood_control = golf = landfill = parks = water_reclaimed = transport_bicycle = transport_bridge = transport_erosion = transport_guardrails = transport_roads = transport_street_enhance = transport_signals = transport_pedestrian_access = transport_pedestrian = transport_lighting = transport_traffic_calming = transport_signal_connection = transport_signal_mods = lat = lng = address = email = phone = ""
                for rownum in range(sh.nrows):
                    values = sh.row_values(rownum)
                    if unicode(values[0]).strip()== 'Community Planning Group:':
                        cpg = values[4].strip().rstrip("\r\n").encode("utf8")
                    if unicode(values[0]).strip()== 'Application Date:':
                        raw_date = values[4]
                        #date = time.strptime(raw_date, "%d-%b-%y")
                        #app_date = time.strftime("%Y-%m-%d",date)
                        app_date = raw_date
                    if unicode(values[0]).strip()== 'Council District (1 - 9):': #'Council District (1-9):':
                        cd = values[4]
                    if unicode(values[0]).strip()== 'Neighborhood:':
                        neighborhood = values[4].strip().rstrip("\r\n").encode("utf8")
                    if unicode(values[0]).strip()== 'Proposed Project Title:':
                        title = values[4].strip().rstrip("\r\n").encode("utf8")
                    if unicode(values[0]).strip()== 'CIP No. (if any, aka WBS#)':
                        cip_num = values[4].strip().rstrip("\r\n").encode("utf8")
                    if unicode(values[0]).strip() == 'TYPE OF PROJECT (check at least one)': #'TYPE OF PROJECT (please check one)':
                        type_codes = []
                        for type_row in range(rownum+3, rownum+39):
                            if unicode(sh.row_values(type_row)[1]).strip() != "":
                                #type_codes.append(lookup_type(sh.row_values(type_row)[3]))
                                col = lookup_type(sh.row_values(type_row)[3])
                                vars()[col] = "1"
                        #types = "|".join(type_codes)
                    if unicode(values[0]).strip()== 'Project Address/Location:': #General Location:':
                        gen_location = values[4].strip().rstrip("\r\n").encode("utf8")
                    if unicode(values[0]).strip()== 'GPS Coordinates (if known)':
                        if sh.row_values(rownum+1)[4] != "" and isinstance(sh.row_values(rownum+1)[4], float):
                            lat = sh.row_values(rownum+1)[4]
                        if sh.row_values(rownum+2)[4] != "" and isinstance(sh.row_values(rownum+2)[4], float):
                            lng = sh.row_values(rownum+2)[4]
                    if unicode(values[0]).strip()== 'Project Description?':
                        desc0 = sh.row_values(rownum+1)[4].strip().rstrip("\r\n").encode("utf8")
                        desc2 = sh.row_values(rownum+2)[4].strip().rstrip("\r\n").encode("utf8")
                        desc3 = sh.row_values(rownum+3)[4].strip().rstrip("\r\n").encode("utf8")
                        description = desc0 + desc2 + desc3
                    if unicode(values[0]).strip()== 'Project Purpose/Need?':
                        purp0 = sh.row_values(rownum+1)[4].strip().rstrip("\r\n").encode("utf8")
                        purp2 = sh.row_values(rownum+2)[4].strip().rstrip("\r\n").encode("utf8")
                        purp3 = sh.row_values(rownum+3)[4].strip().rstrip("\r\n").encode("utf8")
                        purpose = purp0 + purp2 + purp3
                    if unicode(values[0]).strip()== 'Project Urgency?':
                        urgency = sh.row_values(rownum+1)[4].strip().rstrip("\r\n").encode("utf8")
                    if unicode(values[0]).strip()== 'CPG CONTACT/APPLICANT' or unicode(values[0]).strip()== 'CPG CONTACT': #'APPLICANT INFORMATION':
                        name = sh.row_values(rownum+1)[4].strip().rstrip("\r\n").encode("utf8")
                        address = sh.row_values(rownum+2)[4].strip().rstrip("\r\n").encode("utf8")
                        email = sh.row_values(rownum+3)[4].strip().rstrip("\r\n").encode("utf8")
                        phone = sh.row_values(rownum+4)[4].strip().rstrip("\r\n").encode("utf8")
                    if unicode(values[0]).strip()== 'COMMUNITY PLANNING GROUP (CPG) FINDINGS' or unicode(values[0]).strip()== 'COMMUNITY PLANNING GROUP ACTION':
                        raw_date = sh.row_values(rownum+1)[4]
                        #date = time.strptime(raw_date, "%d-%b-%y")
                        #review_date= time.strftime("%Y-%m-%d",date)
                        review_date = raw_date
                        try:
                            scoring = sh.row_values(rownum+2)[4]
                            vote = sh.row_values(rownum+3)[4].strip().rstrip("\r\n").encode("utf8")
                        except:
                            pass
                if cpg != "":
                    if not lng and not lat:
                        lat = 32.7043292
                        lng = -017.1472551
                        try:
                            place_string = gen_location + " San Diego, CA"
                            place, (lat, lng) = list(g.geocode(place_string, exactly_one=False))[0]
                            print place_string, place, lat, lng
                        except:
                            exc_type, exc_value, exc_traceback = sys.exc_info()
                            print exc_type, exc_value
                            traceback.print_tb(exc_traceback, limit=0, file=sys.stdout)
                    project_writer.writerow([cpg, app_date, cd, neighborhood, title, cip_num, gen_location, lat, lng, description, purpose, urgency, name, address, email, phone, review_date, scoring, vote,building_community,building_fire,building_library,building_sewer,build_operations,build_other,build_parks,build_police,build_water,drain_pipe,drain_channel,drain_bmp,drain_pump_station,flood_control,golf,landfill,parks,water_reclaimed,transport_bicycle,transport_bridge,transport_erosion,transport_guardrails,transport_roads,transport_street_enhance,transport_signals,transport_pedestrian_access,transport_pedestrian,transport_lighting,transport_traffic_calming,transport_signal_connection,transport_signal_mods])
            except:
                #print sh.row_values(rownum+2)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print exc_type, exc_value
                traceback.print_tb(exc_traceback, limit=0, file=sys.stdout)
csvfile.close()
