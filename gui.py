import tkinter as tk
import numpy as np
import pandas as pd
from Filter import *
import customtkinter as ctk

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',10)

restaurants = pd.read_excel('Restaurant Filtered Sheet.xlsx')
restaurants['original_idx'] = [x for x in range(len(restaurants))]
shelters = pd.read_excel('Shelter Filtered Info.xlsx')

connections = my_array = np.zeros([len(shelters), len(restaurants)])
print(connections.shape)

def clicked():
    #print(f'clicked {shelterNum.get()}')
    shelt = shelterNum.get()

    #print(f'clicked {radius.get()}')
    rad = radius.get()

    #print(f'clicked {radius.get()}')
    mealCt = meals.get()

    #print(f'clicked {radius.get()}')
    shelf_life = sLife.get()
    foodType = cuisine.get()


    print(shelt, rad, mealCt, shelf_life)

    r1 = filterDistance(restaurants.latitude[int(shelt)], restaurants.longitude[int(shelt)], restaurants, int(rad))
    r2 = filterShelfLife(int(shelf_life), r1)
    r3 = filterNumberOfMeals(int(mealCt), r2)
    r4 = filterCuisine(foodType, r3)

    #rint(r1, '\n')
    #print(r2, '\n')
    #print(r3, '\n')
    print(r4, '\n')


def GUI():

    global rad1, rad2, rad3, rad4, rad5, shelterNum, radius, meals, sLife, cuisine

    window = tk.Tk()
    window.title("Select First Color")
    shelterNum = tk.StringVar()
    radius = tk.StringVar()
    meals = tk.StringVar()
    sLife = tk.StringVar()
    cuisine = tk.StringVar()

    shelterPrompt = tk.Label(window, text='Enter Shelter Number', font=('Times', 15, 'bold'))
    rad1 = tk.Entry(window, textvariable= shelterNum)
    radiusPrompt = tk.Label(window, text='Enter radius', font=('Times', 15, 'bold'))
    rad2 = tk.Entry(window, textvariable= radius)
    mealsPrompt = tk.Label(window, text='Enter Minimum Meals', font=('Times', 15, 'bold'))
    rad3 = tk.Entry(window, textvariable= meals)
    sLifePrompt = tk.Label(window, text='Enter Max Shelf Life', font=('Times', 15, 'bold'))
    rad4 = tk.Entry(window, textvariable= sLife)
    cuisinePrompt = tk.Label(window, text='Enter Cusine Preference', font=('Times', 15, 'bold'))
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
    button1 = tk.Button(window, text="Select", command=clicked)
    button2 = tk.Button(window, text="Quit", command=window.destroy)
    button1.grid(column=6, row=0)
    button2.grid(column=6, row=1)

    window.mainloop()


shelterNum, radius, numMeals, shelfLife, cuisine = None, None, None, None, None
GUI()

