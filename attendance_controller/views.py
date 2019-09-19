from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

from .models import Dailyattendance


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

monthMap={
    'Jan':'01',
    'Feb':'02',
    'Mar':'03',
    'Apr':'04',
    'May':'05',
    'Jun':'06',
    'Jul':'07',
    'Aug':'08',
    'Sep':'09',
    'Oct':'10',
    'Nov':'11',
    'Dec':'12'
    }
timetable={
        "Mon":["Project A"],
        "Tue":["CSL","InfraSec","AI","IS","END","STQA"],
        "Wednes":["CSL","END","AdvSec","AI","InfraSec","InfraSec"],
        "Thurs":["AI","AI","InfraSec","STQA","N/W lab","END","CSL"],
        "Fri":["AI","InfraSec","STQA","STQA","AndroidLab","END","END"],
        "Sat":[],
        "Sun":[]
    }
weekMap=["Mon","Tue","Wednes","Thurs","Fri","Sat","Sun"]

def index(request):
    # today=datetime.date.today()
    #datetime.date(year, month, day)

    if (request.method=="POST"):
        date=request.POST["changeDate"]
        year=int(date[0:4])
        month=int(date[5:7])
        day=int(date[8:10])
        #print(day,month,year)
        #return HttpResponse(1)
        weekDay=datetime.date(year,month,day).weekday()
        attendance={}
        for subject in timetable[weekMap[weekDay]]:
            Qs=Dailyattendance.objects.filter(subject=subject).exclude(ispresent=0)
            totalLec=len(Qs)
            attendedLec=len(Qs.filter(ispresent=1))
            attendance[subject]=[totalLec,attendedLec,0,0]
        #print(day,month,year,weekDay)
        #return HttpResponse(1)
    else:
        today=datetime.date.today()
        year=today.year
        month=today.month
        day=today.day
        weekDay=today.weekday()
        attendance={}
        for subject in timetable[weekMap[weekDay]]:
            Qs=Dailyattendance.objects.filter(subject=subject).exclude(ispresent=0)
            totalLec=len(Qs)
            attendedLec=len(Qs.filter(ispresent=1))
            attendance[subject]=[totalLec,attendedLec,0,0]
        #print(day,month,year,weekDay)
    totalA=(len(Dailyattendance.objects.filter(ispresent=1)))/(len(Dailyattendance.objects.exclude(ispresent=0)))*100
    context={
        "timeTable":timetable,
        "active":weekMap[weekDay],
        "activeDate":[year,month-1,day],
        "attendance":attendance,
        "proxySubject":set(attendance.keys())-set(timetable[weekMap[weekDay]]),
        "total":totalA
        }
    return render(request, "attendance_controller/index.html",context)
@csrf_exempt
def calculate(request):
    data = json.loads(request.body)
    date=data["date"]
    year=date[11:15]
    day=date[8:10]
    month=date[4:7]
    date=year+"-"+monthMap[month]+"-"+day
    lecPresent=data["present"]
    lecAbsent=data["absent"]
    lecOff=data["off"]
    lecProxy=data["proxy"]
    print(lecPresent,lecAbsent,lecOff,lecProxy)
    for i in lecPresent:
        attendanceRow=Dailyattendance(ispresent=1, subject=i, date=date)
        attendanceRow.save()
        attendance[i][0]+=1
        attendance[i][1]+=1
    for i in lecAbsent:
        attendanceRow=Dailyattendance(ispresent=-1, subject=i, date=date)
        attendanceRow.save()
        attendance[i][0]+=1
    for i in lecOff:
        attendanceRow=Dailyattendance(ispresent=0, subject=i, date=date)
        attendanceRow.save()
        attendance[i][2]+=1
    for i in lecProxy:
        attendanceRow=Dailyattendance(ispresent=1, subject=i, date=date)
        attendanceRow.save()
        attendance[i][0]+=1
        attendance[i][1]+=1
        attendance[i][3]+=1
    return JsonResponse({
        "msg":"successfully marked attendance for "+date
    })