import pandas as pd 
import os 
import json 


def get_client_data(client):
    result = {"name": [],
              "description": [],
              "metadata": [],
              "file": []
              }

    cid = client.strip("cl")
    files_list = os.listdir(f"./Data/{cid}")

    for f in files_list:
        if ".json" in f:
            continue
        else: 
            name = f[:f.rfind(".")]
            result["name"].append(name)
            
            metadata_file = open(f"./Data/{cid}/{name}.json", "r", encoding="utf-8") 
            metadata = json.load(metadata_file)

            result["description"].append(metadata["text_desc"])
            result["file"].append(f)
            result["metadata"].append(f"Metadata_{name}")

    return result


data = get_client_data("90")
df = pd.DataFrame(data)

for row in df.iterrows():
    print(row)

    print ("\n\n\n ______________")

print("Ffdsfs")