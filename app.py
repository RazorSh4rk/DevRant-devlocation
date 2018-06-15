from pydevrant import *
import sys, os, json

#python app.py [startindex] [endindex]

startindex = int(sys.argv[1])
endindex = int(sys.argv[2])
elem = RantParser()

out = open('lat_lng.json', 'w')
out.write('[\n')
out.close()

for i in range(startindex, endindex):
    try:
        result = elem.get_user_info(i)
        if(result['success'] != False):

            #we are opening and closing one by one
            #so if the script is stopped, you still have 
            #everything it found up to that point
            location = result['profile']['location']
            log = open('locations.txt', 'a')
            log.write(location)
            log.write('\n')
            log.close()

            #getting latitude and longitude json
            #values from a google maps api
            if(not location.isspace()):
                resp = requests.get('http://maps.google.com/maps/api/geocode/json?address=' + location)
                data = resp.json()
                if (data['status'] == 'OK'):
                    out = open('lat_lng.json', 'a')
                    out.write(str(data['results'][0]['geometry']['location']) + ',\n')
                    out.close()
    except:
        #sometimes there are random
        #errors because of the api?
        #im not entirely sure
        print('')

out = open('lat_lng.json', 'a')
out.write(']')
out.close()

#if you want to have locations with population, e.g.
#{"lat":0, "lng":0, "population":2},
#then run this method at the end
def _squash():
    data = [i.strip().split() for i in open("lat_lng.json").readlines()]
    squashed = []
    population = []

    for value in data:
        if(not value in squashed):
            squashed.append(value)
            population.append(1)
        else:
            population[squashed.index(value)] += 1

    out = open('location_data_squashed.json', 'w')
    for i in range(0, len(squashed)):
        try:
            out.write(str(squashed[i][0]) + str(squashed[i][1]) +  '"population":' + str(population[i]) + ',' + str(squashed[i][2]) + str(squashed[i][3]) + '\n')
        except:
            print()