import pandas as pd

# read all prudcts data (import csv file)
df_orignal = pd.read_csv('prods.csv')

df = df_orignal.copy()

# fill NaN values with blank
df = df.fillna("")


# combine and clean columns for types selection 
df['combined_GB'] = df['Ingredients'] +" "+df['product_title']
df['combined_GB'] = df['combined_GB'].str.lower().str.replace('n/a', '').str.replace('<p>', '').str.replace('[^a-zA-Z0-9 ]', '')

# combine and clean columns for sub types selection
df['combined_HIB'] = df['Description']+" "+df['Reccomended Usage']+" "+df['product_title']
df['combined_HIB'] = df['combined_HIB'].str.lower().str.replace('n/a', '').str.replace('<p>', '').str.replace('[^a-zA-Z0-9 ]', '')

# combine and clean columns for sub types selection
df['combined_G'] = df['Ingredients']
df['combined_G'] = df['combined_G'].str.lower().str.replace('n/a', '').str.replace('<p>', '').str.replace('[^a-zA-Z0-9 ]', '')



# read types mapping and clean text
df_types = pd.read_csv('types.csv')
# fill NaN values
df_types = df_types.fillna("")


# data cleaning (replace all capital letters with lower case and replace all symbols multiple blanks with a single blank.

df_types['B'] = df_types['B'].str.replace('\n', ',').str.lower().str.replace('[^a-zA-Z0-9,\- ]', '')
df_types['C'] = df_types['C'].str.replace('\n', ',').str.lower().str.replace('[^a-zA-Z0-9,\- ]', '')
df_types['D'] = df_types['D'].str.replace('\n', ',').str.lower().str.replace('[^a-zA-Z0-9,\- ]', '')
df_types['E'] = df_types['E'].str.replace('\n', ',').str.lower().str.replace('[^a-zA-Z0-9,\- ]', '')


# set up four conditions to check if the string was included, then append the tag to the product

condition_one = {}
for _, row_i in df.iterrows():
    idx = row_i["NO."]
    condition_one[idx] = {}
    for _, row_j in df_types.iterrows():
        kwrds = row_j['B'].split(",")
        for k in kwrds:
            k = k.strip()
            if k != '' and k in row_i.combined_GB:
                condition_one[idx].setdefault(row_j['TAG'], []).append(k)
                # break
        

condition_two = {}
for _, row_i in df.iterrows():
    idx = row_i["NO."]
    condition_two[idx] = {}
    for _, row_j in df_types.iterrows():
        kwrds = row_j['D'].split(",")
        for k in kwrds:
            k = k.strip()
            if k != '' and k in row_i.combined_HIB:
                condition_two[idx].setdefault(row_j['TAG'], []).append(k)
                # break


condition_three = {}
for _, row_i in df.iterrows():
    idx = row_i["NO."]
    condition_three[idx] = {}
    for _, row_j in df_types.iterrows():
        kwrds = row_j['C'].split(",")
        for k in kwrds:
            k = k.strip()
            if k != '' and k not in row_i.combined_G:
                condition_three[idx].setdefault(row_j['TAG'], []).append(k)
                # break


condition_four = {}
for _, row_i in df.iterrows():
    idx = row_i["NO."]
    condition_four[idx] = {}
    for _, row_j in df_types.iterrows():
        kwrds = row_j['E'].split(",")
        for k in kwrds:
            k = k.strip()
            if k != '' and k in row_i.combined_G:
                condition_four[idx].setdefault(row_j['TAG'], []).append(k)
                # break



df_orignal['INGREDIENTS'] = condition_one.values()
df_orignal['WITHOUT INGREDIENT'] = condition_three.values()
df_orignal['CHARACTERISTICS/DESCRIPTION/TYPE OF PRODUCT'] = condition_two.values()
df_orignal['UNTAG IF PRESENT IN INGREDIENTS'] = condition_four.values()


# merge all the tags to the column - final tag
final_tags = []
for i in range(1, 1+len(condition_one)):
    final_tags.append(", ".join(sorted(list(set.union(set(condition_one[i].keys()),set(condition_two[i].keys()),set(condition_three[i].keys())).difference(set(condition_four[i].keys()))))))
df_orignal['FINAL_TAGS'] = final_tags


# print(union_tags) the csv file with final tags column
df_orignal.to_csv('updated_tags.csv', index=False)
