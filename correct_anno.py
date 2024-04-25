import os
import json

root_path = "/data/dataset/aXcellent/manu-label/v1/xcap001/"

# for every folder in root_path, iter their sub folder
for folder in os.listdir(root_path):
    sub_folder = os.path.join(root_path, folder)
    if os.path.isdir(sub_folder):
        for sub_sub_folder in os.listdir(sub_folder):
            sub_sub_folder = os.path.join(sub_folder, sub_sub_folder)
            if os.path.isdir(sub_sub_folder):
                # for every json file in sub_sub_folder
                for json_file in os.listdir(sub_sub_folder):
                    json_file = os.path.join(sub_sub_folder, json_file)
                    if json_file.endswith(".json"):
                        with open(json_file, 'r') as f:
                            json_data = json.load(f)
                        if "obstacle" in json_data["annotations"]:
                            for ann in json_data["annotations"]["obstacle"]:
                                # if "length" in ann["dimension"].keys():
                                #     continue
                            #change the key "x", "y" , "z" of ann["obstacle"][i]["dimension"] to "length", "width", "height"
                                ann["dimension"]["length"] = ann["dimension"]["x"]
                                ann["dimension"]["width"] = ann["dimension"]["y"]
                                ann["dimension"]["height"] = ann["dimension"]["z"]
                                del ann["dimension"]["x"]
                                del ann["dimension"]["y"]
                                del ann["dimension"]["z"]
                                # change the key "x", "y" , "z" "w" of ann["obstacle"][i]["quaternion"] to "qx", "qy", "qz", "qw"
                                ann["quaternion"]["qx"] = ann["quaternion"]["x"]
                                ann["quaternion"]["qy"] = ann["quaternion"]["y"]
                                ann["quaternion"]["qz"] = ann["quaternion"]["z"]
                                ann["quaternion"]["qw"] = ann["quaternion"]["w"]
                                del ann["quaternion"]["x"]
                                del ann["quaternion"]["y"]
                                del ann["quaternion"]["z"]
                                del ann["quaternion"]["w"]

                            with open(json_file, 'w') as f:
                                json.dump(json_data, f)


# # for every folder in root_path, iter their sub folder
# for json_file in os.listdir("/code/gn0/extract_coco_object/tmp_stageConvert"):
#     json_file = os.path.join("/code/gn0/extract_coco_object/tmp_stageConvert", json_file)
#     if json_file.endswith(".json"):
#         with open(json_file, 'r') as f:
#             json_data = json.load(f)
#         if "obstacle" in json_data["annotations"]:
#             for ann in json_data["annotations"]["obstacle"]:
#                 if "length" in ann["dimension"].keys():
#                     continue
#             #change the key "x", "y" , "z" of ann["obstacle"][i]["dimension"] to "length", "width", "height"
#                 ann["dimension"]["length"] = ann["dimension"]["x"]
#                 ann["dimension"]["width"] = ann["dimension"]["y"]
#                 ann["dimension"]["height"] = ann["dimension"]["z"]
#                 del ann["dimension"]["x"]
#                 del ann["dimension"]["y"]
#                 del ann["dimension"]["z"]
#                 # change the key "x", "y" , "z" "w" of ann["obstacle"][i]["quaternion"] to "qx", "qy", "qz", "qw"
#                 ann["quaternion"]["qx"] = ann["quaternion"]["x"]
#                 ann["quaternion"]["qy"] = ann["quaternion"]["y"]
#                 ann["quaternion"]["qz"] = ann["quaternion"]["z"]
#                 ann["quaternion"]["qw"] = ann["quaternion"]["w"]
#                 del ann["quaternion"]["x"]
#                 del ann["quaternion"]["y"]
#                 del ann["quaternion"]["z"]
#                 del ann["quaternion"]["w"]

#             with open(json_file, 'w') as f:
#                 json.dump(json_data, f)