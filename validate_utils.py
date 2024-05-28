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
    patterns = [r'p[1234567]',r'pnl', r'pn', r'pl\d\d?', r'ph\d\.?\d?'
                , r'pw\d\.?\dm', r'pa\d\d?t', r'pm\d\d?t'
                , r'ps', r'pne', r'i\d[0,1,2]?', r'il\d\d', r'pr\d\d'
                , r'p_other', r'i_other']
                # , r'pm 49t', r'pa14', r'pm49', r'pm4.9t', r'pa13', r'ph未知', r'pm30', r'pw49t', r'pw30t', r'pl 5m', r'pm40', r'il 50', r'pl 80', r'pm20T', r'pl未知']
    # signs = set(["p1", "p2", "p3", "p4", "p5", "p6", "p7"
    #             , "pn", "pnl", "pl10", "pl20", "pl30"
    #             , "pl25","pl15", "pl35", "pl45", "pl55"
    #             , "pl40", "pl50", "pl60", "pl70", "pl80"
    #             , "pl90", "pl100", "pl110", "pl120", "pl130"
    #             , "ph0.5m", "ph1.2m", "ph1.5m", "ph1.6m"
    #             , "ph1m", "ph2m", "ph3m", "ph4m"
    #             , "ph1.8m", "ph2.0m", "ph2.5m", "ph3.0m", "ph3.5m"
    #             , "ph4m", "ph4.5m", "ph5m", "ph5.5m", "ph6m"
    #             , "pw0.5", "pw1.2", "pw1.6", "pw1.8", "pw2.0"
    #             , "pm0.5t", "pm1.2t", "pm1.6t", "pm1.8t", "pm2.0t"
    #             , "pm2.5t", "pm3.0t", "pm3.5t", "pm5t"
    #             , "pa0.5t", "pa1.2t", "pa1.6t", "pa1.8t", "pa2.0t"
    #             , "pa2.5t", "pa3.0t", "pa3.5t", "pa5t"
    #             , "pa6t",  "pa8t",  "pa10t", "pa12t", "pa15t"
    #             , "pa7t", "pa13t", "pa15t"
    #             , "pa16t", "pa18t", "pa20t", "pa22t", "pa24t"
    #             , "pa25t", "pa30t", "pa35t", "pa40t", "pa45t"
    #             , "pm6t", "pm8t", "pm10t", "pm12t", "pm15t"
    #             , "pm16t", "pm18t", "pm20t", "pm22t", "pm24t"
    #             , "pm25t", "pm30t", "pm35t", "pm40t", "pm45t"
    #             , "ps", "pne", "i1", "i2", "i3", "i4"
    #             , "i5", "i6", "i7", "i8", "i9", "i10"
    #             , "i11", "i12", "il5", "il10", "il15"
    #             , "il15", "il20", "il25", "il30", "il35"
    #             , "il40", "il45", "il50", "il55", "il60"
    #             , "il65", "il70", "il75", "il80", "il85"
    #             , "pr5", "pr15", "pr10"
    #             , "pr15", "pr20", "pr25", "pr30", "pr35"
    #             , "pr40", "pr45", "pr50", "pr55", "pr60"
    #             , "pr65", "pr70", "pr75", "pr80", "pr85"
    #             , "p_other", "i_other"])

    for pattern in patterns:
        if re.match(pattern, strrr):
            return True
    # if strrr in signs:
    #     return True

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