# %%
# this script validate axera json format
import os
import json
import sys
from validate_utils import *

# with open(sys.argv[1], 'r') as f:
#     json_data = json.load(f)
# root_path = "/backup/manu_label_v2/ANNOTATION/roadmark_packet_01/FRONT__rect/"
root_path = "/backup/manu_label_v2/ANNOTATION/lane_packet_01/FRONT_rect/"


# %% lint车道线
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        # check_obstacle_annotations(json_data)
        check_lane_annotation(json_data,file)

# %% lint路沿
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        # check_obstacle_annotations(json_data)
        check_road_boundary_annotation(json_data)

# %%
# check obstacle
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        # check_obstacle_annotations(json_data)
        check_obstacle_annotations(json_data, file)
# %% lint traffic light
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        # check_obstacle_annotations(json_data)
        check_traffic_light_annotations(json_data)
# %% lint traffic sign
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        check_traffic_sign_annotations(json_data)

# %% lint road arrow
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        check_road_arrow_annotations(json_data)
# %% lint lane
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        check_lane_annotation(json_data)

# %% lint road_boundary
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        check_road_boundary_annotation(json_data)

# %% lint stop line
for file in os.listdir(root_path):
    file = os.path.join(root_path, file)
    if file.endswith(".json"):
        with open(file, 'r') as f:
            json_data = json.load(f)
        check_stop_line_annotation(json_data)



# # %%
# for file in os.listdir(root_path):
#     file = os.path.join(root_path, file)
#     if file.endswith(".json"):
#         with open(file, 'r') as f:
#             json_data = json.load(f)
#         check_cross_walk_annotation(json_data)

# # %%
# for file in os.listdir(root_path):
#     file = os.path.join(root_path, file)
#     if file.endswith(".json"):
#         with open(file, 'r') as f:
#             json_data = json.load(f)
#         check_intersection_annotation(json_data)
# # %%

# %%
