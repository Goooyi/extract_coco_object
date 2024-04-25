# %%
# this script validate axera json format
import os
import json
import sys
from validate_utils import *

# with open(sys.argv[1], 'r') as f:
#     json_data = json.load(f)

root_path = "/code/gn0/extract_coco_object/tmp_stageConvert"

# %%
# check if all id is unique
check_all_id_diff_with_master_slave_and_frame_name_patter(root_path)
# %%
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        # check_obstacle_annotations(json_data)
        check_traffic_light_annotations(json_data)
# %%
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        check_traffic_light_annotations(json_data)
# %%
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        check_traffic_sign_annotations(json_data)

# %%
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        check_road_arrow_annotations(json_data)
# %%
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        check_lane_annotation(json_data)

# %%
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        check_road_boundary_annotation(json_data)

# %%
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        check_stop_line_annotation(json_data)



# %%
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        check_cross_walk_annotation(json_data)

# %%
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        check_intersection_annotation(json_data)
# %%
