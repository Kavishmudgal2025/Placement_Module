from django.contrib import admin
from .models import Student, StudentProfile, Job, JobApplication

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name','sId')

admin.site.register(StudentProfile)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title','organization','post_date', 'application_deadline')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job', 'apply_date')

    def student(self, obj):
        return f"{obj.sId.name} - {obj.sId.sId}"

    def job(self, obj):
        return obj.job_id.title   # or add more details if you like
