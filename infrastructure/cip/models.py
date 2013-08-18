from django.db import models
from django.db.models.query import QuerySet
import datetime
from django.contrib.humanize.templatetags.humanize import intcomma

class ProjectCosts(object):
    def __init__(self):
        """docstring for __init__"""
        self.cost = [
                [0,300000],
                [300000,500000],
                [500000,1000000],
                [1000000,3000000],
                [3000000,5000000],
                [5000000,8000000],
                [8000000,11000000],
                [11000000,15000000],
                [15000000,0]
                ]
    def get_string(self,value):
        """docstring for get_string"""
        if isinstance(value, list):
            if value[0] == 0:
                return '< {0}'.format(intcomma(value[1]))
            elif value[1] == 0:
                return '> {0}'.format(intcomma(value[0]))
            else:
                return '{0} - {1}'.format(intcomma(value[0]), intcomma(value[1]))
        else:
            return ''
    def get_query(self,value):
        """docstring for get_query"""
        if isinstance(value, list):
            if value[0] == 0:
                return self.filter(SP_TOTAL_PROJECT_COST__lt=value[1])
            elif value[1] == 0:
                return self.filter(SP_TOTAL_PROJECT_COST__gt=value[0])
            else:
                return self.filter(SP_TOTAL_PROJECT_COST__gt=value[0], SP_TOTAL_PROJECT_COST__lt=value[1])

    def get_value(self,value):
        """docstring for get_value"""
        print value
        return self.cost[value]
    def get_touples(self):
        """docstring for get_touples"""
        return [(i,self.get_string(self.cost[i])) for i in range(len(self.cost))]


class ProjectManagerMixin(object):
    def current(self):
        """docstring for current"""
        return self.filter(SP_CONSTR_FINISH_DT__gt=datetime.date.today(), SP_PRELIM_ENGR_START_DT__lt=datetime.date.today())
    def future(self):
        """docstring for future"""
        return self.filter(SP_AWARD_START_DT__gt=datetime.date.today())
    def by_phase(self,phase):
        """docstring for by_phase"""
        return self.filter(SP_PROJECT_PHASE__istartswith=phase)
    def by_asset_group(self,asset_group):
        """docstring for by_asset_group"""
        return self.filter(SP_ASSET_TYPE_GROUP__istartswith=asset_group)
    def by_asset_choice(self,asset_choice):
        """docstring for by_asset_group"""
        return self.filter(SP_ASSET_TYPE_CD__istartswith=asset_choice)
    def by_delivery_method(self,delivery_method):
        """docstring for by_asset_group"""
        return self.filter(SP_DELIVERY_METHOD_CD__istartswith=delivery_method)
    def by_client_departement(self,client_departements):
        """docstring for by_asset_group"""
        return self.filter(SP_CLIENT2__istartswith=client_departements)
    def by_project_cost(self,project_cost):
        """docstring for by_project_cost"""
        return self.get_query(project_cost)

class ProjectQuerySet(QuerySet,ProjectManagerMixin,ProjectCosts):
    pass

class ProjectManager(models.Manager,ProjectManagerMixin):
    def phase_count(self, phase):
        """docstring for phase_count"""
        return self.filter(SP_PROJECT_PHASE__istartswith=phase).count()
    def get_query_set(self):
        """docstring for get_query_set"""
        return ProjectQuerySet(self.model)

PHASE_URLS = (
        ('planning' , 'Planning'),
        ('design' , 'Design'),
        ('bid' , 'Bid and Award'),
        ('construction' , 'Construction'),
        ('post-construction' , 'Post Construction'),
        ('completed' , 'Complete')
       ) 
PHASE_ORDERS = {
        'planning' : 'SP_PRELIM_ENGR_START_DT',
        'design' : 'SP_DESIGN_INITIATION_START_DT',
        'bid' : 'SP_BID_START_DT',
        'construction' : 'SP_CONSTRUCTION_START_DT',
        'post-construction' : 'SP_CONSTR_FINISH_DT',
        'completed' : 'SP_BO_BU_DT'
        }
ASSET_TYPE_URLS = (
   ( "airports", "Airports"),
   ( "buildings", "Buildings"),
   ( "storm-water-drainage", "Storm Water Drainage"),
   ( "parks", "Parks"),
   ( "transportation", "Transportation"),
   ( "sewer", "Sewer"),
   ( "water", "Water"))

ORDER = (
    ('SP_PRELIM_ENGR_START_DT', 'Planning Start ASC'),
    ('-SP_PRELIM_ENGR_START_DT', 'Planning Start DESC'),
    ('SP_CONSTR_FINISH_DT','construction finish ASC'),
    ('-SP_CONSTR_FINISH_DT','construction finish DESC'),
    ('SP_TOTAL_PROJECT_COST','construction cost ASC'),
    ('-SP_TOTAL_PROJECT_COST','construction cost DESC'))

ASSET_TYPE_GROUPS = (
   ( "A", "Airports"),
   ( "B", "Buildings"),
   ( "C", "Storm Water Drainage"),
   ( "G", "Parks"),
   ( "I", "Transportation"),
   ( "J", "Sewer"),
   ( "K", "Water"))

ASSET_TYPE_CHOICES = (
    ("BA","Bldg - Pub Safety - Police Facility/Structure"),
    ("BB","Bldg - Pub Safety - Lifeguard Station"),
    ("BC","Bldg - Pub Safety - Fire Facility/Structure"),
    ("BD","Bldg - Library"),
    ("BE","Bldg - Parks - Recreation/Pool Center"),
    ("BF","Bldg - Parks - Recreational Sports Facility"),
    ("BG","Bldg - Stadium Facility"),
    ("BH","Bldg - Community Center"),
    ("BI","Bldg - Water - Treatment Plant"),
    ("BJ","Bldg - Water - Pump Station"),
    ("BK","Bldg - Water - Reservoir/Dam"),
    ("BL","Bldg - Water - Standpipe"),
    ("BO","Bldg - Sewer - Treatment Plant"),
    ("BP","Bldg - Sewer - Pump Station"),
    ("BS","Bldg - Operations Facility/Structure"),
    ("BT","Bldg - Other City Facility/Structure"),
    ("CA","Drainage - Storm Drain Pipe"),
    ("CB","Drainage - Channel"),
    ("CC","Drainage - Best Mgt Practices BMPs"),
    ("CD","Drainage - Pump Station"),
    ("DA","Flood Control System"),
    ("EA","Golf Course"),
    ("GA","Parks - Community"),
    ("GB","Parks - Neighborhood"),
    ("GC","Parks - Mini Park"),
    ("GE","Parks - Resource Based"),
    ("GF","Parks - Miscellaneous Park"),
    ("GG","Parks - Open Space"),
    ("HC","Reclaimed Water System - Pipeline"),
    ("IA","Trans - Bicycle Facility All Class."),
    ("IB","Trans - Bridge - Vehicular"),
    ("IC","Trans - Bridge - Pedestrian"),
    ("ID","Trans - Roadway"),
    ("IE","Trans - Roadway - GRails/BRails/Safety"),
    ("IF","Trans - Roadway - Erosion/Slope/Ret Wall"),
    ("IG","Trans - Roadway - Enhance/Scape/Median"),
    ("IH","Trans - Roadway - Street Lighting"),
    ("II","Trans - Ped Fac - Accessibility Improvement"),
    ("IJ","Trans - Ped Fac - Curb Ramp"),
    ("IK","Trans - Ped Fac - Sidewalk"),
    ("IL","Trans - Signals - Traffic Signal"),
    ("IM","Trans - Signals - Calming/Speed Abatement"),
    ("IO","Trans - Roads/Widening/Reconfiguration"),
    ("JA","Wastewater - Collection System - Main"),
    ("JB","Wastewater - Collection System - Trunk Sewer"),
    ("JD","Wastewater - Collection System - Laterals"),
    ("KA","Water - Distribution System - Transmission"),
    ("KB","Water - Distribution System - Distribution"),
    ("KC","Water - Reservoir"))

DELIVERY_METHODS = (
    ("AB","Agency Build (CDBG/Caltrans)"),
    ("CF","City Forces"),
    ("CMAR","Construction Manager at Risk"),
    ("DB","Design Build"),
    ("DBB","Design Bid Build"),
    ("DVB","Developer Build"),
    ("EP","Emergency Project (Std, as-needed)"),
    ("JOC","Job Order Contract"),
    ("JU","Joint Use"),
    ("MACC","Multiple Award Construction Contract"),
    ("MC","Minor Contract"),
    ("SS","Sole Source"),
    ("ST","Study"))

PROJECT_PHASES = (
    ("P", "Planning"),
    ("D", "Design"),
    ("B", "Bid and Award"),
    ("N", "Construction"),
    ("O", "Post Construction"),
    ("C", "Complete"))

CLIENT_DEPARTMENTS = (
    ("Airports","Airports Department"),
    ("DS","Disability Services"),
    ("DSD","Development Services Department"),
    ("EDD","Economic Development Division"),
    ("Fire","Fire-Rescue Department (Lifeguard)"),
    ("GSF","General Services Facilities"),
    ("Library","Library Department"),
    ("P&R","Park & Recreation Department"),
    ("PPD","Pollution Prevention Division"),
    ("READ","Real Estate Assets Department"),
    ("SWD","Storm Water Department"),
    ("Sewer","Public Utilities Department - Wastewater"),
    ("Street","Street Division"),
    ("TEO","Transportation Engineering & Operations Division"),
    ("TSWD","Transportation and Storm Water Department"),
    ("Water","Public Utilities Department - Water"))

RESPONSIBLE_DIVISIONS = (
    "AEP/PB","Architectural Engineering & Parks Division - Public Buildings",
    "AEP/PF","Architectural Engineering & Parks Division - Process Facilities",
    "AEP/PK","Architectural Engineering & Parks Division - Parks",
    "AEP/TF","Architectural Engineering & Parks Division - Treatment Facilities",
    "GSD/FD","General Services Facilities Division",
    "PITS/EP","PITS - Environmental & Permitting Support",
    "PITS/GR","PITS - GRC",
    "PITS/PE","PITS - Preliminary Engineering",
    "ROW/BG","Right-of-Way Design Division - Bridges",
    "ROW/DN","Right-of-Way Design Division - Drainage",
    "ROW/SL","Right-of-Way Design Division - Signal & Streetlight Design",
    "ROW/TS","Right-of-Way Design Division - Transportation/Streets",
    "ROW/WS","Right-of-Way Design Division - Water & Wastewater Pipelines",
    "TSWD/SD","Transportation & Storm Water Department - Street Division")

FUND_SOURCE = (
    "C1","Community Development Block Grant (CDBG)",
    "C3","General Fund Revenues",
    "C4","California's Local Streets & Roads Improvement",
    "C5","Enterprise Fund - Metropolitan Wastewater",
    "C6","San Diego Transportation Improvement Program (TransNet)",
    "C7","Enterprise Fund - Water",
    "C8","Facilities Benefit Assessment",
    "C9","Cap Out-Lay",
    "C10","CDBG/Cap-Outlay (ADA)",
    "C11","Developer Impact Fees (Deferred Maintenance)",
    "C12","Redevelopment Agency Fund",
    "C13","Southeastern Economic Development Corp (SEDC)",
    "C14","Deferred Maintenance Bond",
    "C15","Maintenance Assessment District (MAD) Funds",
    "C15","Grants & Reimbursements",
    "C16","Enterprise Fund - Airports",
    "C16","Airports Annual Allocation",
    "C18","Enterprise fund - Golf",
    "F2","Federal Aviation Administration",
    "O1","Other Funding Source",
    "O2","Developer Fair Share",
    "O3","Sea World Mitigation Fund",
    "O4","Underground Utility Fund",
    "S1","",
    "S2","Transportation Bond - State (Prop 1B)",
    "S4","Funding for Public Water Systems (DPH)",
    "S5","Assembly Bill 2928",
    "S6","Transportation Development Act (TDA)",
    "S8","Bond",
    "S10","State Revolving Funds (SRF)")

PROJECT_INFO_DESC = (
    "50", "Code 50",
    "OH", "On Hold",
    "BP", "Bubble Project",
    "PM", "Not Part of Dept Performance Measure 2010",
    "FF", "Fully Funded",
    "PF", "Partially Funded")


PROJECT_INFO_DESC_2 = (
    "ND", "Not Applicable - No Design",
    "CD", "Consultant Design",
    "DB", "Design Build - Consultant Design",
    "IH", "In-House Design")


PROJECT_KIND = (
    "NA", "Not Applicable"
    "1B", "Prop 1B"
    "AD", "Americans with Disabilities Act (ADA) Upgrades"
    "D2", "Deferred Capital (2)"
    "EM", "Environmental Mitigation & Monitoring"
    "OT", "Other"
    "PF", "Park Facilities"
    "OR", "On the Radar"
    "EP", "Emergency Project"
    "DC", "Deferred Capital"
    "09", "Deferred Capital (FY09)"
    "OF", "Other City Facilities"
    "RD", "Redevelopment Agency (RA)"
    "LF", "Lifeguard Facilities"
    "AR", "American Recovery & Reinvestment Act - ARRA (Stimulus Package)",
    "LR", "Low Impact Developments")

class Person(models.Model):
    full_name = models.CharField(max_length=100)


class Contractor(models.Model):
    full_name = models.CharField(max_length=100)


class Project(models.Model):
    SP_SEQ_NUM = models.IntegerField()
    SP_DATA_DATE = models.DateField()
    SP_SAPNO = models.CharField(max_length=8, null=True, blank=True)
    SP_TYPE_CD = models.CharField(max_length=1, null=True, blank=True)
    SP_PROJECT_NM = models.CharField(max_length=512, null=True, blank=True)
    SP_SENIOR_NM = models.CharField(max_length=100, null=True, blank=True)
    SP_ASSET_TYPE_GROUP = models.CharField(max_length=100, null=True, blank=True)
    SP_ASSET_TYPE_CD = models.CharField(max_length=2, null=True, blank=True)
    SP_ASSET_TYPE_DESC = models.CharField(max_length=100, null=True, blank=True)
    SP_SAP_RUN_DT = models.DateField(null=True, blank=True) 
    SP_PRELIM_ENGR_FINISH_DT= models.DateField(null=True, blank=True) 
    SP_DESIGN_FINISH_DT = models.DateField(null=True, blank=True)
    SP_NTP_DT = models.DateField(null=True, blank=True)
    SP_NOC_DT= models.DateField(null=True, blank=True)
    SP_PROJECT_CLOSEOUT_DT= models.DateField(null=True, blank=True)
    SP_DESIGN_INITIATION_START_DT= models.DateField(null=True, blank=True)
    SP_CONSTRUCTION_START_DT= models.DateField(null=True, blank=True)
    SP_BO_BU_DT= models.DateField(null=True, blank=True)
    SP_TOTAL_CONSTRUCTION_COST = models.IntegerField(null=True, blank=True)
    SP_TOTAL_PROJECT_COST = models.IntegerField(null=True, blank=True)
    SP_PLANNING_TO_NOC_DAYS= models.IntegerField(null=True, blank=True)
    SP_VAR_BL_DESIGN_FINISH_DAYS= models.IntegerField(null=True, blank=True)
    SP_VAR_DESIGN_BL_ES065_DAYS= models.IntegerField(null=True, blank=True)
    SP_VAR_BL_NOC_DAYS= models.IntegerField(null=True, blank=True)
    SP_VAR_NOC_BL_ES130_DAYS= models.IntegerField(null=True, blank=True)
    SP_DELIVERY_METHOD_CD = models.CharField(max_length=12, null=True, blank=True)
    SP_DELIVERY_METHOD_DESC = models.CharField(max_length=100, null=True, blank=True)
    SP_FIELD_SENIOR_NM = models.CharField(max_length=100, null=True, blank=True)
    SP_PROJECT_PHASE = models.CharField(max_length=100, null=True, blank=True)
    SP_PROJECT_STATUS_CD = models.CharField(max_length=2)
    SP_UPDATE_DT = models.DateField(null=True, blank=True)
    SP_PROJECT_DESC = models.TextField(null=True, blank=True)
    SP_CLIENT1 = models.CharField(max_length=100, null=True, blank=True)
    SP_CLIENT2 = models.CharField(max_length=100, null=True, blank=True)
    SP_RESP_DIV_SECTION = models.CharField(max_length=8, null=True, blank=True)
    SP_RESP_DIV_SECT_DESC = models.CharField(max_length=100, null=True, blank=True)
    SP_CONTRACT_CODE = models.CharField(max_length=100, null=True, blank=True)
    SP_ANNUAL_ALLOC_NUM = models.CharField(max_length=20, null=True, blank=True)
    SP_PRELIM_ENGR_START_DT = models.DateField(null=True, blank=True)
    SP_BID_START_DT = models.DateField(null=True, blank=True)
    SP_BID_FINISH_DT = models.DateField(null=True, blank=True)
    SP_AWARD_START_DT = models.DateField(null=True, blank=True)
    SP_AWARD_FINISH_DT = models.DateField(null=True, blank=True)
    SP_CONSTR_FINISH_DT = models.DateField(null=True, blank=True)
    SP_ATI_DT = models.DateField(null=True, blank=True)
    SP_ADDL_FUND_SOURCE2_CD = models.CharField(max_length=8, null=True, blank=True)
    SP_ADDL_FUND_SOURCE2_DESC = models.CharField(max_length=100, null=True, blank=True)
    SP_ADDL_FUND_SOURCE3_CD = models.CharField(max_length=8, null=True, blank=True)
    SP_ADDL_FUND_SOURCE3_DESC = models.CharField(max_length=100, null=True, blank=True)
    SP_CONTRACTOR_DESC = models.CharField(max_length=100, null=True, blank=True)
    SP_EF_PO_CLOSE_OUT  = models.DateField(null=True, blank=True)
    SP_ES_CLOSE_OUT = models.DateField(null=True, blank=True)
    SP_ES_PO_CLOSE_OUT = models.DateField(null=True, blank=True)
    SP_FUNDING_SOURCE_CD = models.CharField(max_length=4, null=True, blank=True)
    SP_FUNDING_SOURCE_DESC = models.CharField(max_length=100, null=True, blank=True)
    SP_PROJECT_INFO_DESC = models.CharField(max_length=100, null=True, blank=True)
    SP_PROJECT_INFO2_DESC = models.CharField(max_length=100, null=True, blank=True)
    SP_PROJECT_KIND_DESC = models.CharField(max_length=100, null=True, blank=True)
    SP_PROJECT_KIND2_DESC = models.CharField(max_length=100, null=True, blank=True)
    SP_BID_NUM = models.CharField(max_length=20, null=True, blank=True)
    SP_SPEC_NUM = models.CharField(max_length=20, null=True, blank=True)

    objects = ProjectManager()

    def __unicode__(self):
        return self.SP_PROJECT_NM

class DepartmentNeed(models.Model):
    department = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    facility_name = models.CharField(max_length=255, null=True, blank=True)
    system = models.CharField(max_length=255, null=True, blank=True)
    material = models.CharField(max_length=255, null=True, blank=True)
    rank = models.CharField(max_length=8, null=True, blank=True)
    system_rank = models.CharField(max_length=8, null=True, blank=True)
    distress = models.CharField(max_length=100, null=True, blank=True)
    correction = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=32, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    maintenance = models.CharField(max_length=255, null=True, blank=True)
    cpa = models.CharField(max_length=255, null=True, blank=True)
    deferred_maint = models.NullBooleanField(null=True, blank=True)
    cdbg_elg = models.NullBooleanField(null=True, blank=True)
    require_data = models.NullBooleanField(null=True, blank=True)
    cost_range = models.CharField(max_length=1, null=True, blank=True)
    est_cost = models.FloatField(null=True, blank=True)
    req_date = models.DateField(null=True, blank=True)
    req_source = models.CharField(max_length=30, null=True, blank=True)
    fac_type = models.CharField(max_length=30, null=True, blank=True)
    pipe_num = models.PositiveIntegerField(null=True, blank=True)
    upstream_struct = models.PositiveIntegerField(null=True, blank=True)
    downstream_struct = models.PositiveIntegerField(null=True, blank=True)
    recommendation = models.CharField(max_length=32, null=True, blank=True)
    size = models.PositiveIntegerField(null=True, blank=True)
    material = models.CharField(max_length=32, null=True, blank=True)
    map_length = models.FloatField(null=True, blank=True)
    fci_percent = models.FloatField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    


