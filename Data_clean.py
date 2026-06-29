# %%
import pandas as pd
import numpy as np

# %%
df=pd.read_excel('diabetic_data.xlsx')
print("Shape: ",df.shape)
print("Columns: ",df.columns.to_list())
print(df.describe())

# %%
#Replace missing values "?" with na
df.replace('?',np.nan, inplace=True)
missing=df.isnull().sum()
print(missing[missing>0])
#df.to_excel('diabetic_data.xlsx', index=False)

#%%
#Dropping column with more than 40% missing values
missing_val=df.isnull().mean()
df=df[df.columns[missing_val<0.4]]
print("Updated Shape",df.shape)
print("Columns dropped: ",50-df.shape[1])

# %%
#Remove duplicate patiend ID
print("Before removing duplicates: ",len(df))
print("Duplicated rowS: ",df.duplicated(subset="patient_nbr").sum())
df.drop_duplicates(subset="patient_nbr", inplace=True, keep="first")
print("After removing duplicates: ",len(df))

# %%
#Fix Re_admited columns with 0(No) and 1(yes) as a new column
df['readmitted_30']=df["readmitted"].apply(lambda x:1 if x== '<30' else 0)
print("Count of less than 30 days readmitted patients: ",df["readmitted_30"].value_counts() )
print("Columns: ",df.columns.to_list())

# %%
#Fixing Age columns to proper category label as new columns
df['age_num']=df['age'].str.extract(r'\[(\d+)')[0].astype(float )
df['age_label']=pd.cut(df['age_num'],bins=[0,30,50,70,100],labels=['Young (0-30)', 'Middle (31-50)', 'Senior (51-70)', 'Elderly (71-100)'])
print(df[['age', 'age_num', 'age_label']].head(10))

# %%
# List of medication columns
med_cols = ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide',
            'glimepiride', 'glipizide', 'glyburide', 'insulin']

# Count how many were changed (either Up or Down)
df['med_changes'] = df[med_cols].apply(
    lambda row: (row == 'Up').sum() + (row == 'Down').sum(), axis=1
)

print(df['med_changes'].describe())   # see min, max, average

# %%
# Save clean file
df.to_excel('diabetic_data.xlsx', index=False)

# Confirm it saved
print('Saved! Rows:', len(df))
print('Columns:', df.columns.tolist())

# %%
#Connecting with mySQL
# %%
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:root@localhost/hospital_db"
)

print("Connection successful")

# %%
#Loading data to mySQl
df.to_sql(
    'readmissions',
    con=engine,
    if_exists='replace',
    index=False
)

print("Data loaded successfully!")
# %%
