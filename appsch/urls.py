from django.urls import path

from .views import topics_in_subject, subtopics_in_chapter, subject_counts,subject_list
from . import  views

app_name = 'appsch'

urlpatterns = [
    
       
     path('topics/', views.topics_in_subject),
     path('subtopics/', views.subtopics_in_chapter),
     path('subject_counts/', views.subject_counts),
     path('subjects/', views.subject_list, name='subject_list'),
     path('add_subject/', views.add_subject, name='add_subject'),
     
               
]

