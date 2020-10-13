import requests
import json
import simplekml
import csv
import sys
from datetime import datetime, timedelta



def get_total(addr):
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    #print(my_date.isoformat())
    nowstr=str(now.isoformat())
    yesterdaystr=str(yesterday.isoformat())
    url = "https://api.helium.io/v1/hotspots/" +str(addr)+ "/rewards/sum" + "?min_time="+yesterdaystr+"&max_time="+nowstr
    #print(url)
    data=requests.get(url=url)
    data=data.json()
    data=data['data']
    total=data['sum']
    try:
        #print(total)
        return str(float(total)/1E9)
    except:
        #print(total)
        return str(0)
    #print(url)
    #print(data)


def genkml(earnings=False):
    url = "https://api.helium.io/v1/hotspots"
    data=requests.get(url=url)
    data=data.json()
    cursor = data['cursor']
    data = data['data']
    jsondata=data

    while(cursor):
        data=requests.get(url=url+'?cursor='+cursor)
        data=data.json()
        try:
            cursor = data['cursor']
        except:
            cursor=None
        data = data['data']
        jsondata=jsondata+data
        #print(len(jsondata))
        #print(cursor)


    if earnings:
        fout=open("hotspotsEarnings.csv","w+")
    else:
        fout=open("hotspots.csv","w+")
    fout.write('Name, Latitude, Longitude, Address, 24hrEarnings\n')
    count=0
    noloccount=0
    for hotspot in jsondata:
        try:
            #print(hotspot['name'], hotspot['lat'], hotspot['lng'])
            #print(hotspot)
            addr=str(hotspot['address'])
            if earnings:
                total=get_total(addr)
            else:
                total=str(0)
            a=str(hotspot['name']) +','+ str(hotspot['lat']) +','+ str(hotspot['lng'])+','+ addr+','+total+'\n'
            fout.write(a)
            count=count+1
        except KeyError:
            noloccount=noloccount+1
            #print(hotspot)
            pass
        except Exception as e:
            print(e.__class__, "Exception occurred.")
            #print(hotspot)
            pass

    print('Number of Hotspots with lat,lon: ',count)
    print('Number of Hotspots without lat,lon: ',noloccount)

    fout.close()


    inputfile = csv.reader(open('hotspots.csv','r'))
    kml=simplekml.Kml()

    for row in inputfile:
        kml.newpoint(name=row[0], coords=[(row[2],row[1])])

    kml.save('hotspots.kml')
