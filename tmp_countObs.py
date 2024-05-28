import os
import tqdm
import json


target_path = "/data/dataset/aXcellent/manu-label/v2/xcap001/"
bag_ids_target = []
for sub_folder in os.listdir(target_path):
    if not os.path.isdir(os.path.join(target_path, sub_folder)):
        continue
    to_extend = os.listdir(os.path.join(target_path, sub_folder))
    to_extend = [os.path.join(target_path, sub_folder,x) for x in to_extend]
    bag_ids_target.extend(to_extend)

obs_count = 0

# read json from "ANNOTATION_manu" folder
for bag in tqdm.tqdm(bag_ids_target):
    if os.path.exists(os.path.join(bag, "ANNOTATION_manu")):
        # read json
        for json_file in os.listdir(os.path.join(bag, "ANNOTATION_manu")):
            if json_file.endswith(".json"):
                json_path = os.path.join(bag, "ANNOTATION_manu", json_file)
                with open(json_path, 'r') as f:
                    json_data = json.load(f)
                    if "obstacle" in json_data["annotations"].keys():
                        obs_count += 1


print(obs_count)