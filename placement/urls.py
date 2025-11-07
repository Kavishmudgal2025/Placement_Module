from django.contrib import admin
from django.urls import path , include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.signin, name='index'),

    path('profile/',views.student_profile, name='profile'),

    path('register/',views.signup, name='signup'),

    path('thankyou/', views.job_post_thankyou, name='thankyou'),

    path ('admin_login/', views.admin, name='admin_login'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('export_students/', views.export_students, name='export_students'),

    path('profile/update/', views.updateProfile, name='updateProfile'),

    path('admin_home/job_update/', views.job_post, name='job_update'),
    path('admin_home/view_jobs/', views.view_jobs, name='view_jobs'),
    path('export_jobs/', views.export_jobs, name='export_jobs'),

    path('apply/<uuid:job_id>/', views.job_application, name='apply_job'),

    path('admin_home/edit_job/<uuid:job_id>/', views.edit_job,name='edit_job'),

    path('admin_home/view_jobs/applied_student_list/<uuid:job_id>/', views.applied_student_list, name="applied_student_list"),

    path('admin_home/view_jobs/applied_student_list/<uuid:job_id>/status_update/<uuid:application_id>/', views.status_update, name="status_update"),

    path('admin_home/view_jobs/applied_student_list/export/<uuid:job_id>/', views.export_applied_students, name="export_applied_students"),
    
    path('design/', views.dashboard, name="dashboard")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
