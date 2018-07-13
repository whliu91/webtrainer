from django.contrib import admin
from NNModelManager.models import NNModelHistory, NNJobHistory

# Register your models here.
admin.site.register(NNModelHistory)
admin.site.register(NNJobHistory)