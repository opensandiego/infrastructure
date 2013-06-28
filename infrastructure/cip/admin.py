from django.contrib import admin
from infrastructure.cip.models import Project 

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('SP_PROJECT_NM', 'SP_ASSET_TYPE_GROUP', 'SP_ASSET_TYPE_DESC', 'SP_DELIVERY_METHOD_DESC', 'SP_PROJECT_PHASE', 'SP_CLIENT1', 'SP_CLIENT2', 'SP_RESP_DIV_SECTION', 'SP_FUNDING_SOURCE_DESC')
    list_filter = ('SP_ASSET_TYPE_GROUP', 'SP_ASSET_TYPE_DESC', 'SP_DELIVERY_METHOD_DESC', 'SP_PROJECT_PHASE', 'SP_CLIENT1', 'SP_CLIENT2', 'SP_RESP_DIV_SECTION', 'SP_FUNDING_SOURCE_DESC', 'SP_ADDL_FUND_SOURCE2_DESC', 'SP_ADDL_FUND_SOURCE3_DESC', 'SP_PROJECT_KIND_DESC')

admin.site.register(Project, ProjectAdmin)
