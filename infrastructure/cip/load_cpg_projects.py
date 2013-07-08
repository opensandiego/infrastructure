import csv
from datetime import datetime

from infrastructure.cip.models import Project

def parse_date(date_str, format):
    try:
        return datetime.strptime(date_str, format)
    except:
        return None

projects_file = open('data/cip_snapshot/csv/20130531_cip_dump.csv')
projects_reader = csv.reader(projects_file, delimiter=',', quotechar='"')
headerline = projects_reader.next()
for project in projects_reader:
    print project
    p = Project()
    p.SP_SEQ_NUM = project[0]
    p.SP_DATA_DATE = parse_date(project[1], "%m/%d/%Y")
    p.SP_SAPNO = project[2]
    p.SP_TYPE_CD = project[3]
    p.SP_PROJECT_NM = project[4]
    p.SP_SENIOR_NM = project[5]
    p.SP_ASSET_TYPE_GROUP = project[6]
    p.SP_ASSET_TYPE_CD = project[7]
    p.SP_ASSET_TYPE_DESC = project[8]
    p.SP_SAP_RUN_DT = parse_date(project[9], "%m/%d/%Y")
    p.SP_PRELIM_ENGR_FINISH_DT = parse_date(project[10], "%m/%d/%Y")
    p.SP_DESIGN_FINISH_DT = parse_date(project[11], "%m/%d/%Y")
    p.SP_NTP_DT = parse_date(project[12], "%m/%d/%Y")
    p.SP_NOC_DT = parse_date(project[13], "%m/%d/%Y")
    p.SP_PROJECT_CLOSEOUT_DT = parse_date(project[14], "%m/%d/%Y")
    p.SP_DESIGN_INITIATION_START_DT = parse_date(project[15], "%m/%d/%Y")
    p.SP_CONSTRUCTION_START_DT = parse_date(project[16], "%m/%d/%Y")
    p.SP_BO_BU_DT = parse_date(project[17], "%m/%d/%Y")
    p.SP_TOTAL_CONSTRUCTION_COST = project[18]
    p.SP_TOTAL_PROJECT_COST = project[19]
    p.SP_PLANNING_TO_NOC_DAYS = project[20]
    p.SP_VAR_BL_DESIGN_FINISH_DAYS = project[21]
    p.SP_VAR_DESIGN_BL_ES065_DAYS = project[22]
    p.SP_VAR_BL_NOC_DAYS = project[23]
    p.SP_VAR_NOC_BL_ES130_DAYS = project[24]
    p.SP_DELIVERY_METHOD_CD = project[25]
    p.SP_DELIVERY_METHOD_DESC = project[26]
    p.SP_FIELD_SENIOR_NM = project[27]
    p.SP_PROJECT_PHASE = project[28]
    p.SP_PROJECT_STATUS_CD = project[29]
    p.SP_UPDATE_DT = parse_date(project[30], "%m/%d/%Y")
    p.SP_PROJECT_DESC = project[31]
    p.SP_CLIENT1 = project[32]
    p.SP_CLIENT2 = project[33]
    p.SP_RESP_DIV_SECTION = project[34]
    p.SP_RESP_DIV_SECT_DESC = project[35]
    p.SP_CONTRACT_CODE = project[36]
    p.SP_ANNUAL_ALLOC_NUM = project[37]
    p.SP_PRELIM_ENGR_START_DT = parse_date(project[38], "%m/%d/%Y")
    p.SP_BID_START_DT = parse_date(project[39], "%m/%d/%Y")
    p.SP_BID_FINISH_DT = parse_date(project[40], "%m/%d/%Y")
    p.SP_AWARD_START_DT = parse_date(project[41], "%m/%d/%Y")
    p.SP_AWARD_FINISH_DT = parse_date(project[42], "%m/%d/%Y")
    p.SP_CONSTR_FINISH_DT = parse_date(project[43], "%m/%d/%Y")
    p.SP_ATI_DT = parse_date(project[44], "%m/%d/%Y")
    p.SP_ADDL_FUND_SOURCE2_CD = project[45]
    p.SP_ADDL_FUND_SOURCE2_DESC = project[46]
    p.SP_ADDL_FUND_SOURCE3_CD = project[47]
    p.SP_ADDL_FUND_SOURCE3_DESC = project[48]
    p.SP_CONTRACTOR_DESC = project[49]
    p.SP_EF_PO_CLOSE_OUT = parse_date(project[50], "%m/%d/%Y")
    p.SP_ES_CLOSE_OUT = parse_date(project[51], "%m/%d/%Y")
    p.SP_ES_PO_CLOSE_OUT = parse_date(project[52], "%m/%d/%Y")
    p.SP_FUNDING_SOURCE_CD = project[53]
    p.SP_FUNDING_SOURCE_DESC = project[54]
    p.SP_PROJECT_INFO_DESC = project[55]
    p.SP_PROJECT_INFO2_DESC = project[56]
    p.SP_PROJECT_KIND_DESC = project[57]
    p.SP_PROJECT_KIND2_DESC = project[58]
    p.SP_BID_NUM = project[59]
    p.SP_SPEC_NUM = project[60]
    p.save()
