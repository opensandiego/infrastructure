import datetime
from haystack import indexes
from infrastructure.cip.models import *


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='SP_PROJECT_NM')


    def get_model(self):
        return Project

    def index_queryset(self,**kwargs):
        return self.get_model().objects.all()
