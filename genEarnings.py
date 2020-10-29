import os
import folium
import numpy as np
import csv
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import genkml

def genEarnings():
    #data=([-114.0676896833365,51.163570378739635,1],[-114.0676896833365,51.173570378739635,1])
    try:
        pass
        #os.remove('hotspotEarnings.csv')
    except:
        pass

    #genkml.genkml(earnings=True)
    
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
          radius=d[2]*5,
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


    #plot earnings as histogram
    with open('hotspotsEarnings.csv', newline='') as f:
        reader = csv.reader(f)
        hotspots = list(reader)
    hotspots=hotspots[1:]

    earn=[]
    mid=0
    high=0
    zero=0
    totalhnt=0
    totalmid=0
    totalhigh=0
    for hotspot in hotspots:
        #            lat        lng        earnings          name
        if str(hotspot[4]) == '0':
            zero=zero+1
            #print('hotspot ', hotspot[0],'earned ', hotspot[4])
        elif float(hotspot[4]) < 50:
            earn.append(float(hotspot[4]))
            mid=mid+1
            totalhnt=totalhnt+float(hotspot[4])
            totalmid=totalmid+float(hotspot[4])
        else:
            high=high+1
            print('hotspot ', hotspot[0],'earned ', hotspot[4])
            totalhnt=totalhnt+float(hotspot[4])
            totalhigh=totalhigh+float(hotspot[4])
        #data=heat
    print('hotspot count with earnings of 0(count) = ',zero)
    print('hotspot count with earnings > 500(count) = ',high)
    print('hotspot count with earnings < 500(count) = ',mid)
    #print('zero count',zero)
    print('total HNT earnings(HNT) = ',totalhnt)
    print('total hotspot earnings > 500HNT(HNT) = ', totalhigh)
    print('total hotspot earnings 0<mid<500HNT(HNT) = ', totalmid )

    print('percentage of hotspots with earnings > 500 HNT(%) = ', high/(high +mid)*100)
    print('total percentage of HNT of top earners(%) = ', (totalhigh/totalhnt)*100)
    n, bins, patches = plt.hist(earn, 10)#, density=True, facecolor='g', alpha=0.75,)
    plt.xlabel('Weekly Earnings(HNT)')
    plt.ylabel('Count(Number of Hotspots)')
    #wit=str(wl[w]['name'])
    #plt.title('Packets from '+hname+' measured at '+wit)
    plt.title('Weekly Earnings week 42')
    #plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    #plt.xlim(40, 160)
    #plt.ylim(0, 0.03)
    plt.grid(True)
    #plt.show()
    #strFile=str(wl[w]['name'])+'.jpg'
    #strWitness=str(wl[w]['name'])
    
    #if os.path.isfile(strFile):
        #print('remove')
        #os.remove(strFile)   # Opt.: os.system("rm "+strFile)
    plt.savefig('earnings')
    #encoded[strWitness] = base64.b64encode(open(hname+'//'+strFile, 'rb').read())
    plt.close()
    
