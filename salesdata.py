#!/usr/bin/env python
# coding: utf-8

# In[103]:


#Importing libraries


# In[ ]:





# In[104]:


pip install missingno


# In[105]:


import pandas as pd
import numpy as ny
import seaborn as sns
import missingno as msno
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings('ignore')


# In[106]:


df = pd.read_csv(r"C:\Users\Adithya\Downloads\superstore_final_dataset (1).csv" , encoding ='latin1')


# # Data Investigation

# In[107]:


df.shape


# In[108]:


df.head()


# # more info of dataset

# In[109]:


df.info()


# # descriptive statistical

# In[110]:


df.describe()


# # Missing Values

# In[111]:


df.isnull().sum()


# In[112]:


#Check for white spaces


# In[113]:


df.columns


# # Data Cleaning

# In[114]:


df.head(2)


# In[115]:


df = df.drop(columns=['Row_ID','Postal_Code'], axis = 1)


# In[116]:


df.head(2)


# # missing values

# In[117]:


df.isnull().sum()


# # Visualising missingness

# In[118]:


msno.bar(df)


# # info on dataset

# In[119]:


df.info()


# In[120]:


df.head(2)


# # change date column to appropriate data type

# In[121]:


df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d/%m/%Y')
df['Ship_Date'] = pd.to_datetime(df['Ship_Date'], format='%d/%m/%Y')


# # confriming change

# In[122]:


df.info()


# # Extract numerical columns

# In[123]:


num_cols = df.select_dtypes(include = ['int','float'])


# # Result    

# In[124]:


num_cols.head()


# # Extracting categorical columns
# 

# In[125]:


cat_cols = df.select_dtypes(include =['object','category'])


# # Result

# In[126]:


cat_cols.head()


# # Data Validation
# 

# In[127]:


cat_cols.value_counts()


# In[128]:


cat_cols['Category'].unique()


# In[129]:


cat_cols['Sub_Category'].value_counts()


# In[130]:


cat_cols['Product_Name'].unique()


# In[131]:


#Dta validation for numerical columns


# In[132]:


num_cols['Sales'].value_counts()


# # Exploratory Data Analysis

# ### univariant eda

# In[133]:


#droping orderid and customer id
cat_cols = cat_cols.drop(columns =['Order_ID','Customer_ID','Product_ID'], axis = 1)


# In[134]:


#confriming result
cat_cols


# In[135]:


#combine numerical and categorical columns


# In[136]:


df1 = pd.concat([num_cols,cat_cols], axis=1)


# # Result

# In[137]:


df1.head()


# ### univariant eda

# In[138]:


cat_cols.info()


# In[140]:


cat_cols['Product_Name'].unique()


# In[147]:


# create a bar chart for ship mode

#count of ship_mode
count_ship_mode = cat_cols['Ship_Mode'].value_counts()

#setting figure size
plt.figure(figsize =(6,4))
count_ship_mode.plot(kind='bar',color='blue', edgecolor='yellow')

#cutomie bar chart
plt.title('Count of ship mode')
plt.xlabel('ship mode')
plt.ylabel('count of ship mode')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# # Writing a story and giving business recomendation

# From the analysis the company operates in a three different shipping mode, which are the standard class, ssecond class, first class, same day . The standard mode of shipping has the highest count of ship mode followed by seccond class with the same day has the lowest . From this analysis we can understand customer prefer standard shipping process compared to the othe shipping mode. The reason is that standard shipping mode offer cheaper rate compared to other shipping modes.
# 
# 
# --Business recomendation
# -The price of other shipping modes should be revised to attract more customer
# -Promo programs can be used to entice customers that make use of shipping modes aside the standard class
# -Further analysis should be made to understand the difference between the delivery for all shipping modes , that way we can determine that customer actually get the value for their money they opt for other shippping modes aside from the the standard shipping.

# In[148]:


# create a bar chart for Segment

#count of Shipmode
count_of_Segment = cat_cols['Segment'].value_counts()

#setting figure size
plt.figure(figsize =(6,4))
count_of_Segment.plot(kind='bar',color='blue', edgecolor='yellow')

#cutomie bar chart
plt.title('Count of Segment')
plt.xlabel('Segment')
plt.ylabel('count of Segment')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# # Writing a story and giving business recommendations

# This analysis shows consumer segment has highest number of sales orders , followed by the corporate,then home office. This indicates 
# that the business serves a predominantly consumer base with most of their transaction coming from business clients. 
# 
# Business Recommendation
# --Since most of the orders comes from consumers , we should ensure the buying experience is seemless. 
# Product availability should be optimized , including the pricing and conssumer support.
# --The lower volume of the other segmants suggest a room for growth. We should consider targeted outreach or tailored offerings 
# to increase their engagement.
# --Segmant based marketing should also be considered.
# 

# In[151]:


#Bivariate Exploratory Analysis
df1.head(2)


# In[156]:


df1.info()


# In[160]:


# Segment by sales 

# Grouping sales by segment 
sales_segment = df1.groupby('Segment')['Sales'].sum().reset_index()

#figure of bar chart 

plt.figure(figsize=(7,6))
plt.bar(sales_segment['Segment'], sales_segment ['Sales'], color='skyblue')
plt.title('Total sales by segment')
plt.xlabel('Segment')
plt.ylabel('Total sales')
plt.tight_layout()
plt.show()


# In[161]:


df1['Region'].unique()


# In[162]:


# region with the highest sales 

# Grouping sales by region 
sales_region = df1.groupby('Region')['Sales'].sum().reset_index()

#figure of bar chart 

plt.figure(figsize=(7,6))
plt.bar(sales_region['Region'], sales_region ['Sales'], color='skyblue')
plt.title('Total sales by region')
plt.xlabel('Region')
plt.ylabel('Total sales')
plt.tight_layout()
plt.show()


# # Story for analysis

# From the analysis we can see central region has highest sales followed by east,south and west region.

# # Business Recomendation

# In[ ]:


--A/B testing campaign should be using for underoerforming regions to determine which ad campaign performs better in 
improving sales.
--The marketing strategy used for the west should be studied for underperforming regions.


# # Multivariant Analysis

# In[167]:


# sales by segment and shipping mode across regions

grouped = df1.groupby(['Region','Segment','Ship_Mode'])['Sales'].sum().reset_index()

grouped['Segment_Ship_Mode'] =grouped['Segment'] + '-' + grouped['Ship_Mode']

pivot_df = grouped.pivot(index = 'Region', columns = 'Segment_Ship_Mode', values = 'Sales')

pivot_df.plot(kind = 'bar', stacked=True , figsize=(6,8))
plt.title('Sale by region and ship_mode')
plt.xlabel('Region')
plt.ylabel('Sales')
plt.legend(title = 'Segment - Ship Mode' , bbox_to_anchor=(1.05,1), loc='upper left')
plt.tight_layout()
plt.show()


# The west region leads all other region exceeding 700k, driven mainly by consumer and corporations using the standard shipping class. The
# follows south falls slowly 
# Across all standard shipping mode dominates . This shows consumers preference for affordablity over speed 

# # Business Recomendation

# -Premium shoppind should be promoted through incentive and bundle offer.
# -Weak demands should be investigated and targeted promotins should be introduced.

# In[ ]:




