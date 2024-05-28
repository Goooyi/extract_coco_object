# 检查是否有重叠json文件被放在了不同的文件夹
import os
import tqdm

target_path = "/data/dataset/aXcellent/manu-label/v2/xcap001/"

bag_ids_target = []
for sub_folder in os.listdir(target_path):
    if not os.path.isdir(os.path.join(target_path, sub_folder)):
        continue
    to_extend = os.listdir(os.path.join(target_path, sub_folder))
    for bag_id in to_extend:
        cur = os.path.join(target_path, sub_folder, bag_id)
        bag_ids_target.append(cur)

bag_ids_target.sort()

for idx, bag in enumerate(tqdm.tqdm(bag_ids_target)):
    if idx < 2:
        continue
    if not os.path.exists(os.path.join(bag_ids_target[idx - 1], "ANNOTATION_manu")):
        continue
    if not os.path.exists(os.path.join(bag_ids_target[idx - 2], "ANNOTATION_manu")):
        continue
    if not os.path.exists(os.path.join(bag, "ANNOTATION_manu")):
        continue
    set1 = set(os.listdir(os.path.join(bag_ids_target[idx - 2], "ANNOTATION_manu")))
    set2 = set(os.listdir(os.path.join(bag_ids_target[idx - 1], "ANNOTATION_manu")))
    set3 = set(os.listdir(os.path.join(bag_ids_target[idx], "ANNOTATION_manu")))
    # check if set3 is overlapped with set1 and set2
    if set3.intersection(set1) :
        print(f"{bag} is overlapped with {bag_ids_target[idx - 2]}")
        print(f"intersect size is {sorted(list(set3.intersection(set1)))}")
    if set3.intersection(set2) :
        print(f"{bag} is overlapped with {bag_ids_target[idx - 1]}")
        print(f"intersect size is {sorted(list(set3.intersection(set2)))}")