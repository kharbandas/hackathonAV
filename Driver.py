import tkinter as tk
import numpy as np
import pandas as pd
from Filter import *
import random
desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',10)

pd.set_option('display.max_rows', 11)


restaurants = pd.read_excel('Restaurant Filtered Sheet.xlsx')
restaurants['original_idx'] = [x for x in range(len(restaurants))]
shelters = pd.read_excel('Shelter Filtered Info.xlsx')



connections = np.zeros([len(shelters), len(restaurants)])

for i in range(len(connections)):
    connections[i] = random.choices([i for i in range(24)], weights = [1/i**1.25 for i in range(1,25)], k = len(restaurants))
connections[55][48] = 28
def clicked():
    clear()
    shelt = shelterNum.get()
    rad = radius.get()
    mealCt = meals.get()
    shelf_life = sLife.get()
    foodType = cuisine.get()

    r = restaurants
    if len(shelt) == 0:
        print("Please Enter a Shelter First.")
        return
    if len(rad) != 0:
        r = filterDistance(restaurants.latitude[int(shelt)], restaurants.longitude[int(shelt)], r, float(rad))
    if len(shelf_life) != 0:
        r = filterShelfLife(int(shelf_life), r)
    if len(mealCt) != 0:
        r = filterNumberOfMeals(int(mealCt), r)
    if len(foodType) != 0:
        r = filterCuisine(foodType, r)

    preference = sheltersPreference(r, int(shelt), connections)
    print("There are", len(r), "restaurants that match your inputted filters. They are shown below")
    r = r.drop(columns=['original_idx'])
    r = r.rename(columns = {'DistanceFromShelter': 'distanceFromShelter(mi)'})
    print(r, '\n')
    if len(preference) == 3:
        print("We recommend you choose to recieve food from", restaurants.name[preference[0]],
              "because they have donated", int(connections[int(shelt)][preference[0]]),
              "times to you. That \nis more than any other restaurant that matches the given filters. The Next best options are",
              restaurants.name[preference[1]], "\nand", restaurants.name[preference[2]], "with",
              int(connections[int(shelt)][preference[1]]), "and", int(connections[int(shelt)][preference[2]]),
              "previous donations with you.")
    elif len(preference) == 2:
        print("We recommend you choose to recieve food from", restaurants.name[preference[0]],
              "because they have donated", int(connections[int(shelt)][preference[0]]),
              "times to you. That \nis more than any other restaurant that matches the given filters.The Next best option is",
              restaurants.name[preference[1]], "\nwith",
              int(connections[int(shelt)][preference[1]]),"previous donations with you.")
    elif len(preference) == 1:
        print("We recommend you choose to recieve food from", restaurants.name[preference[0]],
              "because they have donated", int(connections[int(shelt)][preference[0]]),
              "times to you. That \nis more than any other restaurant that matches the given filters.")


def GUI():

    global rad1, rad2, rad3, rad4, rad5, shelterNum, radius, meals, sLife, cuisine

    window = tk.Tk()
    window.title("A2B")
    shelterNum = tk.StringVar()
    radius = tk.StringVar()
    meals = tk.StringVar()
    sLife = tk.StringVar()
    cuisine = tk.StringVar()

    shelterPrompt = tk.Label(window, text='Enter Shelter Number', font=('Times', 15, 'bold'))
    rad1 = tk.Entry(window, textvariable= shelterNum)
    radiusPrompt = tk.Label(window, text='Enter Radius (miles)', font=('Times', 15, 'bold'))
    rad2 = tk.Entry(window, textvariable= radius)
    mealsPrompt = tk.Label(window, text='Enter Minimum Meals', font=('Times', 15, 'bold'))
    rad3 = tk.Entry(window, textvariable= meals)
    sLifePrompt = tk.Label(window, text='Enter Max Shelf Life (days)', font=('Times', 15, 'bold'))
    rad4 = tk.Entry(window, textvariable= sLife)
    cuisinePrompt = tk.Label(window, text='Enter Cuisine Preference', font=('Times', 15, 'bold'))
    rad5 = tk.Entry(window, textvariable= cuisine)

    #Text boxes
    shelterPrompt.grid(column = 0, row = 0)
    rad1.grid(column=1, row=0)
    radiusPrompt.grid(column =0, row = 1)
    rad2.grid(column=1, row=1)
    mealsPrompt.grid(column=0, row=2)
    rad3.grid(column=1, row=2)
    sLifePrompt.grid(column =0, row = 3)
    rad4.grid(column=1, row=3)
    cuisinePrompt.grid(column=0, row=4)
    rad5.grid(column=1, row=4)

    #Submit and quit button
    button1 = tk.Button(window, text="Filter", command=clicked)
    button2 = tk.Button(window, text="Quit", command=window.destroy)
    button1.grid(column=6, row=0)
    button2.grid(column=6, row=1)

    window.mainloop()


shelterNum, radius, numMeals, shelfLife, cuisine = None, None, None, None, None
GUI()