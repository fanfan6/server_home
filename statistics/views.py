from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'static.html', {'res': {}})


def app_pass(request):
    return render(request, 'app_pass.html', {'res':{}})


def mod_grade(request):
    return render(request, 'mod_grade.html', {'res':{}})
