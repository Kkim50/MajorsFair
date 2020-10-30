import pandas as pd
import tabula
import os
import re
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

        # if item.casefold() == "Exploratory Center":
        #     matches[best_match].append(item)

    return matches


# initalize directories and lists
csv_path = "majors_categories.csv"
xl_file = "masterlist.xlsx"
df = pd.read_csv(csv_path, sep=',')

# creative_list, leadership_list, life_list, service_list = [], [], [], []
# tech_list, culture_list, nature_list = [], [], []

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
bad_names = ['nan']

# read the majors fair excel file
xl = pd.ExcelFile(xl_file)
# print(xl.sheet_names)

# iterate over the sheet_names
# pull the data that matches name, append to the dictionary
# Dictionary map names to majors
names_to_major_dict = {}
names_to_zoom_dict = {}
names_to_minor_dict = {}
names_to_cat_dict = {}
organized_dict = {}

responses = xl.parse("Form Responses 1")

# Get every zoom link, match it to the majors
for row in responses.iterrows():
    majors = re.split("[;/,]",str(row[1][4])) + re.split("[;/,]", str(row[1][5]))
    minors = re.split("[;/,]",str(row[1][6])) + re.split("[;/,]",str(row[1][7]))
    certificates = re.split("[;/,]",str(row[1][8])) + re.split("[;/,]",str(row[1][9]))

    # Method that takes in major/minor/category and then returns the best match, then appends value to dictionary key[name]
    names_to_major_dict[str(row[1][1])] = find_best_match(
        majors, category_list, category_names, bad_names)
    names_to_minor_dict[str(row[1][1])] = find_best_match(
        minors, category_list, category_names, bad_names)
    names_to_cat_dict[str(row[1][1])] = find_best_match(
        certificates, category_list, category_names, bad_names)

# go through all the xl sheets and pull the zoom links, match them to the correct person
for sheet in xl.sheet_names:
    if sheet == "Form Responses 1" or sheet == "Other":
        continue
    responses = xl.parse(sheet)
    for row in responses.iterrows():
        names_to_zoom_dict[row[1][2]] = row[1][0]

# Export it to an excel sheet
for key in sorted(names_to_major_dict.keys()):
    if key in names_to_zoom_dict.keys():
        cols = [names_to_zoom_dict[key]]
        # for name in category_names:
        #     col = 'Majors: ' + ', '.join(names_to_major_dict[key]) + ', minors: '
        # creative = names_to_major_dict[key]['Creative'] + names_to_minor_dict[key]['Creative']
        # print(names_to_major_dict[key])
        organized_dict[key + ' - Majors'] = [names_to_zoom_dict[key],
                                             *[sorted(items) for items in names_to_major_dict[key].values()]]
        organized_dict[key + ' - Minors'] = ['',
                                             *[sorted(items) for items in names_to_minor_dict[key].values()]]
        organized_dict[key + ' - Certificates'] = ['',
                                                   *[sorted(items) for items in names_to_cat_dict[key].values()]]

organized_df = pd.DataFrame.from_dict(organized_dict, orient="index")
organized_df = organized_df.rename(columns={0: "Zoom Links", 1: "Creative", 2: "Life",
                                            3: "Leadership", 4: "Service", 5: "Technology", 6: "Culture", 7: "Nature"})
print(organized_df)
organized_df.to_csv(r'./Organized_MasterList.csv')
organized_df.to_excel(r'./Organized_MasterList.xlsx')

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
