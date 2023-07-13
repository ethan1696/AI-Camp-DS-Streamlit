#import libraries
import streamlit as st
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

#look for more information here https://docs.streamlit.io/library/cheatsheet

#adding title
st.title("My Title")

#adding discription to your website
st.text('asdf')

animal_data = pd.read_csv('animals_info.csv')


def clean_data(col_name, new_col_name, unit_dict):
  global animal_data
  vals = animal_data[col_name]
  avg_vals = []
  for v_str in vals:
    try:
      #print(v_str)
      if type(v_str) == type(0.0):
        avg_vals.append(v_str)
        continue

      if len(v_str.split(" ")) != 2:
        avg_vals.append(np.nan)
        continue

      nums = v_str.split(" ")[0]
      units = v_str.split(" ")[1]

      if len(nums.split("-")) != 2:
        if len(nums.split("-")) == 1:
          avg = float(nums.split("-")[0]) * unit_dict[units]
          avg_vals.append(avg)
          continue
        avg_vals.append(np.nan)
        continue

      num1 = float(nums.split("-")[0])
      num2 = float(nums.split("-")[1])

      if units not in unit_dict.keys():
        avg_vals.append(np.nan)
        continue

      avg = ((num1 + num2) / 2) * unit_dict[units]

      avg_vals.append(avg)
    except Exception as e:
      avg_vals.append(np.nan)
      continue

  animal_data[new_col_name] = avg_vals


clean_data("Weight", "avg_weights", {'g': 0.001, 'kg': 1.0, 't': 1016.04691})
clean_data("Height", "avg_heights", {'cm': 0.01, 'm': 1.0})
clean_data("Length", "avg_lengths", {'cm': 0.01, 'm': 1.0, 'mm': 0.001})
clean_data("Top speed", "avg_top_speeds", {'km/h': 1})
clean_data("Life span", "avg_life_spans", {'yrs': 1, 'years': 1})

st.write(animal_data.head())

HW_data = animal_data[['avg_heights', 'avg_weights', "Order"]]
HW_data.dropna(inplace=True)

fig = px.scatter(
  HW_data,
  x="avg_weights",
  y="avg_heights",
  color="Order",
)
fig.update_layout(xaxis=dict(range=[0, 3500]), yaxis=dict(range=[0, 5]))
st.write(fig)


L_data = animal_data[['avg_life_spans', 'avg_lengths']]
L_data.dropna(inplace=True)
fig1 = px.scatter(L_data, x='avg_life_spans', y='avg_lengths')
fig1.update_layout(xaxis=dict(range=[0, 40]),yaxis=dict(range=[-50, 500]))
st.write(fig1)

