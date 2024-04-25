import os
import json
import re

def check_all_id_diff_with_master_slave_and_frame_name_patter(json_root):
    slave_set = set()
    id_set = set()
    json_files = []

    for json_file in os.listdir(json_root):
        json_file = os.path.join(json_root, json_file)
        if json_file.endswith(".json"):
            json_files.append(json_file)

    for json_file in json_files:
        with open(json_file, 'r') as f:
            json_data = json.load(f)
        # check frame name pattern like Regular expression "*_*.*"
        pattern = r'.*_.+\..+'
        if not re.match(pattern, json_data["images"]["frame_name"]):
            raise ValueError(f"frame name pattern not match: {json_data['images']['frame_name']}")

        # check if id is unique, 3D obstacle may have same id when they are overlapped in camera view
        # if "obstacle" in json_data["annotations"].keys():
        #     for ann in json_data["annotations"]["obstacle"]:
        #         if ann["id"] in id_set:
        #             raise ValueError(f"duplicate id: {ann['id']}")
        #         id_set.add(ann["id"])

        if "traffic_sign" in json_data["annotations"].keys():
            for ann in json_data["annotations"]["traffic_sign"]:
                if ann["id"] in id_set:
                    raise ValueError(f"duplicate id: {ann['id']}")
                id_set.add(ann["id"])

        if "traffic_light" in json_data["annotations"].keys():
            for ann in json_data["annotations"]["traffic_light"]:
                if ann["master_slave"] == 1:
                    slave_set.add(ann["id"])
                    continue
                if ann["id"] in id_set:
                    raise ValueError(f"duplicate id: {ann['id']}")
                id_set.add(ann["id"])

        # check if all item in slave set also in master set
        for id in slave_set: # id is not in
            if id not in id_set:
                raise ValueError(f"id {id} not in master set")

        if "road_arrow" in json_data["annotations"].keys():
            for ann in json_data["annotations"]["road_arrow"]:
                if ann["id"] in id_set:
                    raise ValueError(f"duplicate id: {ann['id']}")
                id_set.add(ann["id"])

        if "lane" in json_data["annotations"].keys():
            for ann in json_data["annotations"]["lane"]:
                if ann["id"] in id_set:
                    raise ValueError(f"duplicate id: {ann['id']}")
                id_set.add(ann["id"])


        if "road_boundary" in json_data["annotations"].keys():
            for ann in json_data["annotations"]["road_boundary"]:
                if ann["id"] in id_set:
                    raise ValueError(f"duplicate id: {ann['id']}")
                id_set.add(ann["id"])


        if "stop_line" in json_data["annotations"].keys():
            for ann in json_data["annotations"]["stop_line"]:
                if ann["id"] in id_set:
                    raise ValueError(f"duplicate id: {ann['id']}")
                id_set.add(ann["id"])

        if "cross_walk" in json_data["annotations"].keys():
            for ann in json_data["annotations"]["cross_walk"]:
                if ann["id"] in id_set:
                    raise ValueError(f"duplicate id: {ann['id']}")
                id_set.add(ann["id"])

        if "no_parking_area" in json_data["annotations"].keys():
            for ann in json_data["annotations"]["no_parking_area"]:
                if ann["id"] in id_set:
                    raise ValueError(f"duplicate id: {ann['id']}")
                id_set.add(ann["id"])


        if "intersection" in json_data["annotations"].keys():
            for ann in json_data["annotations"]["intersection"]:
                if ann["id"] in id_set:
                    raise ValueError(f"duplicate id: {ann['id']}")
                id_set.add(ann["id"])


def check_obstacle_annotations(json_data, file_name):
    obstacle_anno_keys = ["id",
                          "category",
                          "activity",
                          "visibility",
                          "pointCount",
                          "truncated",
                          "position",
                          "dimension",
                          "quaternion",
                          "taillight",
                          "wheel",
                          "wheel_point",
                          "rect"
                          ]

    for anno in json_data["annotations"]["obstacle"]:
        for key in anno.keys():
            if key not in obstacle_anno_keys:
                raise ValueError(f"key {key} not in {obstacle_anno_keys} for {file_name}")
            # if key in ["category", "activity"]:
            #     # check key is seperated by "_" not by "."
            #     if "_" not in anno[key]:
            #         raise ValueError(f"key: {key} for {anno[key]} should be seperated by '_' not by '.'")

            # if key == "visibility":
            #     if anno[key] not in ["0%", "0%-30%", "30%-50%", "50%-100%", "100%"]:
            #         raise ValueError(f"value for key {key} should be in [0%, 0%-30%, 30%-50%, 50%-100%, 100%], but got {anno[key]}")

            if key == "taillight":
                for sub_keys in anno[key].keys():
                    if "occlusion" in anno[key][sub_keys].keys():
                        if anno[key][sub_keys]["occlusion"] not in ["true", "false"]:
                            raise ValueError(f"value for key {key}-{sub_keys}-occlusion should be in [True, False], but got {anno[key][sub_keys]['occlusion']} of type: {type(anno[key][sub_keys]['status'])}")
                    if "status" in anno[key][sub_keys].keys():
                        if anno[key][sub_keys]["status"] not in ["true", "false", "unknown"]:
                            raise ValueError(f"value for key {key}-{sub_keys}-status should be in [True, False, 'unknown'], but got {anno[key][sub_keys]['status']} of type: {type(anno[key][sub_keys]['status'])}")

            if key == "wheel":
                for sub_keys in anno[key].keys():
                    if "occlusion" in anno[key][sub_keys].keys():
                        if anno[key][sub_keys]["occlusion"] not in ["true", "false", "unknown"]:
                            raise ValueError(f"value for key {key}-{sub_keys}-occlusion should be in [True, False, 'unknown'] but got {anno[key][sub_keys]['status']}")

            if key == "wheel_point":
                for sub_keys in anno[key].keys():
                    if "occlusion" in anno[key][sub_keys].keys():
                        if anno[key][sub_keys]["occlusion"] not in ["true", "false", "unknown"]:
                            raise ValueError(f"value for key {key}-{sub_keys}-occlusion should be in [True, False, 'unknown'] but got {anno[key][sub_keys]['status']}")



def check_traffic_light_annotations(json_data):
    traffic_light_keys = ["id",
                         "cam_name",
                         "master_slave",
                         "category",
                         "occlusion",
                         "truncated",
                         "bbox",
                         "color",
                         "direction"]
    traffic_light_category = ["box",
                             "light",
                             "pedestrian",
                             "cyclist",
                             "straight",
                             "left",
                             "right",
                             "u-turn",
                             "unknown"]

    traffic_light_color = ["red",
                          "yellow",
                          "green",
                          "black",
                          "unknown"]

    if "traffic_light" in json_data["annotations"].keys():
        for anno in json_data["annotations"]["traffic_light"]:
            for key in anno.keys():
                if key not in traffic_light_keys:
                    raise ValueError(f"key {key} not in {traffic_light_keys}")
                if key == "category":
                    if anno[key] not in traffic_light_category:
                        raise ValueError(f"value for key {key} should be in {traffic_light_category}, but got {anno[key]}")

                if key == "occlusion" or key == "truncated":
                    if anno[key] not in [0, 1]:
                        raise ValueError(f"value for key {key} should be in [0,1], but got {anno[key]}")

                if key == "color":
                    if anno[key] not in traffic_light_color:
                        raise ValueError(f"value for key {key} should be in {traffic_light_color}")

                if key == "direction":
                    if anno[key] not in [0, 1]:
                        raise ValueError(f"value for key {key} should be in [0,1]")

                if key == "master_slave":
                    if anno[key] not in [0, 1]:
                        raise ValueError(f"value for key {key} should be in [0,1]")

def match_tfs_patterns(strrr):
    if strrr == "unknown" or strrr == "other":
        return True
    patterns = [r'^pl.*', r'^pr.*', r'^p.*', r'^i.*']

    for pattern in patterns:
        if re.match(pattern, strrr):
            return True

    return False
def check_traffic_sign_annotations(json_data):
    traffic_sign_keys = ["id",
                         "cam_name",
                         "category",
                         "occlusion",
                         "truncated",
                         "bbox"
                         ]

    if "traffic_sign" in json_data["annotations"].keys():
        for anno in json_data["annotations"]["traffic_sign"]:
            for key in anno.keys():
                if key not in traffic_sign_keys:
                    raise ValueError(f"key {key} not in {traffic_sign_keys}")
                if key == "category":
                    if not match_tfs_patterns(anno[key]):
                        raise ValueError(f"traffic sign's category not match pre-defined, got {anno[key]}")

                if key == "occlusion" or key == "truncated":
                    if anno[key] not in [0, 1]:
                        raise ValueError(f"value for key {key} should be in [0,1], but got {anno[key]}")

                if key == "master_slave":
                    if anno[key] not in [0, 1]:
                        raise ValueError(f"value for key {key} should be in [0,1]")


def check_road_arrow_annotations(json_data):
    road_arrow_keys = ["id",
                       "cam_name",
                       "category",
                       "occlusion",
                       "truncated",
                       "bbox"
                       ]

    road_arrow_category = ["straight",
                           "straight_left",
                           "left",
                           "right",
                           "straight_right",
                           "u-turn",
                           "straight_u-turn",
                           "left_u-turn",
                           "left_right",
                           "left_bend",
                           "right_bend",
                           "unknown"]

    if "road_arrow" in json_data["annotations"].keys():
        for anno in json_data["annotations"]["road_arrow"]:
            for key in anno.keys():
                if key not in road_arrow_keys:
                    raise ValueError(f"key {key} not in {road_arrow_keys}")
                if key == "category":
                    if anno[key] not in road_arrow_category:
                        raise ValueError(f"value for key {key} should be in {road_arrow_category}")
                elif key == "occlusion" or key == "truncated":
                    if anno[key] not in [0, 1]:
                        raise ValueError(f"value for key {key} should be in [0,1], but got {anno[key]}")


def check_sequence(sequence):
    for i in range(len(sequence)):
        if sequence[i] == 2:
            if i == 0 or sequence[i-1] not in [1, 2, 4]:
                return False
            if i == len(sequence) - 1 or sequence[i+1] not in [2, 3, 4]:
                return False
    return True
def check_lane_annotation(json_data, file_name):
    lane_keys = ["cam_name", "category", "color", "lane_id", "id", "points"]
    lane_category = ["solid", "dashed", "double_solid","double_dashed","solid_dashed","dashed_solid", "unknown"]
    lane_color = ["white", "yellow", "blue", "unknown"]
    lane_id_set = set()
    lane_point_occ = [0,1,2,3,4]


    if "lane" in json_data["annotations"].keys():
        for anno in json_data["annotations"]["lane"]:
            for key in anno.keys():
                if key not in lane_keys:
                    raise ValueError(f"key {key} not in {lane_keys}")
                if key == "category":
                    if anno[key] not in lane_category:
                        raise ValueError(f"value for key {key} should be in {lane_category}")
                elif key == "color":
                    if anno[key] not in lane_color:
                        raise ValueError(f"value for key {key} should be in {lane_color}")
                # elif key == "lane_id":
                #     if anno[key] in lane_id_set:
                #         raise ValueError(f"value for key {key} should be unique")
                #     else:
                #         lane_id_set.add(anno[key])
                elif key == "points":
                    occ1_count = 0
                    occ2_count = 0
                    occ_sequence= []
                    for point in anno[key]:
                        occ_sequence.append(point["occ"])
                        if point["occ"] not in lane_point_occ:
                            raise ValueError(f"value for key {key} should be in {lane_point_occ}")
                        if point["occ"] == 1:
                            occ1_count += 1
                        elif point["occ"] == 3:
                            occ2_count += 1
                    if occ1_count != occ2_count:
                        raise ValueError(f"key {key} should have the same number of occ = 1 and occ = 3, but got total {occ1_count}  of occ = 1 and {occ2_count}  of occ = 3")
                    if not check_sequence(occ_sequence):
                        raise ValueError(f"value for key {key} should be a sequence of 1,2,..2,3. number 2 appears but not in proper position for file {file_name}, the given sequence is {occ_sequence}")


def check_road_boundary_annotation(json_data):
    road_boundary_keys = ["id",
                          "cam_name",
                          "texture",
                          "points"]
    road_boundary_texture = ["grass",
                             "curb",
                             "handrail",
                             "wall",
                             "sandstone",
                             "grassland",
                             "water_safety_barriers",
                             "other"]

    road_boundary_occ_type = [0,1,2,3]

    if "road_boundary" in json_data["annotations"].keys():
        for anno in json_data["annotations"]["road_boundary"]:
            for key in anno.keys():
                if key not in road_boundary_keys:
                    raise ValueError(f"key {key} not in {road_boundary_keys}")
                if key == "texture":
                    if anno[key] not in road_boundary_texture:
                        raise ValueError(f"value for key {key} should be in {road_boundary_texture}, but got {anno[key]}")
                elif key == "points":
                    for point in anno[key]:
                        if point["occ"] not in road_boundary_occ_type:
                            raise ValueError(f"value for key {key} should be in {road_boundary_occ_type}")

def check_stop_line_annotation(json_data):
    stop_line_keys = ["id",
                          "cam_name",
                          "points"]
    stop_line_occ_type = [0,1,2,3]

    if "stop_line" in json_data["annotations"].keys():
        for anno in json_data["annotations"]["stop_line"]:
            for key in anno.keys():
                if key not in stop_line_keys:
                    raise ValueError(f"key {key} not in {stop_line_keys}")
                if key == "points":
                    for point in anno[key]:
                        if point["occ"] not in stop_line_occ_type:
                            raise ValueError(f"value for key {key} should be in {stop_line_occ_type}")

def check_cross_walk_annotation(json_data):
    cross_walk_keys = ["id",
                          "cam_name",
                          "points"]

    cross_walk_occ_type = [0,1,2,3]

    if "cross_walk" in json_data["annotations"].keys():
        for anno in json_data["annotations"]["cross_walk"]:
            for key in anno.keys():
                if key not in cross_walk_keys:
                    raise ValueError(f"key {key} not in {cross_walk_keys}")
                if key == "points":
                    for point in anno[key]:
                        if point["occ"] not in cross_walk_occ_type:
                            raise ValueError(f"value for key {key} should be in {cross_walk_occ_type}")


def check_intersection_annotation(json_data):
    intersection_keys = ["id",
                          "cam_name",
                          "points",
                          "category"]

    intersection_category = ["conflux_point", "split_point"]


    if "intersection" in json_data["annotations"].keys():
        for anno in json_data["annotations"]["intersection"]:
            for key in anno.keys():
                if key not in intersection_keys:
                    raise ValueError(f"key {key} not in {intersection_keys}")
                if key == "category":
                    if anno[key] not in intersection_category:
                        raise ValueError(f"value for key {key} should be in {intersection_category}, but got {anno[key]}")