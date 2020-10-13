import os
import folium
import numpy as np
import csv
from folium.plugins import HeatMap
import genkml

def genEarnings():
    #data=([-114.0676896833365,51.163570378739635,1],[-114.0676896833365,51.173570378739635,1])
    try:
        os.remove('hotspotEarnings.csv')
    except:
        pass

    genkml.genkml(earnings=True)
    
    with open('hotspotsEarnings.csv', newline='') as f:
        reader = csv.reader(f)
        hotspots = list(reader)
    hotspots=hotspots[1:]

    heat=[]
    for hotspot in hotspots:
        #            lat        lng        earnings          name
        heat.append([hotspot[1],hotspot[2],float(hotspot[4]),hotspot[0]])
    data=heat

    m = folium.Map([50., -114.], tiles='stamentoner', zoom_start=6)

    # I can add marker one by one on the map
    for d in data:
        folium.Circle(
          location=[d[0],d[1]],
          popup=str(d[3])+'\n'+str(d[2]),
          radius=d[2]*10,
          color='crimson',
          fill=True,
          fill_color='crimson'
       ).add_to(m)
     
    # Save it as html
    m.save('earnCircle.html')

    m = folium.Map([50., -114.], tiles='stamentoner', zoom_start=6)

    d5=[]
    d20=[]
    d50=[]
    d100=[]
    for d in data:
        if d[2]<5:
            d5.append([d[0],d[1],1.0])
        elif d[2]<20:
            d20.append([d[0],d[1],1.0])
        elif d[2]<50:
            d50.append([d[0],d[1],1.0])
        else:
            d100.append([d[0],d[1],1.0])
            
    HeatMap(d5,radius=5,max_zoom=18,max_val=5.,min_opacity=6.0,gradient= {0.4: 'blue', 0.65: 'lime', 1: 'green'}).add_to(m)
    HeatMap(d20,radius=10,max_zoom=18,max_val=5.,min_opacity=6.0,gradient= {0.4: 'blue', 0.65: 'lime', 1: 'green'}).add_to(m)
    HeatMap(d50,radius=20,max_zoom=18,max_val=5.,min_opacity=6.0,gradient= {0.4: 'blue', 0.65: 'lime', 1: 'green'}).add_to(m)
    HeatMap(d100,radius=30,max_zoom=18,max_val=5.,min_opacity=6.0,gradient= {0.4: 'blue', 0.65: 'lime', 1: 'green'}).add_to(m)
    #HeatMap(data,min_opacity=0.5,max_zoom=3,max_val=6.0,radius=50,blur=100).add_to(m)
    #,gradient= {0.4: 'blue', 0.65: 'lime', 1: 'red'}
    m.save('earnHeat.html')
