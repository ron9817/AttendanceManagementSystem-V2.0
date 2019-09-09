from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime


# Create your views here.
#0-total
#1-attended
#2-off
#3-proxy
attendance={
    "STQA":[0,0,0,0],
    "AI":[0,0,0,0],
    "END":[0,0,0,0],
    "InfraSec":[0,0,0,0],
    "Project A":[0,0,0,0],
    "CSL":[0,0,0,0],
    "IS":[0,0,0,0],
    "AdvSec":[0,0,0,0],
    "N/W lab":[0,0,0,0],
    "AndroidLab":[0,0,0,0]
}
def index(request):
    # today=datetime.date.today()

    #datetime.date(year, month, day)
    timetable={
        "Mon":["STQA","AI","END","InfraSec","Project A"],
        "Tue":["CSL","InfraSec","AI","IS","END","STQA"],
        "Wednes":["CSL","END","AdvSec","AI","InfraSec"],
        "Thurs":["InfraSec","AI","N/W lab","END","CSL"],
        "Fri":["END","AI","InfraSec","AndroidLab","STQA","STQA"],
        "Sat":[],
        "Sun":[]
    }
    weekMap=["Mon","Tue","Wednes","Thurs","Fri","Sat","Sun"]
    if (request.method=="POST"):
        date=request.POST["changeDate"]
        year=int(date[0:4])
        month=int(date[5:7])
        day=int(date[8:10])
        #print(day,month,year)
        #return HttpResponse(1)
        weekDay=datetime.date(year,month,day).weekday()
        #print(day,month,year,weekDay)
        #return HttpResponse(1)
    else:
        today=datetime.date.today()
        year=today.year
        month=today.month
        day=today.day
        weekDay=today.weekday()
        #print(day,month,year,weekDay)
    context={
        "timeTable":timetable,
        "active":weekMap[weekDay],
        "activeDate":[year,month-1,day],
        "attendance":attendance,
        "proxySubject":set(attendance.keys())-set(timetable[weekMap[weekDay]])
        }

    return render(request, "attendance_controller/index.html",context)
@csrf_exempt
def calculate(request):
    data = json.loads(request.body)
    print(data)
    lecPresent=data["present"]
    lecAbsent=data["absent"]
    lecOff=data["off"]
    lecProxy=data["proxy"]
    print(lecPresent,lecAbsent,lecOff,lecProxy)
    for i in lecPresent:
        attendance[i][0]+=1
        attendance[i][1]+=1
    for i in lecAbsent:
        attendance[i][0]+=1
    for i in lecOff:
        attendance[i][2]+=1
    for i in lecProxy:
        attendance[i][0]+=1
        attendance[i][1]+=1
        attendance[i][3]+=1
    print("\nAttendance\n")
    print(attendance)
    return JsonResponse({
        "msg":"successfully marked attendance for "+data["date"]
    })