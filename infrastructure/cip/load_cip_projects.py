import csv
from datetime import datetime

from infrastructure.cip.models import Project

def parse_date(date_str, format):
    try:
        return datetime.strptime(date_str, format)
    except:
        return None

projects_file = open('/home/ubuntu/infrastructure/data/cip_snapshot/csv/20130531_cip_dump.csv')
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
    p.SP_ASSET_TYPE_GROUP = project[7]
    p.SP_ASSET_TYPE_CD = project[8]
    p.SP_ASSET_TYPE_DESC = project[9]
    p.SP_SAP_RUN_DT = parse_date(project[23], "%m/%d/%Y")
    p.SP_PRELIM_ENGR_FINISH_DT = parse_date(project[24], "%m/%d/%Y")
    p.SP_DESIGN_FINISH_DT = parse_date(project[25], "%m/%d/%Y")
    p.SP_NTP_DT = parse_date(project[26], "%m/%d/%Y")
    p.SP_NOC_DT = parse_date(project[27], "%m/%d/%Y")
    p.SP_PROJECT_CLOSEOUT_DT = parse_date(project[28], "%m/%d/%Y")
    p.SP_DESIGN_INITIATION_START_DT = parse_date(project[29], "%m/%d/%Y")
    p.SP_CONSTRUCTION_START_DT = parse_date(project[30], "%m/%d/%Y")
    p.SP_BO_BU_DT = parse_date(project[31], "%m/%d/%Y")
    p.SP_TOTAL_CONSTRUCTION_COST = project[32]
    p.SP_TOTAL_PROJECT_COST = project[33]
    p.SP_PLANNING_TO_NOC_DAYS = project[34]
    p.SP_VAR_BL_DESIGN_FINISH_DAYS = project[35]
    p.SP_VAR_DESIGN_BL_ES065_DAYS = project[36]
    p.SP_VAR_BL_NOC_DAYS = project[37]
    p.SP_VAR_NOC_BL_ES130_DAYS = project[38]
    p.SP_DELIVERY_METHOD_CD = project[39]
    p.SP_DELIVERY_METHOD_DESC = project[40]
    p.SP_FIELD_SENIOR_NM = project[46]
    p.SP_PROJECT_PHASE = project[48]
    p.SP_REPORT_PHASE = project[49] #new
    p.SP_PROJECT_STATUS_CD = project[50]
    p.SP_UPDATE_DT = parse_date(project[52], "%m/%d/%Y")
    p.SP_COUNCIL_DISTRICTS = project[55] #new
    p.SP_PROJECT_DESC = project[123]
    p.SP_CLIENT1 = project[124]
    p.SP_CLIENT2 = project[125]
    p.SP_RESP_DIV_SECTION = project[126]
    p.SP_RESP_DIV_SECT_DESC = project[127]
    p.SP_CONTRACT_CODE = project[128]
    p.SP_ANNUAL_ALLOC_NUM = project[129]
    p.SP_PRELIM_ENGR_START_DT = parse_date(project[130], "%m/%d/%Y")
    p.SP_BID_START_DT = parse_date(project[131], "%m/%d/%Y")
    p.SP_BID_FINISH_DT = parse_date(project[132], "%m/%d/%Y")
    p.SP_AWARD_START_DT = parse_date(project[133], "%m/%d/%Y")
    p.SP_AWARD_FINISH_DT = parse_date(project[132], "%m/%d/%Y")
    p.SP_CONSTR_FINISH_DT = parse_date(project[133], "%m/%d/%Y")
    p.SP_ATI_DT = parse_date(project[134], "%m/%d/%Y")
    p.SP_ADDL_FUND_SOURCE2_CD = project[138]
    p.SP_ADDL_FUND_SOURCE2_DESC = project[139]
    p.SP_ADDL_FUND_SOURCE3_CD = project[140]
    p.SP_ADDL_FUND_SOURCE3_DESC = project[141]
    p.SP_CONTRACTOR_DESC = project[142]
    p.SP_EF_PO_CLOSE_OUT = parse_date(project[143], "%m/%d/%Y")
    p.SP_ES_CLOSE_OUT = parse_date(project[144], "%m/%d/%Y")
    p.SP_ES_PO_CLOSE_OUT = parse_date(project[145], "%m/%d/%Y")
    p.SP_FUNDING_SOURCE_CD = project[146]
    p.SP_FUNDING_SOURCE_DESC = project[147]
    p.SP_PROJECT_INFO_DESC = project[149]
    p.SP_PROJECT_INFO2_DESC = project[150]
    p.SP_PROJECT_KIND_DESC = project[151]
    p.SP_PROJECT_KIND2_DESC = project[152]
    p.SP_BID_NUM = project[153]
    p.SP_SPEC_NUM = project[154]
    p.save()
