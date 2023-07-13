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
st.title("Animal Planet Data")

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

diets = animal_data['Diet']

diet_new = []

for diet in diets:
  if type(diet) == type(0.0):
    diet_new.append(np.nan)
    continue

  diet_new.append(diet.split(",")[0])

animal_data["diet singular"] = diet_new

st.write(animal_data.head())

HW_data = animal_data[['avg_heights', 'avg_weights', "Order"]]
HW_data.dropna(inplace=True)

fig = px.scatter(
  HW_data,
  x="avg_weights",
  y="avg_heights",
  color="Order",
)
fig.update_layout(title="How Animal Orders Relate to Their Height and Weight",
                  xaxis_title='Average Weight',
                  yaxis_title='Average Height',
                  xaxis=dict(range=[0, 1000]),
                  yaxis=dict(range=[0, 3]))
st.write(fig)

st.markdown(
  "In many animals, height increases with weight. Animals in different orders follow different trends in both their heights and weights. Like how the Gruiformes are all tall and light due to them sharing a similar charateristic of being birds and crane-like. "
)
st.markdown(
  "Gruiformes (an order of crane-like birds) - mostly tall and not very heavy")
st.markdown(
  "Artiodactyla (even toed ungulates like pigs) - tend to be heavier and height grows little compared to weight growth --> exception very tall (giraffe)"
)
st.markdown(
  "Proboscidea (only living family left, elephants) - very heavy and not very tall "
)
st.markdown(
  "Perissodactyla (odd toed ungulates like horses) - medium heavy and not very tall, clustered around 200 - 300 kg and 0.8 - 1.2 m --> exception very heavy (rhino) "
)
st.markdown(
  "Carnivora (primarily carnivore mammals) - not tall or overly heavy, kinda random "
)
st.markdown(
  "Diprotodontia (marsupials) - pretty light and mostly short but some are taller "
)
st.markdown("Rodentia (rodents) - light and short ")

# You could make the x axis go from 0 to 1000
# Maybe change the order of these paragraphs
# In your description, the height of the animals increases with the weight, so make note of that

LSW_data = animal_data[['avg_life_spans', 'avg_weights', 'Class']]
LSW_data.dropna(inplace=True)
fig1 = px.scatter(LSW_data, x='avg_life_spans', y='avg_weights', color="Class")
fig1.update_layout(
  xaxis=dict(range=[0, 80]), yaxis=dict(range=[0, 350])
)  #One small thing, you might want to change the bounds on your y-axis.
fig1.update_layout(title='Weight vs Average Life Span Based On Animal Class',
                   xaxis_title='Average Life Span',
                   yaxis_title='Weight')
st.write(fig1)
st.markdown(
  "For the animals in the study, we can see that as their weight and average life span increase together. This correlation can be due to smaller animals having a higher risk of being eaten by predators and larger animals have a slower metabolism and a lower body temperature, which helps them live longer. Having a lower metabolism and body temperature can help animals conserve energy and minimize heat loss in cold and unfavorable environments. This can be beneficial for survival when food is scarce."
)

# Might want to change it to saying weight and average life span increase together

fig2 = px.scatter(animal_data,
                  x='avg_top_speeds',
                  y='avg_weights',
                  color="Class")
fig2.update_layout(xaxis=dict(range=[0, 180]), yaxis=dict(range=[0, 40000]))

fig2.update_layout(title='Relationship between Top Speed and Weight',
                   xaxis_title='Top Speed',
                   yaxis_title='Weight')

st.write(fig2)

fig2_1 = px.scatter(animal_data,
                    x='avg_top_speeds',
                    y='avg_weights',
                    color="Class")
fig2_1.update_layout(xaxis=dict(range=[0, 180]), yaxis=dict(range=[0, 200]))

fig2_1.update_layout(title='Relationship between Top Speed and Weight',
                     xaxis_title='Top Speed',
                     yaxis_title='Weight')

st.write(fig2_1)
st.markdown(
  "The scatterplots displayed above illustrate that animals with lower weights tend to occupy the central to lower range in terms of top speed. While some smaller animals have both low and high top speeds, there are very few larger animals that have high top speeds. Since only a small number of larger animals exhibit high top speeds, despite their greater weight, it suggests that factors other than weight play a significant role in determining the animals' speed capabilities. There are also trends indicating that as the weight of an animal increases, the top speed increases as well. For every weight class, there are always animals with lower top speeds."
)

# You could say something about the weight increasing as the top speed increases. Maybe you could also mention that there are always animals with low top speeds for every weight class

# you could simply not add the x_axis and y_axis arguments #yeah but how do i add the text #Do you mean the title? Yeah thats already in the title argument, since your pie chart doesnt have an x and y axis you dont need to add x and y axis arguments

b = animal_data[animal_data["Genus"] == "Canis"]
diet_counts = b["Diet"].value_counts()
diet_counts_df = pd.DataFrame({
  "Diet": diet_counts.index,
  "Count": diet_counts.values
})
fig4 = px.pie(diet_counts_df, values='Count', names='Diet')
fig4.update_layout(title="The Diet of Wild Canines")

#b["diet singular"].value_counts().plot.pie()
st.write(fig4)
st.markdown(
  "This pie chart is visually discribing what all of the canines in the wild's diet consists of. Being a canivore ment you had to hunt for food, meaning this isn't the best choice for canines. Being a scavenger, though, ment there was way more food avalible to canines, because they could fight off the other scavengers due to their size and strength. Lastly, being an omnivore ment you could eat pretty much anything, this ment the two best choices to choose would be a scavenger and an omnivore."
)

#aniaml me of the li

# fig3, ax = plt.figure(figsize=(12,4))
# sns.histplot(animal_data, x = 'avg_life_spans', hue = 'class')
# plt.title title ("Average Life span base on species and class")

fig3 = px.histogram(animal_data['avg_life_spans'], nbins=40)
fig3.update_layout(
  title='Frequency of different lifespans',
  xaxis_title='Lifespan',
  yaxis_title='Frequency',
)
st.write(fig3)
st.text(
  "According to a recent study, most animals struggle to survive above the age of 15 to 20 years. With the exception of a few outliers, birds likewise experience difficulties at that stage."
)

# Maybe add something about how the data reflects the findings of this study

#st.title("Different Orders and their diet groups")
FD_data = animal_data[['Order', 'diet singular']]
FD_data.dropna(inplace=True)

fig4 = px.scatter(FD_data, x="Order", y="diet singular")
fig4.update_layout(title="Different Diets in Orders", yaxis_title="Diet")
st.write(fig4)
st.markdown("Carnivores are the most common type of diet across the different orders. After that, it is herbivores and omnivores. W") #this paragraph has no organization :) dont mind it

# Add the title to your graph instead of doing it in streamlit
# Try to use more of the graph than just the carnivora column, maybe note that carnivores are the most common of all diets

diets = animal_data['Diet']
diet_new = []
for diet in diets:
  if type(diet) == type(0.0):
    diet_new.append(np.nan)
    continue

  diet_new.append(diet.split(",")[0])

animal_data["diet singular"] = diet_new

#st.title("Average Life Spans Based on Diet")

diet_counts = animal_data["diet singular"].value_counts()
diet_counts_df = pd.DataFrame({
  "Diet": diet_counts.index,
  "Count": diet_counts.values
})
fig5 = px.bar(diet_counts_df,
              x="Diet",
              y="Count",
              color="Diet",
              hover_data=["Count"])
fig5.update_layout(title="Average Life Spans Based on Diet")
#fig5 = animal_data.head(15)["diet singular"].value_counts().plot.bar(y="avg_life_spans")
st.write(fig5)

st.markdown(
  "The animals in the data set are classified into various dietary categories. (Carnivore, Herbivore, Omnivore, Scavenger) Looking at the data from the graph we can see the animals with a predominantly carnivorous diet typically live longer than their counterparts."
)

#Using this information in the future we can judge life expectancy at early ages in an animals life.
# You might want to edit that a bit, since it is not related to the graph
