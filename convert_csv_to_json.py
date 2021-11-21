import pandas as pd
import json

df = pd.read_csv("data.csv", skip_blank_lines=True, converters={'Level 1 - ID' : str, 'Level 2 - ID': str})
base_url_list = df['Base URL'].to_list()

menu_list = []
parent_menu_ids = []
children = []
sub_children = []

for index, row in enumerate(base_url_list):
   
    level_1_name = str(df['Level 1 - Name'][index])
    level_1_id = str(df['Level 1 - ID'][index])
    level_1_url = str(df['Level 1 - URL'][index])
    
    if level_1_id == "nan" or level_1_name == "nan" or level_1_url == "nan":        
        continue
  
    # Level One Menu
    menu_item = { "label": level_1_name, "id": level_1_id, "link": level_1_url }    
    
    if not level_1_id in parent_menu_ids:
        # menu_list.append(menu_item)    
        parent_menu_ids.append(level_1_id)

        children_menu_ids = []
        children_menu = []

        for i, a in enumerate(base_url_list):           
            parent_id = str(df['Level 1 - ID'][i])
            level_2_name = str(df['Level 2 - Name'][i])
            level_2_id = str(df['Level 2 - ID'][i])
            level_2_url = str(df['Level 2 URL'][i])

            if level_2_id == "nan" or level_2_name == "nan" or level_2_url == "nan":
                print("--- B ---")                          
                continue

            if level_1_id == parent_id:
                child_info = {"label": level_2_name, "id": level_2_id, "link": level_2_url }

                if not level_2_id in children_menu_ids:
                    children_menu_ids.append(level_2_id)                  
                    
                    sub_children_menu_list = []

                    for k, b in enumerate(base_url_list):                       
                        parent_id = str(df['Level 1 - ID'][k])
                        children_id = str(df['Level 2 - ID'][k])
                        level_3_name = str(df['Level 3 - Name'][k])
                        level_3_url = str(df['Level 3 URL'][k])

                        if level_3_url == "nan" or level_3_name == "nan":                          
                            continue

                        if parent_id == level_1_id and children_id == level_2_id: 
                            # pass
                            sub_children_menu = { "label": level_3_name, "link": level_3_url }
                            sub_children_menu_list.append(sub_children_menu)

                    child_info['children'] = sub_children_menu_list
                    children_menu.append(child_info)
        
        menu_item['children'] = children_menu
        menu_list.append(menu_item)    


    
f = open("data.json", "w")
f.write(json.dumps(menu_list))
f.close()        