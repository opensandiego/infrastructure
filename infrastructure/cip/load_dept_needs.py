import csv
from datetime import datetime

from infrastructure.cip.models import Project, DepartmentNeed

def parse_date(date_str, format):
    try:
        return datetime.strptime(date_str, format)
    except:
        return None

def parse_int(int_str):
    try:
        return int(int_str)
    except:
        return None

def load_buildings():
    building_projects_file = open('/home/ubuntu/infrastructure/data/dept-needs/csv/building_facilities.csv')
    building_reader = csv.reader(building_projects_file, delimiter=',', quotechar='"')
    headerline = building_reader.next()
    for project in building_reader:
        print project
        p = DepartmentNeed()
        p.department = "Buildings"
        p.rank = project[0]
        p.system_rank = project[1]
        p.fac_type = project[2]
        try:
            p.fci_percent = float(project[3].replace('%', ''))
        except ValueError:
            pass
        p.facility_name = project[4]
        p.system = project[5]
        p.maintenance = project[6]
        p.district = project[7]
        p.material = project[8]
        p.distress = project[9]
        p.correction = project[10]
        p.name = project[4] + ' - ' + project[10]
        p.est_cost = float(project[11].replace('$', '').replace(',',''))
        p.save()

def load_parks():
    parks_projects_file = open('/home/ubuntu/infrastructure/data/dept-needs/csv/parks_rec.csv')
    parks_reader = csv.reader(parks_projects_file, delimiter=',', quotechar='"')
    headerline = parks_reader.next()
    for project in parks_reader:
        print project
        p = DepartmentNeed()
        p.department = "Parks & Rec"
        try:
            parts = project[0].split(':')
            p.name = parts[0]
            p.address = parts[1]
            p.facility_name = parts[0]
        except:
            p.name = project[0]
            p.facility_name = project[0]
        p.district = project[1]
        p.cpa = project[2]
        p.description = project[3]
        p.deferred_maint = project[4]
        p.cdbg_elg = project[5]
        p.require_data = project[6]
        p.cost_range = project[7]
        p.req_date = parse_date(project[8], 'YYYY')
        p.req_source = project[9]
        p.remarks = project[10]
        p.save()

def load_water():
    water_projects_file = open('/home/ubuntu/infrastructure/data/dept-needs/csv/water.csv')
    water_reader = csv.reader(water_projects_file, delimiter=',', quotechar='"')
    headerline = water_reader.next()
    for project in water_reader:
        print project
        p = DepartmentNeed()
        p.department = "Water"
        p.rank = project[0]
        p.name = project[1]
        p.description = project[2]
        p.save()

def load_sewer():
    sewer_projects_file = open('/home/ubuntu/infrastructure/data/dept-needs/csv/sewer.csv')
    sewer_reader = csv.reader(sewer_projects_file, delimiter=',', quotechar='"')
    headerline = sewer_reader.next()
    for project in sewer_reader:
        print project
        p = DepartmentNeed()
        p.department = "Sewer"
        p.rank = project[0]
        p.name = project[1]
        p.description = project[2]
        p.facility_type = project[3]
        p.save()

def load_storm_drains():
    storm_drain_projects_file = open('/home/ubuntu/infrastructure/data/dept-needs/csv/storm_drains.csv')
    storm_drain_reader = csv.reader(storm_drain_projects_file, delimiter=',', quotechar='"')
    headerline = storm_drain_reader.next()
    for project in storm_drain_reader:
        print project
        p = DepartmentNeed()
        p.department = "Storm Drain"
        p.pipe_num = parse_int(project[0])
        p.upstream_struct = parse_int(project[1])
        p.downstream_struct = parse_int(project[2])
        p.recommendation = project[3]
        p.size = parse_int(project[4])
        p.material = project[5]
        p.map_length = project[6]
        p.location = project[7]
        p.name = project[3] + ' - Pipe Num ' + project[0]
        p.save()

def load_transportation():
    transportation_projects_file = open('/home/ubuntu/infrastructure/data/dept-needs/csv/transportation.csv')
    transportation_reader = csv.reader(transportation_projects_file, delimiter=',', quotechar='"')
    headerline = transportation_reader.next()
    for project in transportation_reader:
        print project
        p = DepartmentNeed()
        p.department = "Transportation"
        p.category = project[0]
        p.name = project[1]
        p.description = project[2]
        p.save()


load_buildings()
load_parks()
load_water() 
load_sewer()
load_storm_drains()
load_transportation()
