# -*- coding: utf-8 -*-
"""Google Playstore Assignment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LJgkyTmwSFTRBm0XW-IowxjFWbwkl7p4

#WELCOME

##GOOGLE PLAYSTORE ASSESMENT

###1). Load the data file using pandas.
"""

import pandas as pd
import numpy as np

df = pd.read_csv("/content/googleplaystore.csv")
df

"""###2). Check for null values in the data. Get the number of null values for each column"""

null_values= df.isna().sum()
null_values

"""###3.) Drop records with nulls in any of the columns."""

clean = df.dropna(inplace= True)
clean
df

"""*WE COULD SEE SIGNIFICANT DROP IN NUMBER OF ROWS IN THE DATAFRAME AFTER
DROPPING NULL VALUES.* **FROM 10841 TO 9360**

###4) Variables seem to have incorrect type and inconsistent formatting. You need to fix them:

####4.1) Size column has sizes in Kb as well as Mb. To analyze, you’ll need to convert these to numeric.
"""

data=pd.DataFrame(df)
data

def process_size(size_str):
  size_str = str(size_str)
  if 'M' in size_str:
        # Remove 'MB' and convert to numeric, then multiply by 1000
        size_numeric = float(size_str.replace('M', 'K')) * 1000
        # Convert back to a string with 'KB'
        return size_numeric
  else:
        return size_str  # Keep as is

# Apply the function to the 'Size' column
df['Size'] = df['Size'].apply(process_size)

df

df['Size']

"""####4.2) Reviews is a numeric field that is loaded as a string field. Convert it to numeric (int/float)."""

df['Reviews'] = df['Reviews'].astype(int)

df

"""####4.3) Installs field is currently stored as string"""

df['Installs'] = df['Installs'].str.replace('+', '').str.replace(',', '')

# Step 2: Convert the cleaned strings to integers
df['Installs'] = df['Installs'].astype(int)
df

df['Price']= df['Price'].str.replace('$', '')
df['Price']= df['Price'].astype(float)
df

df

df['Size']

"""###5.) SANITY CHECKS

####5.1) Average rating should be between 1 and 5 as only these values are allowed on the play store. Drop the rows that have a value outside this range.
"""

df = df[(df['Rating'] >= 1) & (df['Rating'] <= 5)]
df

"""####5.2) Reviews should not be more than installs as only those who installed can review the app. If there are any such records, drop them."""

df = df[df['Reviews'] < df['Installs']]
df

"""####5.3) Performing univariate analysis: Boxplot for Price"""

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
sns.boxplot(data=df, y='Price')
plt.title('Boxplot of Price')
plt.ylabel('Price')
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
sns.boxplot(data=df, y='Reviews')
plt.title('Boxplot of Reviews')
plt.ylabel('Reviews')
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8,6))
sns.histplot(data=df, x= 'Rating', bins=30,kde=True)
plt.title('Histogram of Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')

"""###6.) Outlier treatment:

####6.1) Dropping Price that exceeds 200 and Visualizing it
"""

df=df[df['Price']<=200]
df

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
sns.boxplot(data=df, y='Price')
plt.title('Boxplot of Price')
plt.ylabel('Price')
plt.show()

"""####6.2) Checking the outlier by visualizing with the help of boxplot and eliminating the rows that are above the threashold values"""

a= max(df['Installs'])
a

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
sns.boxplot(data=df, y='Installs')
plt.title('Boxplot of Installs')
plt.ylabel('Installs')
plt.show()

df['Installs'] = df['Installs'].astype(int)

percentiles = [10, 25, 50, 70, 90, 95, 99]
install_percentiles = df['Installs'].quantile([p / 100 for p in percentiles])

threshold = 100000000  # For example, setting a threshold at 10 million installs

df = df[df['Installs'] <= threshold]

print(f'Percentiles: {install_percentiles}')
print(f'Threshold for Outliers: {threshold}')

df=df[df["Installs"]<=100000000]
df

"""###7.) Bivariate analysis:

####7.1) Make scatter plot/joinplot for Rating vs. Price

What pattern do you observe? Does rating increase with price?
"""

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))  # Set the size of the plot
sns.scatterplot(data=df, x='Price', y='Rating')
plt.title('Scatter Plot of Rating vs. Price')
plt.xlabel('Price')
plt.ylabel('Rating')

plt.show()

"""####7.2) Make scatter plot/joinplot for Rating vs. Size"""

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))  # Set the size of the plot
sns.scatterplot(data=df, x='Size', y='Rating')
plt.title('Scatter Plot of Size vs. Rating')
plt.xlabel('Size')
plt.ylabel('Rating')


plt.show()

import seaborn as sns
import matplotlib.pyplot as plt


plt.figure(figsize=(8, 6))  # Set the size of the plot
sns.scatterplot(data=df, x='Reviews', y='Rating')
plt.title('Scatter Plot of Rating vs. Reviews')
plt.xlabel('Reviews')
plt.ylabel('Rating')

plt.show()

"""####7.4) Make boxplot for Ratings vs. Category"""

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='Category', y='Rating')
plt.xticks(rotation=90)
plt.title('Boxplot of Ratings by Category')
plt.xlabel('Category')
plt.ylabel('Rating')

plt.show()

df

"""###8.) Data preprocessing

For the steps below, create a copy of the dataframe to make all the edits. Name it inp1.

####8.1) Apply log transformation (np.log1p) to Reviews and Installs.
"""

import pandas as pd
import numpy as np

inp1 = df.copy()

inp1['Reviews'] = pd.to_numeric(inp1['Reviews'], errors='coerce')
inp1['Installs'] = pd.to_numeric(inp1['Installs'], errors='coerce')

inp1['Reviews'] = np.log1p(inp1['Reviews'])
inp1['Installs'] = np.log1p(inp1['Installs'])

inp1

"""####8.2) Drop columns App, Last Updated, Current Ver, and Android Ver. These variables are not useful for our task."""

columns_to_drop = ['App', 'Last Updated', 'Current Ver', 'Android Ver','Size']
inp1 = inp1.drop(columns=columns_to_drop)

"""####8.3) Get dummy columns for Category, Genres, and Content Rating."""

inp1 = inp1.dropna(subset=['Type'])

import pandas as pd

inp2 = pd.get_dummies(inp1, columns=['Category', 'Genres', 'Content Rating','Type'])

inp2

"""###9.) Train test split  and apply 70-30 split. Name the new dataframes df_train and df_test."""

from sklearn.model_selection import train_test_split

# Split the DataFrame into training and test sets with a 70-30 split
df_train, df_test = train_test_split(inp2, test_size=0.3, random_state=42)

# The 'random_state' parameter ensures reproducibility of the split

import pandas as pd

# Create a new DataFrame with 10,000 rows and a single column filled with 0
new_data = pd.DataFrame({'target': [0] * 9206})

# Concatenate the new DataFrame with the original DataFrame
inp2 = pd.concat([inp2, new_data], axis=1)

import pandas as pd

# Create a new DataFrame with 10,000 rows and a single column filled with 0
new_data = pd.DataFrame({'target': [0] * 6444})

# Concatenate the new DataFrame with the original DataFrame
df_train = pd.concat([df_train, new_data], axis=1)

import pandas as pd

# Create a new DataFrame with 10,000 rows and a single column filled with 0
new_data = pd.DataFrame({'target': [0] * 2762})

# Concatenate the new DataFrame with the original DataFrame
df_test = pd.concat([df_test, new_data], axis=1)

"""###10.) Separate the dataframes into X_train, y_train, X_test, and y_test."""

target_column = 'target'

# Create X_train, y_train, X_test, and y_test
X_train = df_train.drop(columns=[target_column])
y_train = df_train[target_column]
X_test = df_test.drop(columns=[target_column])
y_test = df_test[target_column]

"""###11.) Model building - REGRESSION ANALYSIS"""

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.impute import SimpleImputer

# Create a linear regression model
model = LinearRegression()

# Impute missing values in your DataFrame for both X and y
imputer = SimpleImputer(strategy='mean')

X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

y_train_imputed = imputer.fit_transform(y_train.values.reshape(-1, 1)).ravel()
y_test_imputed = imputer.transform(y_test.values.reshape(-1, 1)).ravel()

# Fit the model on the training data with imputed values
model.fit(X_train_imputed, y_train_imputed)

# Predict on the training set
y_train_pred = model.predict(X_train_imputed)

# Calculate R2 on the training set
r2_train = r2_score(y_train_imputed, y_train_pred)
#print(f'R2 on the training set: {r2_train:.2f}')

# Predict on the test set with imputed values
y_test_pred = model.predict(X_test_imputed)

# Calculate R2 on the test set
r2_test = r2_score(y_test_imputed, y_test_pred)
print(f'R2 on the test set: {r2_test:.2f}')