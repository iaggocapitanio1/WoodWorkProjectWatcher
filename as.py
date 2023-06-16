import json
import os
import time
import uuid

import pandas as pd
import requests
import watchdog.events
import watchdog.observers
from watchdog.events import FileSystemEventHandler

# Define the columns to read from the sheets
cols = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
cols2 = [0, 1, 2, 3, 4]
cols1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


def on_created(path):
    print("Watchdog received created event - %s." % path)
    filename = path
    filename2 = os.path.basename(filename)
    filename3 = filename2.split("_", 3)[-1].split(".")[0]
    print("Nome do ficheiro:", filename3)

    # Read data from sheet_name=[6]
    df6 = pd.read_excel(filename, sheet_name=['DATA - Paineis'], usecols=cols)
    df6_concat = pd.concat(df6[frame] for frame in df6.keys())
    df6_concat = df6_concat.dropna(subset=['REF PEÇA (A)'])

    # Read data from sheet_name=[9]
    df9 = pd.read_excel(filename, sheet_name=['DATA - Macicos'], usecols=cols1)
    df9_concat = pd.concat(df9[frame] for frame in df9.keys())
    df9_concat = df9_concat.dropna(subset=['REF PEÇA (A)'])

    # Combine data from sheet_name=[6] and sheet_name=[9]
    combined_df = pd.concat([df6_concat, df9_concat])

    # Initialize a new list to store the updated group tuples
    updated_group_names = []
    df10 = pd.read_excel(filename, sheet_name=['DATA - ASM'], usecols=cols2)
    df11 = pd.concat(df10[frame] for frame in df10.keys())
    df12 = df11.isnull()
    for j in range(0, len(df11)):
        if df12['Ref CONJ (A)'].values[j] == True:
            break
    df11 = df11.fillna(0)
    for i in range(j):
        if df12._get_value(i, 0, takeable=True) == True:
            continue
        name = df11['Ref CONJ (A)'].values[i]
        print("nomes da pagina dos grupos:", name)
    etiq_groups = {}
    for index, row in df11.iterrows():
        etiq = row["ETIQ"]
        if etiq not in etiq_groups:
            etiq_groups[etiq] = []  # initialize the list for this group
        etiq_groups[etiq].append(row)
        group_names = []
    for etiq, rows in etiq_groups.items():
        name = rows[0]["Ref CONJ (A)"]
        group_names.append(name)
    print(f"number_of_groups:{len(etiq_groups)}")
    # print(f"name_of_groups:{group_names}")
    # Initialize a list to store the group names
    group_names = []

    # Iterate over each group in etiq_groups
    for i, (etiq, rows) in enumerate(etiq_groups.items()):
        # Get the name of the group (i.e., the 'Ref CONJ (A)' value) from the first row
        name = rows[0]['Ref CONJ (A)']
        # Append a tuple to the group_names list containing the group number and name
        group_names.append(('group' + str(i + 1), name))
    print("name_of_groups:", group_names)
    # Iterate over each group in group_names
    for group_number, group_name in group_names:
        # Initialize a list to store the matching data for the current group
        matching_names = []

        # Iterate over the rows in the combined DataFrame
        for _, row in combined_df.iterrows():
            # Check if the 'REF PEÇA (A)' value starts with the group_name
            if row['REF PEÇA (A)'].startswith(group_name):
                # Add the row data to the matching_data list
                matching_names.append(row['REF PEÇA (A)'])

        # Append a tuple to the updated_group_names list containing the group number, name, and matching data
        updated_group_names.append((group_number, group_name, matching_names))
    id_module = 'urn:ngsi-ld:Assembly:' + str(uuid.uuid4()) + str(filename3)
    # Print the updated_group_names list
    print("Updated group names with additional data:")
    for group in updated_group_names:
        print(group)
    url = "http://localhost:1026/ngsi-ld/v1/entities"
    payload = json.dumps({
        'id': id_module,
        'type': 'Module',
        'name': {
            'type': 'Property',
            'value': group_names
        },
        'amount': {
            'type': 'Property',
            'value': len(etiq_groups)
        },
        'belongsToAssembly': {
            'type': 'Relationship',
            'object': f"urn:ngsi-ld:Assembly:{filename3}"  ##pertence ao Assembly
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Fiware-Service': 'woodwork40',
        'Link': '<http://woodwork4.ddns.net/context/ww4zero.context.jsonld>; <http://woodwork4.ddns.net/context/ww4zero.context-ngsi.jsonld>'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    print(response.text)


if __name__ == "__main__":
    src_path = "/home/iaggo/Documents/Eins/WoodWorkProjectWatcher/media/public/mofreitas/clientes/iaggo.capitanio@gmail.com/Chanut/briefing/Listas de Corte e Etiquetas/CHANUT_BAR.xlsx"
    on_created(src_path)


