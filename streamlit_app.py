import streamlit as st
import pandas as pd


st.title('🤖 Tood')

st.info("I'm Todd")

df = pd.read_csv('penguins_cleaned.csv')
df
