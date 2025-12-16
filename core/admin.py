from django.contrib import admin
from .models import Subject , StudySession

admin.site.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name", )

admin.site.register(StudySession)
class StudySessonAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "date")


# Register your models here.
