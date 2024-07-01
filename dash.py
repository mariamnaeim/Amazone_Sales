import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import re #Regular Expressions
import string #importing string functions
import warnings
import plotly.express as px
import datetime as dt
import warnings
import plotly.graph_objects as go
df = pd.read_csv('Amazon Sale Report.csv',index_col = 'index')
pd.set_option('display.max_columns',None)
st.sidebar.header(" Amazone  sales  report ")
st.sidebar.image("AM.jpeg")
st.sidebar.write("This dataset provides detailed insights into Amazon sales data")
st.sidebar.write("")
st.sidebar.markdown("Made with  :heart_eyes: by Eng. [Mariam Naeim ](https://www.linkedin.com/in/mariam-naeim-a8a02821a)")
df.drop_duplicates('Order ID',inplace=True)
df=df.drop(['fulfilled-by','Unnamed: 22','promotion-ids'], axis=1)
df=df.dropna()
df['Size'] = df['Size'].astype('category')
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
def format_large_number(number):
    suffixes = ["", "K", "M", "B", "T"]  # Suffixes for thousands, millions, billions, etc.
    for suffix in suffixes:
        if abs(number) < 1000:
            return f"{number:.1f}{suffix}"
        number /= 1000
    return f"{number:.1f}T"  # If the number is very large
sales=format_large_number(df['Amount'].sum().round(1))
Orders=format_large_number(df['Order ID'].count().round(1))
Quantities=format_large_number(df['Qty'].sum().round(1))
print(Quantities)
a1,a2,a3,a4,a5=st.columns(5)
a1.metric("Total Sales",sales)
a3.metric("Total Orders",Orders)
a5.metric("Total Quantities",Quantities)
st.subheader("Sales Over Time")
data = df.groupby('Date', as_index=False)['Amount'].count().head(10)
a1=st.plotly_chart( px.line(data, x='Date', y='Amount'))
df['month'] = df['Date'].dt.month
data = df.groupby('month', as_index=False)['Order ID'].count().head(10)
l = data['month']
sizes = data['Order ID']
st.subheader("Distribution of Sales by Months")
c1,c2,c3=st.columns((5,5,10))
c1.plotly_chart(px.pie(df, values=sizes, names=l,color=data['month']))
c2.plotly_chart(px.bar(df, x=l, y=sizes,color=data['month']))
# Example: Creating a bar chart
data2 = df.groupby(['month', 'Category']).size().reset_index(name='count').reset_index(drop=True)
df_pivot =data2.pivot(index='month', columns='Category', values='count')
fig = px.bar(df_pivot, x=df_pivot.index, y=df_pivot.columns, 
            )
fig.update_layout(xaxis_title='Month', yaxis_title='Count')
c3.plotly_chart(fig)


lables = df['Size'].value_counts().sort_values(ascending=False)
lables = pd.DataFrame(lables)
lables=lables.reset_index()
lables.columns = ['size','count']
st.subheader("DEMAND OF CLOTHES")
a1,a2,a3=st.columns((3,4,6))
a1.plotly_chart(px.pie(lables, values=lables['count'], names=lables['size']))
a2.plotly_chart(px.bar(lables, x=lables['size'], y=lables['count']),use_container_width=True)
data2 = df.groupby(['month', 'Category']).size().reset_index(name='count').reset_index(drop=True)
fig1 = px.bar(data2, x='Category', y='count', color='Category', 
             labels={'count':'Number of Occurrences'})
a3.plotly_chart(fig1)
