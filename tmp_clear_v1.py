import os

from_path = "/data/dataset/aXcellent/manu-label/v1/xcap001/"

for folder in os.listdir(from_path):
    # sub_folder like "/data/dataset/aXcellent/manu-label/v1/xcap001/20231009"
    sub_folder = os.path.join(from_path, folder)
    if os.path.isdir(sub_folder):
        # sub_sub_folder like "/data/dataset/aXcellent/manu-label/v1/xcap001/20231009/2023-10-09-17-06-49"
        for sub_sub_folder in os.listdir(sub_folder):
            sub_sub_folder = os.path.join(sub_folder, sub_sub_folder)
            if os.path.isdir(sub_sub_folder):
                # make "ANNOTATION_manu" folder
                if not os.path.exists(os.path.join(sub_sub_folder, "ANNOTATION_manu")):
                    os.makedirs(os.path.join(sub_sub_folder, "ANNOTATION_manu"))

                for json_file in os.listdir(sub_sub_folder):
                    json_file = os.path.join(sub_sub_folder, json_file)
                    if json_file.endswith(".json"):
                        # move all json files to folder "ANNOTATION_manu"
                        os.replace(json_file, os.path.join(sub_sub_folder, "ANNOTATION_manu", json_file.split("/")[-1]))