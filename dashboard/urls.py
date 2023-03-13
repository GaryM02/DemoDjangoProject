from django.urls import path

from . import views

urlpatterns = [
    path('projects/', views.ProjectsList.as_view(), name='projects'),
    path('projects/?P<str:name>', views.project_details, name='viewproject'),
    path('createproject/', views.create_project_view, name='createproject'),

]