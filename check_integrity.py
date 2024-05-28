import os
import json
import shutil
import tqdm
import time
from utils import unixTime2Date

# record start time
start_time = time.time()
file_count = 0
frame_count = 0
copy_count = 0
total_file_size = 0

carid = "001"
source_path = "/backup/v2_extract/"
target_path = "/data/dataset/aXcellent/manu-label/v2/xcap001/"

bag_ids_target = []
for sub_folder in os.listdir(target_path):
    if not os.path.isdir(os.path.join(target_path, sub_folder)):
        continue
    to_extend = os.listdir(os.path.join(target_path, sub_folder))
    for bag_id in to_extend:
        cur = os.path.join(target_path, sub_folder, bag_id)
        bag_ids_target.append(cur)

sub_folder_candidates = ["LIDAR_VCS"
                        , "LIDAR_TOP"
                        , "FRONT_WIDE_rect"
                        , "FRONT_WIDE"
                        , "FRONT_rect"
                        , "FRONT"
                        , "FISHEYE_RIGHT_rect"
                        , "FISHEYE_RIGHT"
                        , "FISHEYE_LEFT_rect"
                        , "FISHEYE_LEFT"
                        , "FISHEYE_FRONT_rect"
                        , "FISHEYE_FRONT"
                        , "FISHEYE_BACK_rect"
                        , "FISHEYE_BACK"
                        , "BACK_rect"
                        , "BACK"
                        , "FRONT_redist_new"
                        ]


for bag in tqdm.tqdm(bag_ids_target):
    file_count_set = set()
    if os.path.exists(os.path.join(bag, "ANNOTATION_manu")):
        anno_json_count = len(os.listdir(os.path.join(bag, "ANNOTATION_manu")))
        json_name = os.listdir(os.path.join(bag, "ANNOTATION_manu"))
        frame_names = [x.split(".j")[0] for x in json_name]
        for sub_can in sub_folder_candidates:
            candidate_names = set()
            if not os.path.isdir(os.path.join(bag, sub_can)):
                continue
            else:
                # count files
                files = os.listdir(os.path.join(bag, sub_can))
                candidate_names = set([".".join(x.split(".")[:2]) for x in files ])
                for frame_name in frame_names:
                    if frame_name not in candidate_names:
                        print(f"{frame_name} from {bag} not in {sub_can}")

