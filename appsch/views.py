from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection
from appsch.models import Subject
from .forms import SubjectForm
from django.http import JsonResponse
import json;

# Create your views here.
def all_user(request):
    return HttpResponse('The Output Of Queries')

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {'subjects': subjects})

def topics_in_subject(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT T.id, T.name
            FROM appsch_topic AS T
            INNER JOIN appsch_chapter AS C ON T.chapter_id = C.id
            INNER JOIN appsch_subject AS S ON C.subject_id = S.id
            WHERE S.name = 'Mathematics';
        """)
        topics = cursor.fetchall()
    
    return render(request, 'topics.html', {'topics': topics})

def subtopics_in_chapter(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ST.id, ST.name
            FROM appsch_subtopic AS ST
            INNER JOIN appsch_topic AS T ON ST.topic_id = T.id
            INNER JOIN appsch_chapter AS C ON T.chapter_id = C.id
            WHERE C.name = 'Algebra';
        """)
        subtopics = cursor.fetchall()
    
    return render(request, 'subtopics.html', {'subtopics': subtopics})



def subject_counts(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT s.name AS subject_name, 
                   COUNT(DISTINCT c.id) AS chapter_count, 
                   COUNT(DISTINCT t.id) AS topic_count, 
                   COUNT(st.id) AS subtopic_count
            FROM appsch_subject s
            LEFT JOIN appsch_chapter c ON c.subject_id = s.id
            LEFT JOIN appsch_topic t ON t.chapter_id = c.id
            LEFT JOIN appsch_subtopic st ON st.topic_id = t.id
            GROUP BY s.name
        """)
        counts = cursor.fetchall()
    
    return render(request, 'subject_counts.html', {'counts': counts})

def subject_list(request):
    subjects = Subject.objects.all()
    form = SubjectForm()
    return render(request, 'subject_list.html', {'subjects': subjects, 'form': form})

def add_subject(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        if name:
            subject = Subject.objects.create(name=name)
            return JsonResponse({'success': True, 'id': subject.id})
    return JsonResponse({'success': False})

