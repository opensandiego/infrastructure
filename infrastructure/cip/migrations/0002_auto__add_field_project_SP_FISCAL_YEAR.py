# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Project.SP_FISCAL_YEAR'
        db.add_column(u'cip_project', 'SP_FISCAL_YEAR',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Project.SP_FISCAL_YEAR'
        db.delete_column(u'cip_project', 'SP_FISCAL_YEAR')


    models = {
        u'cip.contractor': {
            'Meta': {'object_name': 'Contractor'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cip.departmentneed': {
            'Meta': {'object_name': 'DepartmentNeed'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cdbg_elg': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'correction': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cost_range': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'cpa': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'deferred_maint': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'distress': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'downstream_struct': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'est_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fac_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'facility_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fci_percent': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'maintenance': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'map_length': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'material': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pipe_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'recommendation': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'req_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'req_source': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'require_data': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'system_rank': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'upstream_struct': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'cip.person': {
            'Meta': {'object_name': 'Person'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cip.phase': {
            'Meta': {'object_name': 'Phase'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'cip.project': {
            'Meta': {'object_name': 'Project'},
            'SP_ADDL_FUND_SOURCE2_CD': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'SP_ADDL_FUND_SOURCE2_DESC': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_ADDL_FUND_SOURCE3_CD': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'SP_ADDL_FUND_SOURCE3_DESC': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_ANNUAL_ALLOC_NUM': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'SP_ASSET_TYPE_CD': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'SP_ASSET_TYPE_DESC': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_ASSET_TYPE_GROUP': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_ATI_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_AWARD_FINISH_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_AWARD_START_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_BID_FINISH_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_BID_NUM': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'SP_BID_START_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_BO_BU_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_CLIENT1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_CLIENT2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_CONSTRUCTION_START_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_CONSTR_FINISH_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_CONTRACTOR_DESC': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_CONTRACT_CODE': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_COUNCIL_DISTRICTS': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_DATA_DATE': ('django.db.models.fields.DateField', [], {}),
            'SP_DELIVERY_METHOD_CD': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'SP_DELIVERY_METHOD_DESC': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_DESIGN_FINISH_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_DESIGN_INITIATION_START_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_EF_PO_CLOSE_OUT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_ES_CLOSE_OUT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_ES_PO_CLOSE_OUT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_FIELD_SENIOR_NM': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_FISCAL_YEAR': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'SP_FUNDING_SOURCE_CD': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'SP_FUNDING_SOURCE_DESC': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_NOC_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_NTP_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_PLANNING_TO_NOC_DAYS': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'SP_PRELIM_ENGR_FINISH_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_PRELIM_ENGR_START_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_PROJECT_CLOSEOUT_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_PROJECT_DESC': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'SP_PROJECT_INFO2_DESC': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_PROJECT_INFO_DESC': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_PROJECT_KIND2_DESC': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_PROJECT_KIND_DESC': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_PROJECT_NM': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'SP_PROJECT_PHASE': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_PROJECT_STATUS_CD': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'SP_REPORT_PHASE': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_RESP_DIV_SECTION': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'SP_RESP_DIV_SECT_DESC': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_SAPNO': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'SP_SAP_RUN_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_SENIOR_NM': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'SP_SEQ_NUM': ('django.db.models.fields.IntegerField', [], {}),
            'SP_SPEC_NUM': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'SP_TOTAL_CONSTRUCTION_COST': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'SP_TOTAL_PROJECT_COST': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'SP_TYPE_CD': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'SP_UPDATE_DT': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'SP_VAR_BL_DESIGN_FINISH_DAYS': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'SP_VAR_BL_NOC_DAYS': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'SP_VAR_DESIGN_BL_ES065_DAYS': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'SP_VAR_NOC_BL_ES130_DAYS': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['cip']