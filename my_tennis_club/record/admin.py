from django.contrib import admin
from .models import PlayRecord

class PlayRecordAdmin(admin.ModelAdmin):
  list_display = ("username", "score", "date",)
  
admin.site.register(PlayRecord, PlayRecordAdmin)