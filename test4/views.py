from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

import json


def index(request):
    return render(request, 'test.html', {})


def add(request):
    a = request.POST['a']
    b = request.POST['b']
    data = {
        'a': int(a),
        'b': int(b),
        'sum': int(a)+int(b)
    }
    return JsonResponse(data)
