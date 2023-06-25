#!/usr/bin/env python
# coding: utf-8

# Learning to use Pandas for Data Analysis

# In[1]:


# Import the pandas package
import pandas as pd


# In[2]:


## Read the customer table and assign it to 'customer' object
customer = pd.read_csv("customer.csv")


# ### Exploring the data
# 
# 
# Exploring using .head() and .tail()

# In[3]:


# call the customer table
customer.head()


# In[4]:


customer.tail()


# In[5]:


# examine the tail
customer.sample(5)


# In[6]:


# examine column names
customer.columns


# In[7]:


# examine the data types
customer.dtypes


# In[8]:


# import the payment table and repeat the above
payment = pd.read_csv("payment.csv")
payment.head()


# In[9]:


# descriptive stats on the customer and payment tables
customer.describe()


# Why are only certain columns described?
# Ans - Because the method by default provides descriptive statistics for numerical columns. It calculates statistics such as count, mean, standard deviation, minimum, quartiles, and maximum for numerical data.
# 
# 
# What happens if we try and call describe on categorical columns?
# Ans - If you try to call describe() on categorical columns, it will provide descriptive statistics specific to categorical data. It will include the count of non-null values, the number of unique categories, the most frequent category, and the frequency of the most frequent category.

# 
# ### Selecting Columns
# 
# 
# A dataframe is a collection of `series`(columns), a `series` is a `numpy array` with an index
# 

# In[10]:


# select a column as a series
customer['first_name']


# In[11]:


# select a column as a dataframe
customer[['first_name']]


# In[12]:


# select multiple columns
customer[['first_name', 'last_name']]


# In[13]:


# describe first and last name columns
customer[['first_name', 'last_name']].describe()


# Describe a categorical column

# In[14]:


# look at unique values for store_id
customer['store_id'].unique()


# In[15]:


# using value counts
customer['store_id'].value_counts()


# ### Plotting
# 
# Lets find out how frequent different amounts are paid.

# In[16]:


# call the payment table
payment = pd.read_csv('payment.csv')


# In[17]:


payment.hist(column = 'amount');


# In[18]:


# pandas method of histogram for amount in payment table
payment['amount'].hist(grid = False, bins = 12)


# In[19]:


# save the plot
plot = payment['amount'].hist(grid = False, bins = 12)
plot.set_title('amount of payment')
plot.get_figure().savefig('output.pdf', format='pdf')


# ### Sorting
# 

# In[20]:


# sort by customers by name
customer.sort_values(by = 'first_name').head()


# In[21]:


# sort by store_id and address_id
customer.sort_values(by = ['store_id', 'address_id'], ascending = False).head()


# This does not alter the values in the dataframe, in order to do so we must reassign or use a flag for inplace, Re-assigning is the preferred method

# In[22]:


# using inplace
customer.sort_values(by = 'first_name', inplace=True)
customer.head()


# In[23]:


# reset by index
customer.sort_index(inplace=True)
customer.head()


# In[24]:


# using reassignment
customer = customer.sort_values(by='first_name')


# In[25]:


## Reset the index
customer.reset_index().head()


# This creates a new column, order to do so without we drop the previous index

# In[26]:


## Reset the index in place and drop previous index column
customer = customer.reset_index(drop=True)
customer.head()


# 
# ### Filtering Rows
# 
# 
# To look at subsets of the data, we will  filter or group required sets. 

# In[27]:


# Filter the table to just the store that we are interested in, store number 2
customer[customer['store_id'] == 2]


# ## Explanation of whats going on in this operation

# In[28]:


# Creating a Boolean mask to filter rows

store_id_filter = customer['store_id'] == 2
store_id_filter


# In[29]:


# Applying boolean mask to the dataframe
customer[store_id_filter]


# In[30]:


# create a boolean mask where first name is Terry
# experiment with case
first_name_filter = customer['first_name'].str.upper() == 'TERRY'
first_name_filter


# In[31]:


# apply both filters
customer[store_id_filter & first_name_filter]


# 
# # Aggregation

# In[32]:


# total amount per customer
payment.groupby('customer_id').sum().head()


# In[33]:


payment[['customer_id', 'amount']].groupby('customer_id').sum()


# In[34]:


# agg with renaming the column
payment[['customer_id', 'amount']].groupby('customer_id').agg(total_amount = ('amount', 'sum'))


# Sort customers by descending total amount

# In[35]:


# do again with renaming to total_amount
payment[['customer_id', 'amount']].groupby('customer_id'
                                          ).agg(total_amount=('amount','sum')
                                               ).sort_values(by='total_amount', ascending=False)


# In[36]:


# Find the staff member with the highest average sale
payment[['staff_id', 'amount']].groupby('staff_id'
                                       ).agg(avg_sale = ('amount','mean')
                                            ).sort_values(by='avg_sale', ascending=False)


# In[37]:


avg_sales_per_staff = payment[['staff_id', 'amount']].groupby('staff_id'
                                                            ).agg(avg_sale = ('amount','mean')
                                                                  ).sort_values(by='avg_sale', ascending=False)


# In[38]:


# Save aggregation to csv 
# do again with index=False
avg_sales_per_staff.to_csv('avg_sales_per_staff.csv', index=False)


# In[39]:


# Save to Excel
avg_sales_per_staff.to_excel('customer.xlsx', sheet_name='payment_details')


# ### Joins
# 
# 

# In[40]:


## Merge the DataFrames using the .merge() method
pd.merge(left = customer,
         right = payment,
         how = 'left',
         left_on = 'customer_id',
         right_on = 'customer_id'
        ).head()

