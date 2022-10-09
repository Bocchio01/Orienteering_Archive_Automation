import glob
import json


base_file_path = r"C:\Users\Bocchio\Documents\MEGAsync\Orienteering\Carte\\"
file_name_list = glob.glob(base_file_path + "*/*.ocd")

with open("./ocadAutomation/OcadFileList.json", "w") as outfile:
    matches = ['_', 'impaginazione', 'Lieto Colle']
    file_name_selected_list = [
        el for el in file_name_list if not any(x in el for x in matches)]
    json.dump(file_name_selected_list, outfile, sort_keys=True, indent=4)
