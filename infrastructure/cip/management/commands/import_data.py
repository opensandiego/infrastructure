from django.core.management.base import BaseCommand, CommandError
from infrastructure.cip.models import Project
from optparse import make_option
from datetime import datetime
import csv

class Command(BaseCommand):
    args = '<csvfile>'
    option_list = BaseCommand.option_list + (
        make_option('--header',
            action='store_true',
            dest='header',
            default=False,
            help='CSV has Header?'),
        )

    def handle(self,*args,**options):
        """docstring for handle"""
        csv_file = args[0]
        project_file = open(csv_file)
        projects_reader = csv.reader(project_file, delimiter=',', quotechar='"')
        if options['header']:
            headerline = projects_reader.next()
        for project_row in projects_reader:
            self.create_or_update_project(project_row)

    def parse_date(self,date_str, format = "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(date_str, format)
        except:
            return None

    def create_or_update_project(self,project_row):
        """docstring for new_project"""
        project_seq_nr = project_row[0]
        print project_seq_nr
        try:
            p= Project.objects.get(SP_SEQ_NUM=int(project_seq_nr))
            print "update"
        except Project.DoesNotExist:
            print "new"
            p= Project()
        p.SP_SEQ_NUM = project_row[0]
        p.SP_DATA_DATE = self.parse_date(project_row[1])
        p.SP_SAPNO = project_row[2]
        p.SP_TYPE_CD = project_row[3]
        p.SP_PROJECT_NM = project_row[4]
        p.SP_SENIOR_NM = project_row[5]
        p.SP_ASSET_TYPE_GROUP = project_row[7]
        p.SP_ASSET_TYPE_CD = project_row[8]
        p.SP_ASSET_TYPE_DESC = project_row[9]
        p.SP_FISCAL_YEAR = project_row[22]
        p.SP_SAP_RUN_DT = self.parse_date(project_row[23])
        p.SP_PRELIM_ENGR_FINISH_DT = self.parse_date(project_row[24])
        p.SP_DESIGN_FINISH_DT = self.parse_date(project_row[25])
        p.SP_NTP_DT = self.parse_date(project_row[26])
        p.SP_NOC_DT = self.parse_date(project_row[27])
        p.SP_PROJECT_CLOSEOUT_DT = self.parse_date(project_row[28])
        p.SP_DESIGN_INITIATION_START_DT = self.parse_date(project_row[29])
        p.SP_CONSTRUCTION_START_DT = self.parse_date(project_row[30])
        p.SP_BO_BU_DT = self.parse_date(project_row[31])
        p.SP_TOTAL_CONSTRUCTION_COST = project_row[32]
        p.SP_TOTAL_PROJECT_COST = project_row[33]
        p.SP_PLANNING_TO_NOC_DAYS = project_row[34]
        p.SP_VAR_BL_DESIGN_FINISH_DAYS = project_row[35]
        p.SP_VAR_DESIGN_BL_ES065_DAYS = project_row[36]
        p.SP_VAR_BL_NOC_DAYS = project_row[37]
        p.SP_VAR_NOC_BL_ES130_DAYS = project_row[38]
        p.SP_DELIVERY_METHOD_CD = project_row[39]
        p.SP_DELIVERY_METHOD_DESC = project_row[40]
        p.SP_FIELD_SENIOR_NM = project_row[46]
        p.SP_PROJECT_PHASE = project_row[48]
        p.SP_REPORT_PHASE = project_row[49] #new
        p.SP_PROJECT_STATUS_CD = project_row[50]
        p.SP_UPDATE_DT = self.parse_date(project_row[52])
        p.SP_COUNCIL_DISTRICTS = project_row[55] #new
        p.SP_PROJECT_DESC = project_row[59]
        p.SP_CLIENT1 = project_row[60]
        p.SP_CLIENT2 = project_row[61]
        p.SP_RESP_DIV_SECTION = project_row[62]
        p.SP_RESP_DIV_SECT_DESC = project_row[63]
        p.SP_CONTRACT_CODE = project_row[64]
        p.SP_ANNUAL_ALLOC_NUM = project_row[65]
        p.SP_PRELIM_ENGR_START_DT = self.parse_date(project_row[66])
        p.SP_BID_START_DT = self.parse_date(project_row[67])
        p.SP_BID_FINISH_DT = self.parse_date(project_row[68])
        p.SP_AWARD_START_DT = self.parse_date(project_row[69])
        p.SP_AWARD_FINISH_DT = self.parse_date(project_row[70])
        p.SP_CONSTR_FINISH_DT = self.parse_date(project_row[71])
        p.SP_ATI_DT = self.parse_date(project_row[72])
        p.SP_ADDL_FUND_SOURCE2_CD = project_row[74]
        p.SP_ADDL_FUND_SOURCE2_DESC = project_row[75]
        p.SP_ADDL_FUND_SOURCE3_CD = project_row[76]
        p.SP_ADDL_FUND_SOURCE3_DESC = project_row[77]
        p.SP_CONTRACTOR_DESC = project_row[78]
        p.SP_EF_PO_CLOSE_OUT = self.parse_date(project_row[79])
        p.SP_ES_CLOSE_OUT = self.parse_date(project_row[80])
        p.SP_ES_PO_CLOSE_OUT = self.parse_date(project_row[81])
        p.SP_FUNDING_SOURCE_CD = project_row[82]
        p.SP_FUNDING_SOURCE_DESC = project_row[83]
        p.SP_PROJECT_INFO_DESC = project_row[85]
        p.SP_PROJECT_INFO2_DESC = project_row[86]
        p.SP_PROJECT_KIND_DESC = project_row[87]
        p.SP_PROJECT_KIND2_DESC = project_row[88]
        p.SP_BID_NUM = project_row[89]
        p.SP_SPEC_NUM = project_row[90]
        try:
            p.save()
        except:
            print "Project not saved: %s" % project_seq_nr
