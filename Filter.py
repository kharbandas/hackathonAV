import numpy as np
import pandas as pd
import math
pd.options.mode.chained_assignment = None
from os import system, name


#Used to clear the console between filters
def clear():
    # for windows the name is 'nt'
    if name == 'nt':
        _ = system('cls')

    # and for mac and linux, the os.name is 'posix'
    else:
        _ = system('clear')


##Helper function for filterDistance. Modified distance function's source code from
#https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
def distance_in_miles(lat1,long1,lat2,long2):
  R = 6371 #Radius of the earth in km
  dLat = deg2rad(lat2-lat1)
  dLong = deg2rad(long2-long1)
  a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLong/2) * math.sin(dLong/2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  d = R * c * .621371 #distance in miles
  return d

def deg2rad(deg):
  return deg * (math.pi/180)

#A shelter may have a requirement on the distance they can travel to get the
#food. This function drops restaurants from the table if they are futher than
#a given radius from the shelter.
def filterDistance(shelter_lat, shelter_long, restaurants, radius):
  temp = restaurants.copy(deep = True)
  temp['DistanceFromShelter'] = 0.0
  for i in range(len(restaurants)):
    temp['DistanceFromShelter'][i] = distance_in_miles(shelter_lat, shelter_long, temp['latitude'][i], temp['longitude'][i])
    #coords_1 = (shelter_lat, shelter_long)
    #coords_2 = (restaurants.latitude[i], restaurants.longitude[i])
    #temp['DistanceFromShelter'][i] = geodesic(coords_1, coords_2).mi
  temp =  temp[temp.DistanceFromShelter <= radius]
  temp = temp.sort_values('DistanceFromShelter')
  return temp

#A shelter may have a preference on cuisine due to religion, health, allergies,
#and more. This function drops restaurants from the table if they do not provide
#the cusine the shelter is looking for.
def filterCuisine(cuisine_preference, restaurants):
  temp = restaurants.copy(deep = True)
  temp = temp[temp.type.str.contains(cuisine_preference)]
  return temp

#A shelter has a number of people that they must serve food to. This function drops
#restaurants from the table if they don't have enough available meals.
def filterNumberOfMeals(numMeals, restaurants):
  temp = restaurants.copy(deep = True)
  temp = temp[temp.meals >= numMeals]
  return temp

#A shelter has a maximum amount of time they can hold food. This function drops
#restaurants from the table if they have food that lasts longer than the shelter's
#shelf life. This is in an effort to not waste donated food.
def filterShelfLife(shelf_life_preference, restaurants):
  temp = restaurants.copy(deep = True)
  temp = temp[temp['shelf life'] <= shelf_life_preference]
  return temp

#After any number of filters, there may be n remaining restaraunts. This function first finds restaurants
#that have the most previous deliveries with. If there are multiple remaining restaurants with the same
#amount of previous deliveries, the closest restaurant to the shelter will be the preference.
def sheltersPreference(restaurants, shelter_idx, connections):
    #restaurants_indices = restaurants.index
    restaurants_most_connections = get3MaxIndices(connections[shelter_idx], restaurants.index)
    #print(get3MaxIndices(connections[shelter_idx], restaurants.index))
    #rest = restaurants[restaurants['idx'] in restaurants_most_connections]
    return restaurants_most_connections


def getMaxIndex(connections_array, indices):
  #find max connections
  m = 0
  for i in indices:
    if connections_array[i] > m:
      m = connections_array[i]
  #find first occurents of max connections
  for i in indices:
    if connections_array[i] == m:
      return i
  return 0

def get3MaxIndices(connections_array, indices):
  m = []
  for i in indices:
    #print(m)
    m.append(connections_array[i])
    m.sort(reverse = True)
    m = m[0:3]
  ret = []
  for j in range(len(m)):
    for i in indices:
      if(len(ret) == 3):
        return ret
      if connections_array[i] == m[j] and i not in ret :
        ret.append(i)
  return ret



  #return [i for i in indices if connections_array[i] == m]
