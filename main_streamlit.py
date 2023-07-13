#import libraries
import streamlit as st
import pandas as pd
import warnings
import seaborn as sns
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

st.title("How Animal Orders Relate to Their Height and Weight")
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
st.text("Gruiformes (an order of crane-like birds) - mostly tall and not very heavy \nArtiodactyla (even toed ungulates like pigs) - tend to be heavier and height grows little compared to weight growth --> exception very tall (giraffe) \nProboscidea (only living family left, elephants) - very heavy and not very tall \nPerissodactyla (odd toed ungulates like horses) - medium heavy and not very tall, clustered around 200 - 300 kg and 0.8 - 1.2 m --> exception very heavy (rhino) \nCarnivora (primarily carnivore mammals) - not tall or overly heavy, kinda random \nDiprotodontia (marsupials) - pretty light and mostly short but some are taller \nRodentia (rodents) - light and short \nIn many animals, having heavier body results in them not being very tall. Many animals in specific orders follow trends in both their heights and weights. Like how the Gruiformes are all tall and light due to them sharing a similar charateristic of being birds and crane-like. ")


LSW_data = animal_data[['avg_life_spans', 'avg_weights', 'Class']]
LSW_data.dropna(inplace=True)
fig1 = px.scatter(LSW_data, x='avg_life_spans', y='avg_weights', color="Class")
fig1.update_layout(xaxis=dict(range=[5, 40]),yaxis=dict(range=[0, 350])) #One small thing, you might want to change the bounds on your y-axis. 
st.write(fig1)
st.text("For mammals, we can see that as their weight increase, most of the time the average life span also increase.This correlation can be due to smaller mammals having a higher risk of being eaten by predators and larger mammals have a lower metabolism and a lower body temperature, which helps them live longer.Having a lower metabolism and body temperature can help mammals conserve energy and minimize heat loss in cold and unfavorable environments. This can be beneficial for survival when food is scarce.")

fig2 = px.scatter(LSW_data, x='avg_top_speeds', y='avg_weights', color="Class")
fig2.update_layout(xaxis=dict(range=[0, 180]),yaxis=dict(range=[0, 70000]))

fig.update_layout(
    title='Relationship between Top Speed and Weight',
    xaxis_title='Top Speed',
    yaxis_title='Weight',
)

st.write(fig2)
st.text("The scatterplot displayed above illustrates that animals with lower weights tend to occupy the central to lower range in terms of top speed. While there are some lower-weight animals with low top speeds and high-top speeds, there are very few animals with higher weights with high top speeds.")

plt.title("The Diet of Wild Canines")
b = animal_data[animal_data["Genus"] == "Canis"]
HL_data = animal_data[["Diet", "Genus"]]
HL_data.dropna(inplace = True)
b["Diet"].value_counts().plot.pie()
st.set_label("Diet")
st.text("This pie chart is visually discribing what all of the canines in the wild's diet consists of. Being a canivore ment you had to hunt for food, meaning this isn't the best choice for canines. Being a scavenger, though, ment there was way more food avalible to canines, because they could fight off the other scavengers due to their size and strength. Lastly, being an omnivore ment you could eat pretty much anything, this ment the two best choices to choose were scavendry and omnivory.")

#aniaml me of the li


fig3, ax = plt.figure(figsize=(12,4))
sns.histplot(animal_data, x = 'avg_life_spans', hue = 'class')
# plt.title title ("Average Life span base on species and class")
st.pylot(fig3)
st.text("# According to a recent study, most animals struggle to survive above the age of 15 to 20 years. With the exception of a few outliers, birds likewise experience difficulties at that stage.")


FD_data = animal[['Order', 'diet singular']]
FD_data.dropna(inplace=True)

fig4 = px.scatter(FD_data, x="Order", y="diet singular")
st.write(fig4)
st.text("Although the Carnivora class is supposed to be composed of primarily carnivores, it also has other animals that are not carnivores. This is because of how their body is structured such as claws and skull shape. Most orders have carnivores except for a select few. ")



diets = animal_data['Diet']
diet_new = []
for diet in diets:
  if type(diet) == type(0.0):
    diet_new.append(np.nan)
    continue

  diet_new.append(diet.split(",")[0])

animal_data["diet singular"] = diet_new

st.title("Average Life Spans Based on Diet")
fig5 = animal_data.head(15)["diet singular"].value_counts().plot.bar(y="avg_life_spans")
st.write(fig5)
st.text("The animals in the data set are classified into various dietary categories. (Carnivore, Herbivore, Omnivore, Scavenger) Looking at the data from the graph we can see the ")
