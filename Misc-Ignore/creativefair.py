import pandas as pd 

file = "masterlist.xlsx"
xl = pd.ExcelFile(file)
#print(xl.sheet_names)

#iterate over the sheet_names
#pull the data that matches name, append to the dictionary

creative_list = ["art", "consumer", "dance", "enterainment", "media", "furnishings", "interiors", "journalism", "music", "theatre", "agricultural communication", "landscape architecture", "communication", "pr", "public relations", "interdisciplinary"]

#Dictionary map names to majors
names_to_major_dict = {}
responses = xl.parse("Creative")

#Get every zoom link, match it to the majors 
for row in responses.iterrows():
    #print(row[1][0]) #gets zoom links
    #print(row[1][2]) #gets their names
    majors = str(row[1][5]).split(",") + str(row[1][6]).split(",") 
    minors = str(row[1][7]).split(",") + str(row[1][8]).split(",") 
    certificates = str(row[1][9]).split(",") + str(row[1][10]).split(",") 

    zoom = row[1][0]
    majors_list = []

    for i in majors:
        i = i.strip()
        # print(i)

        for text in creative_list:
            if text.casefold() in i.casefold(): 
                majors_list.append(i)

    names_to_major_dict[row[1][2]] = (zoom, majors_list, minors,certificates)
    print(majors_list, "\n Minors: ", minors, "\n Certificates:", certificates)

    #majors_to_zoom_dict[row[1][5]] = row[1][0], row[1][6]
    #print(row[1][5]) #gets majors
    #print(row[1][6]) #gets other majors
#print(names_to_major_dict)
#Dictionary map major to creative (or vise versa)
new = pd.DataFrame.from_dict(names_to_major_dict)
new.to_excel(r'./Creatve_File.xlsx', index = False)
