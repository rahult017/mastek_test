import json,traceback
import pandas as pd

class ParentNode(object):
    #initialize class object

    def __init__(self, id, label, link):
        self.link = link
        self.label = label
        self.id = id
        self.children = []
    
    def child(self,id,label,link):
         #check if label already exists in children list
        child_found = [d for d in self.children if d.label == label]
        #append to children list if doesnt exist
        if not child_found:
            child = ParentNode(id,label,link)
            #initialize child class object
            self.children.append(child)
        else:
            child = child_found[0]
        return child

    def as_dict(self):
        #convert class object to dictionary
        res = {'id': int(self.id),
            "link":self.link,
            "label":self.label}
        
        #append the child class objects as list elements
        res['children'] = [c.as_dict() for c in self.children]
        return res

def preprocess_file(file_name):
    #read the csv file
    try:
        df = pd.read_csv(file_name)
        #check if file is empty
        if df.shape[0] == 0 or df.shape[1] == 0:
            print("Empty file")
            response ={
                "status":"Fail"
            }
            return response
    except Exception as e:
        print("Error reading file path")
        response ={
                "status":"Fail"
            }
        return response
    
    #remove empty rows
    df = df.dropna(how='all')
    #Create parent with the first row
    first_row = df.loc[0]
    root = ParentNode(first_row[2],first_row[1],first_row[0])

    #Remove the first row/parent
    df = df.iloc[1: , :]

    response = {
        "df":df,
        "root":root,
        "status":"Success"
    }

    return response

def iterate_dataframe(df, root):
    try:
        #Iterate all rows to form parent-child
        for row in df.iterrows():
            #convert tuple to dataframe
            row = row[1].to_frame()
            #check if row level 1 label is equal to parent label
            if (row.iloc[1,0] == root.label):
                #drop null coloums
                row = row.dropna()
                #get no of child from row size, 3 as three fields, -1 for parent
                no_child = int(row.size/3)-1

                for i in range(no_child):
                    #for the first level of child, append directly to root node
                    if (i==0):
                        root.child(row.iloc[(i*3)+5,0],row.iloc[(i*3)+4,0],row.iloc[(i*3)+6,0])
                    if (i>0):
                        #check if the row label exits in parent node
                        child_found = [c for c in root.children if c.label == row.iloc[(i*3)+1,0]]
                        if not child_found:
                            #if child node doesnt exist for parent, return -1 node to append the child into
                            child_found = [c for c in root.children if c.label == row.iloc[(i*3)-2,0]]
                            #append child node to the returned parent node, used for nesting child-parent
                            child_found[-1].children[-1].child(row.iloc[(i*3)+5,0],row.iloc[(i*3)+4,0],row.iloc[(i*3)+6,0])
                        else:
                            child_found[0].child(row.iloc[(i*3)+5,0],row.iloc[(i*3)+4,0],row.iloc[(i*3)+6,0])
            else:
                response = {
                    "status":"Fail"
                }
                return response
        #convert class object to json
        json_file = json.dumps(root.as_dict(), indent=4)
        print(json_file)
        response = {
            "json_file":json_file,
            "status":"Success"
        }

        return response
    except Exception as e:
        print("Error iterating code")
        response ={
            "status"=="Fail"
        }
        return response

def write_to_disk(json_file):
    try:
        #write to disk
        with open("data.json", "w") as outfile:
            outfile.write(json_file)
        return True
    except Exception as e:
        print("Error writing json to disk")
        print(traceback.format_exc())
        return False

#Main execution block
try:
    file_name = "data.csv"
    response = preprocess_file(file_name)
    response = iterate_dataframe(response['df'], response['root'])
    status = write_to_disk(response['json_file'])
    if status == True:
        print("Success")
except Exception as e:
    print("Failed")
    print(traceback.format_exc())
