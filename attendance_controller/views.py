from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.

def index(request):
    timetable={
        "Mon":["STQA","AI","END","IfraSec","Project A"],
        "Tue":["CSL","InfrSec","AI","IS","END","STQA"],
        "Wednes":["CSL","END","AdvSec","AI","InfraSec"],
        "Thurs":["InfraSec","AI","N/W lab","END","CSL"],
        "Fri":["END","AI","InfraSec","AndroidLab","STQA","STQA"]
    }
    context={
        "timeTable":timetable,
        "active":"Tue"
        }
    return render(request, "attendance_controller/index.html",context)
@csrf_exempt
def calculate(request):
    data = json.loads(request.body)
    return JsonResponse({
        "msg":"successfully marked attendance for "+data["date"]
    })