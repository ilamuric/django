from django.shortcuts import render
from django.http import HttpResponse
from .  import models
# Create your views here.

def index(request):
    courses = models.Course.objects.all()
    return render(request,'courses.html',{'courses':courses})


def single_course(request,course_id):
    course  = models.Course.objects.get(pk=course_id)
    return render(request, 'singe_course.html', {'course': course})
