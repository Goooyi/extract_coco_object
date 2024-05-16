import os
import tqdm
from distutils.dir_util import copy_tree

from_path = "/data/dataset/aXcellent/manu-label/v2/xcap001/"

print("Collect /backup/raw/v2_extract subfolder names..." )
raw_folder_names = []
for name in os.listdir("/backup/v2_extract"):
    if "-" not in name:
        continue
    raw_folder_names.append(name)
raw_folder_names.sort()



print("Collect /data/dataset/aXcellent/manu-label/v2/xcap001 subfolder names..." )
bag_folder = []
for folder in tqdm.tqdm(os.listdir(from_path)):
    # sub_folder like "/data/dataset/aXcellent/manu-label/v2/xcap001/20231009"
    sub_folder = os.path.join(from_path, folder)
    if os.path.isdir(sub_folder):
        for sub_sub_folder in os.listdir(sub_folder):
            sub_sub_folder = os.path.join(sub_folder, sub_sub_folder)
            if os.path.isdir(sub_sub_folder):
                bag_folder.append(sub_sub_folder)
bag_folder.sort()

print("checking...")
count = 0
not_found_count = 0
last_set = set()
last_path = ""
for idx, bag in enumerate(tqdm.tqdm(bag_folder)):
    json_path = os.path.join(bag, "ANNOTATION_manu")

    jpg_path = os.path.join(bag,"FRONT_rect")
    jpg_name_set = set()
    for jpg_name in os.listdir(jpg_path):
        jpg_name = jpg_name.split(".jpg")[0]
        jpg_name_set.add(jpg_name)

    if not os.path.exists(json_path):
        last_set = jpg_name_set
        last_path = bag
        continue

    already_moved = set()
    for json_name in os.listdir(json_path):
        json_name = json_name.split(".js")[0]
        if json_name not in jpg_name_set:
            count += 1
            if json_name not in last_set:
                # print("copy whole folder here")
                bag_tag = bag.split("/")[-1]
                tmp_idx = raw_folder_names.index(bag_tag) - 1
                if tmp_idx < 0:
                    raise ValueError("F**")
                new_bag_tag = raw_folder_names[tmp_idx]

                raw_path = os.path.join("/backup/v2_extract", new_bag_tag)

                should_exist = os.path.join("/backup/v2_extract", new_bag_tag,"FRONT_rect", json_name + ".jpg")
                if not os.path.exists(should_exist):
                    not_found_count += 1
                    raise ValueError("F**, not even found in /backup/v2_extract")

                if raw_path not in already_moved:
                    tmp_parent = list(new_bag_tag.split("-"))[:3]
                    tmp_parent = "".join(tmp_parent)
                    new_target_folder = os.path.join("/data/dataset/aXcellent/manu-label/v2/xcap001", tmp_parent,new_bag_tag)
                    print(f"copy folder from {raw_path} to {new_target_folder}")
                    copy_tree(raw_path, new_target_folder)
                    already_moved.add(raw_path)
                    print("make ANNOTATION_manu fodler")
                    if not os.path.exists(os.path.join(new_target_folder, "ANNOTATION_manu")):
                        os.makedirs(os.path.join(new_target_folder, "ANNOTATION_manu"))
                    print(f"move from {os.path.join(json_path, json_name + '.json')} to {os.path.join(new_target_folder, 'ANNOTATION_manu', json_name + '.json')}")
                    os.replace(os.path.join(json_path, json_name + ".json"), os.path.join(new_target_folder, "ANNOTATION_manu", json_name + ".json"))
                else:
                    tmp_parent = list(new_bag_tag.split("-"))[:3]
                    tmp_parent = "".join(tmp_parent)
                    new_target_folder = os.path.join("/data/dataset/aXcellent/manu-label/v2/xcap001", tmp_parent,new_bag_tag)
                    print("not copy but only move json")
                    print(f"move from {os.path.join(json_path, json_name + '.json')} to {os.path.join(new_target_folder, 'ANNOTATION_manu', json_name + '.json')}")
                    os.replace(os.path.join(json_path, json_name + ".json"), os.path.join(new_target_folder, "ANNOTATION_manu", json_name + ".json"))


            else:
                # print("only move json file here")
                # print("move from {} to {}".format(os.path.join(json_path, json_name + ".json"), os.path.join(last_path, "ANNOTATION_manu", json_name + ".json")))
                if not os.path.exists(os.path.join(last_path, "ANNOTATION_manu")):
                    os.makedirs(os.path.join(last_path, "ANNOTATION_manu"))
                os.replace(os.path.join(json_path, json_name + ".json"), os.path.join(last_path, "ANNOTATION_manu", json_name + ".json"))
                # print(f"move from {os.path.join(json_path, json_name + ".json")} to {os.path.join(last_path, "ANNOTATION_manu", json_name + ".json")}")
    last_set = jpg_name_set
    last_path = bag

print("count: {}, not found count: {}".format(count, not_found_count))