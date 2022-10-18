from urllib import response
from django.shortcuts import render
from django.http import HttpResponse # create http response(for testing)
import csv
from collections import defaultdict
from datetime import date
import json



def getQuery(request):
    if request.POST:
        # get formdata from frontend
        year = request.POST['year']
        startMonth = request.POST['startMonth']
        startDay = request.POST['startDay']
        startHour = request.POST['startHour']
        endMonth = request.POST['endMonth']
        endDay = request.POST['endDay']
        endHour = request.POST['endHour']

        start = year + "/" + startMonth + "/" + startDay + "-" + ("%02d" % int(startHour)) + ":00"
        end = year + "/" + endMonth + "/" + endDay + "-" + ("%02d" % int(endHour)) + ":00"

        library = defaultdict(dict)
        # read file
        with open('/home/tsai-jen/Customize-2DString-/mysite/weather/codes/file_output(try2)_wind.csv', newline='') as csvfile:
            rows = csv.reader(csvfile)
            next(rows)
            for row in rows:
                tmp = row
                # tmp[0]: date and hour
                # print(tmp)
                # index = tmp[0] + "-" + tmp[1]
                index = tmp[0].replace(' ', '-')
                library[index]['date'] = tmp[0].split(' ')[0]
                library[index]['hour'] = tmp[0].split(' ')[1].split(':')[0]
                library[index]['WD'] = tmp[3]
                library[index]['WS'] = float(tmp[4])
                library[index]['PS'] = float(tmp[5])
                library[index]['TP'] = float(tmp[6])
                library[index]['RH'] = int(tmp[7])
        # print(library['2018/12/31-11'])
        # print(library['2018/1/4-2']['PS'])
        #ctx: a dict will be sent to frontend as result
        # print(library.keys())
        ctx = {}
        ctx['startMonth'] = startMonth
        ctx['startDay'] = startDay
        ctx['startHour'] = startHour
        ctx['endMonth'] = endMonth
        ctx['endDay'] = endDay
        ctx['endHour'] = endHour
        # ctx['start'] = [startMonth, startDay, startHour]
        # ctx['end'] = [endMonth, endDay, endHour]
        
        # dataset store in ctx
        dateData = []
        hourData = []
        WDdata = []
        WSdata = []
        PSdata = []
        TPdata = []
        RHdata = []
        imageData = []

        # select index between two dates
        dates = list(library.keys())
        # dates.index(start): the index num of the start
        # dates.index(end): the index num of the end
        for i in range(dates.index(start), dates.index(end)+1):
            index = dates[i]
            dateData.append(library[index]['date'].replace('/','-'))
            hourData.append(library[index]['hour'])
            imageData.append(library[index]['date'].replace('/','-') + "-" + library[index]['hour'] + "-00.png")
            PSdata.append(library[index]['PS'])
            TPdata.append(library[index]['TP'])
            RHdata.append(library[index]['RH'])
            WSdata.append(library[index]['WS'])
            WDdata.append(library[index]['WD'])

        # ctx['total'] = dates.index(end) - dates.index(start) + 1
        ctx['resultDate'] = dateData
        ctx['resultHour'] = hourData
        ctx['resultImage'] = imageData
        ctx['resultPS'] = PSdata
        ctx['resultTP'] = TPdata
        ctx['resultRH'] = RHdata
        ctx['resultWS'] = WSdata
        ctx['resultWD'] = WDdata
        # jsonDate = json.dumps(ctx['resultDate'])
        # ctx['jsonDate'] = jsonDate
        # print(type(ctx))
        # print(ctx)

        # print("a:", a)
        # return HttpResponse("<h1>home page</h1>")
        return render(request, "bbtw.html", ctx)

# Create your views here.
def bbtw(request):
    # return HttpResponse("Hello, world. You're at the query index.")
    # return 30 data (100) 
    return render(request, 'bbtw.html')