import pandas as pd 
import tabula
import os
csv_path = "Final.csv"

csv_path1 = "./First_half.csv"
csv_path2 = "./Sec_half.csv"
xl_file = "./masterlist.xlsx"

df1 = pd.read_csv(csv_path1, sep=',')
df2 = pd.read_csv(csv_path2, sep=',')
#iterate over the sheet_names
#pull the data that matches name, append to the dictionary

creative_list, leadership_list, life_list, service_list = [],[],[],[]
tech_list, culture_list, nature_list = [],[],[]


creative_list.append(df1["Creative"].dropna())
leadership_list.append(df1["Leadership"].dropna())
life_list.append(df1["Life"].dropna())
service_list.append(df1["Service"].dropna())

tech_list.append(df2["Technology"].dropna())
culture_list.append(df2["Culture"].dropna())
nature_list.append(df2["Nature"].dropna())

print(nature_list)

df = pd.concat([df1["Creative"],df1["Leadership"], df1["Life"],  df1["Life"], df1["Service"],  df2["Technology"],  df2["Culture"], df2["Nature"]], axis=1)
df.to_csv(csv_path, index=False)
xl = pd.ExcelFile(xl_file)
#print(xl.sheet_names)


#Dictionary map names to majors
names_to_major_dict = {}

responses = xl.parse("Form Responses 1")

#Get every zoom link, match it to the majors 
for row in responses.iterrows():
    #print(row[1][0]) #gets zoom links
    #print(row[1][2]) #gets their names
    majors = str(row[1][4]).split(",") + str(row[1][5]).split(",") 
    #zoom = row[1][0]
    majors_list = []

    for i in majors:
        i = i.strip()
        majors_list.append(i)
    
    names_to_major_dict[row[1][1]] = majors_list

for sheet in xl.sheet_names:
    df = pd.read_excel("masterlist.xlsx", sheet_name=sheet)

    #for row in df.iterrows():
       # if row[1][2] in names_to_major_dict.keys():
          #  zoom = row[1][0]

    #majors_to_zoom_dict[row[1][5]] = row[1][0], row[1][6]
    #print(row[1][5]) #gets majors
    #print(row[1][6]) #gets other majors
#print(names_to_major_dict)
#Dictionary map major to creative (or vise versa)
#majors_to_category = {}
