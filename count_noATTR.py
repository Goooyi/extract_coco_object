import os
import json
from tqdm import tqdm

v1_root = "/data/dataset/aXcellent/manu-label/axera_manu_v1.0/ANNOTATION_TRAFFIC/"
sub_folder = ["FRONT_WIDE_rect", "FRONT_rect"]

traffic_light_file_count = 0
traffic_sign_file_count = 0
traffic_sign_instance_count = 0
traffic_light_instance_count = 0
traffic_sign_withoutAttr_instance_count = 0
traffic_light_withoutAttr_instance_count = 0

for subf in sub_folder:
    for file in os.listdir(os.path.join(v1_root,subf)):
        json_file = os.path.join(v1_root, subf, file)
        if json_file.endswith(".json"):
            with open(json_file, 'r') as f:
                json_data = json.load(f)
                for instanc in json_data["instances"]:
                    if instanc["category"] == "traffic_light" or instanc["category"] == "交通灯":
                        traffic_light_instance_count += 1
                        if instanc["attributes"] == {}:
                            print(json_file)
                            traffic_light_withoutAttr_instance_count += 1
                    elif instanc["category"] == "traffic_sign" or instanc["category"] == "交通标志":
                        traffic_sign_instance_count += 1
                        if instanc["attributes"] == {}:
                            traffic_light_withoutAttr_instance_count += 1


# print(f"V1 annotation has total {traffic_light_file_count} traffic_light files")
print(f"V1 annotation has total {traffic_sign_instance_count} traffic_sign instances, in which {traffic_sign_withoutAttr_instance_count} without attributes")
print(f"V1 annotation has total {traffic_light_instance_count} traffic_light instances, in which {traffic_light_withoutAttr_instance_count} without attributes")
