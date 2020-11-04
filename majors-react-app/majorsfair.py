import pandas as pd
import tabula
import os
import re
import json
from difflib import SequenceMatcher

def print_dict(arg_dict):
    for key, val in arg_dict.items():
        print(key, val)
        print()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_best_match(majors, category_list, category_names, bad_words):
    matches = {'Creative': [], 'Life': [], 'Leadership': [],
               'Service': [], 'Technology': [], 'Culture': [], 'Nature': []}
    # Find the best matching category
    for item in majors:  # For each major in the excel row
        item = item.strip()
        if item in bad_words:
            break
        best_match, best_ratio = None, 0
        for category_name, majors_list in zip(category_names, category_list):
            for true_major in majors_list:
                ratio = similar(item, true_major)
                if ratio > best_ratio:
                    best_match = category_name
                    best_ratio = ratio
        matches[best_match].append(item)
    return matches


# initalize directories and lists
csv_path = "majors_categories.csv"
xl_file = "masterlist.xlsx"
df = pd.read_csv(csv_path, sep=',')
xl = pd.ExcelFile(xl_file)

# append all of the data to lists
creative_list = list(df["Creative"].dropna())
leadership_list = list(df["Leadership"].dropna())
life_list = list(df["Life"].dropna())
service_list = list(df["Service"].dropna())
tech_list = list(df["Technology"].dropna())
culture_list = list(df["Culture"].dropna())
nature_list = list(df["Nature"].dropna())
# all_lists = creative_list + leadership_list + life_list + service_list + tech_list + culture_list + nature_list
category_list = [creative_list, life_list, leadership_list,
                 service_list, tech_list, culture_list, nature_list]
category_names = ['Creative', 'Life', 'Leadership',
                  'Service', 'Technology', 'Culture', 'Nature']
category_to_inds = {'Creative': 0, 'Life': 1, 'Leadership': 2, 'Service': 3, 'Technology': 4, 'Culture': 5, 'Nature': 6}
inds_to_category = {value: key for key, value in category_to_inds.items()}
bad_names = ['nan']
# iterate over the sheet_names
# pull the data that matches name, append to the dictionary
# Dictionary map names to majors
names_to_major_dict = {}
names_to_zoom_dict = {}
names_to_minor_dict = {}
names_to_cat_dict = {}
names_to_doubledawgs_dict = {}
responses = xl.parse("Form Responses 1")
# responses = responses.fillna(" ")

# Get every zoom link, match it to the majors
for row in responses.iterrows():
    majors = re.split("[;/,]", str(row[1][4])) + \
        re.split("[;/,]", str(row[1][5]))
    minors = re.split("[;/,]", str(row[1][6])) + \
        re.split("[;/,]", str(row[1][7]))
    certificates = re.split("[,;/]", str(row[1][8])) + \
        re.split("[,;/]", str(row[1][9]))
    good_certs = []
    for cert in certificates:
        if cert is None or cert == 'nan':
            continue
            # good_certs.append("")
        else:
            good_certs.append(cert)

    doubledawgs = re.split("[,;/]", str(row[1][10])) + \
        re.split("[,;/]", str(row[1][11]))
    good_dawgs = []

    for dawg in doubledawgs:
        if dawg is None or dawg == 'nan':
            continue
            # good_dawgs.append("")
        else:
            good_dawgs.append(dawg)
        
    certificates = good_certs
    doubledawgs = good_dawgs

    # Method that takes in major/minor/category and then returns the best match, then appends value to dictionary key[name]
    names_to_major_dict[str(row[1][1])] = find_best_match(
        majors, category_list, category_names, bad_names)
    names_to_minor_dict[str(row[1][1])] = find_best_match(
        minors, category_list, category_names, bad_names)
    names_to_cat_dict[str(row[1][1])] = certificates
    names_to_doubledawgs_dict[str(row[1][1])] = doubledawgs

names_to_zoom = {}
# go through all the xl sheets and pull the zoom links, match them to the correct person
for sheet in xl.sheet_names:
    if sheet == "Form Responses 1" or sheet == "Other":
        continue
    responses = xl.parse(sheet)
    # zoom_arr = []
    for row in responses.iterrows():
        # zoom_arr=[] #makes an empty array
        if(str(row[1][0])) == "nan":
            continue
        else:
            name = str(row[1][2])
            link = str(row[1][0])
            if name not in names_to_zoom:
                names_to_zoom[name] = ['' for _ in range(len(category_names))]
            names_to_zoom[name][category_to_inds[str(sheet)]] = link

# Sort the majors for each person, preserves the order of the categories
for name in names_to_major_dict.keys():
    names_to_major_dict[name] = [sorted(vals) for vals in names_to_major_dict[name].values()]

# Sort the minors for each person, preserves the order of the categories
for name in names_to_minor_dict.keys():
    names_to_minor_dict[name] = [sorted(vals) for vals in names_to_minor_dict[name].values()]

organized_dict = {}
for category in category_names:
    category_ind = category_to_inds[category]
    organized_dict[category] = {}
    for person in sorted(names_to_major_dict.keys()):
        if person not in names_to_zoom.keys():
            continue
        person_info = {}
        person_info['Zoom Link'] = names_to_zoom[person][category_ind]
        person_info['Majors'] = names_to_major_dict[person][category_ind]
        person_info['Minors'] = names_to_minor_dict[person][category_ind]
        person_info['Certificates'] = names_to_cat_dict[person]
        person_info['Double Dawgs / Double Majors'] = names_to_doubledawgs_dict[person]
        organized_dict[category][person] = person_info

# print(organized_dict)
organized_df = pd.DataFrame.from_dict(organized_dict)
organized_df = organized_df.rename(columns=inds_to_category)
# print(organized_dict)
# organized_df.to_csv(r'Organized_MasterList.csv')

# df = organized_df.to_json(orient='columns', default_handler=blank)
# print(df)
jsonfiles = json.loads(organized_df.to_json())
# print(jsonfiles)
organized_df.to_json(r'Organized_MasterList.json')

# print(organized_df['Creative'].apply(pd.Series))

with pd.ExcelWriter(r'Organized_MasterList.xlsx') as writer:
    for name in category_names:
        organized_df[name].apply(pd.Series).to_excel(writer, sheet_name=name)

# organized_df.to_excel(r'Organized_MasterList.xlsx', columns=inds_to_category)

# for word in major.split('-')[0].strip().split(' '):  # Take all the words before the dash -
#     if word in bad_words: break  # Skip if bad word
#     for category_name, majors_list in zip(category_names, category_list):
#         for true_major in majors_list:
#             if word in true_major:  # If the word is in one of the majors of this category, then add it
#                 matches[category_name].append(major)
#                 break

# for creative_major in creative_list:
#     if word in creative_major:
#         categories['Creative'].append(major)
#         matched = True
#         break
# if matched:
#     break

# matched = False

# for text in all_lists:
#     for word in text.strip().split(' '):

#         if word.casefold() in major.casefold():
#             majors_list.append(major)
#             matched = True
#             break

#     if matched:
#         break

# if major.casefold() in text.strip().casefold():
#     majors_list.append(major)
# if major.casefold() == "Exploratory Center":
#     majors_list.append(major)

# print(names_to_major_dict)
# for sheet in xl.sheet_names:
#     df = pd.read_excel("masterlist.xlsx", sheet_name=sheet)

# for reference:
# print(row[1][0]) #gets zoom links
# print(row[1][2]) #gets their names
# print(row[1][5]) #gets majors
# print(row[1][6]) #gets other majors
