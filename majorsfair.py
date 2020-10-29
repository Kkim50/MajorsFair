import pandas as pd 
import tabula
import os

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#initalize directories and lists
csv_path = "majors_categories.csv"
xl_file = "masterlist.xlsx"
df = pd.read_csv(csv_path, sep=',')

creative_list, leadership_list, life_list, service_list = [],[],[],[]
tech_list, culture_list, nature_list = [],[],[]

#append all of the data to lists
creative_list = list(df["Creative"].dropna())
leadership_list = list(df["Leadership"].dropna())
life_list = list(df["Life"].dropna())
service_list = list(df["Service"].dropna())
tech_list = list(df["Technology"].dropna())
culture_list = list(df["Culture"].dropna())
nature_list = list(df["Nature"].dropna())
all_lists = creative_list + leadership_list + life_list + service_list + tech_list + culture_list + nature_list

#read the majors fair excel file
xl = pd.ExcelFile(xl_file)
#print(xl.sheet_names)

#iterate over the sheet_names
#pull the data that matches name, append to the dictionary
#Dictionary map names to majors
names_to_major_dict = {}
names_to_zoom_dict = {}
organized_dict = {}

responses = xl.parse("Form Responses 1")
bad_words = ['nan']

#Get every zoom link, match it to the majors 
for row in responses.iterrows():
    majors = str(row[1][4]).split(",") + str(row[1][5]).split(",") 
    minors = str(row[1][6]).split(",") + str(row[1][7]).split(",") 
    certificates = str(row[1][8]).split(",") + str(row[1][9]).split(",") 

    # majors_list = []
    category_list = [creative_list, life_list, leadership_list, service_list, tech_list, culture_list, nature_list]
    category_names = ['Creative', 'Life', 'Leadership', 'Service', 'Technology', 'Culture', 'Nature']

    matches = {'Creative': [], 'Life': [], 'Leadership': [], 'Service': [], 'Technology': [], 'Culture': [], 'Nature': []}
    for major in majors:  # For each major in the excel row
        major = major.strip()
        if major in bad_words: break

        # Find the best matching category
        best_match, best_ratio = None, 0
        for category_name, majors_list in zip(category_names, category_list):
            for true_major in majors_list:
                ratio = similar(major, true_major)
                if ratio > best_ratio:
                    best_match = category_name
                    best_ratio = ratio
        matches[best_match].append(major)
    names_to_major_dict[str(row[1][1])] = matches

for key, val in names_to_major_dict.items():
    continue
    #print(key, val)
    #print()

#go through all the xl sheets and pull the zoom links, match them to the correct person
for sheet in xl.sheet_names: 
    if sheet == "Form Responses 1" or sheet == "Other":
        continue
    responses = xl.parse(sheet)
    for row in responses.iterrows():
        names_to_zoom_dict[row[1][2]] = row[1][0]


#Export it to an excel sheet
names_to_major_df = pd.DataFrame.from_dict(names_to_major_dict,orient="index",)
names_to_zoom_df = pd.DataFrame.from_dict(names_to_zoom_dict,orient="index",)

for key in sorted(names_to_major_dict.keys()):
    if key in names_to_zoom_dict.keys():
        organized_dict[key] = [names_to_zoom_dict[key], *names_to_major_dict[key].values()]

organized_df = pd.DataFrame.from_dict(organized_dict,orient="index",)
print(organized_df)
#organized.to_excel(r'./Organized_MasterList.xlsx', index = False)

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

#for reference:
    #print(row[1][0]) #gets zoom links
    #print(row[1][2]) #gets their names
    #print(row[1][5]) #gets majors
    #print(row[1][6]) #gets other majors
