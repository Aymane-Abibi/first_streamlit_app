import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('New healthy diner')

streamlit.header('Breakfast menu')
   
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)


def get_fruity_advice(fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
   else:
      fruityvice_advice = get_fruity_advice(fruit_choice)
      streamlit.dataframe(fruityvice_advice)
except URLError as e:
   stramlit.error()


def load_fruit_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from fruit_load_list")
      return my_cur.fetchall()

if streamlit.button('Get fruit list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = load_fruit_list()
   streamlit.dataframe(my_data_rows)

def insert_to_list(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute(f'insert into fruit_load_list values {new_fruit}')
      return "Thanks for adding" + new_fruit
   
fruit_added = streamlit.text_input("What fruits you want to add ?")
if streamlit.button('Add to fruit list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   ret_func = insert_to_list(fruit_added)
   streamlit.write(ret_func)
   

#my_cur.execute("insert into fruit_load_list values ")

