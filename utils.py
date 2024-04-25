import cv2
import yaml
import time
import numpy as np

def unixTime2Date(unixTime):
    if type(unixTime) == str:
        unixTime = int(unixTime)

    time1 =  time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(unixTime))
    # change time format to UTC/GMT+08:00
    time1 = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime(unixTime+8*3600))
    tmp = list(time1.split("-"))
    time2 = tmp[0] + tmp[1] + tmp[2]
    return time1, time2

def apply_mask(image, mask, alpha=0.5):
    """Apply the given mask to the image.
    """
    ic = image.copy()
    for c in range(3):
        ic[:, :, c] = np.where(mask[:,:,c] != 0,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * mask[:, :, c],
                                  image[:, :, c])
    # image = (1 - alpha) * image + alpha * mask
    return ic

def binary_masking(img, height, mask):
    pass

def create_default_json():
    default_json = {
        "info": {
            "format_version": "1.0",
            "description": "Exported from Stage 1 annotation",
            "contributor": "appen",
            "date_created": "2024-03-17 09:48:27"
        },
        "licenses": [
            {
              "name": "AXERA"
            }
        ],
        "categories": [
            {
                "3d_bbox": ["obstacle"]
            },
		    {
		    	"rect":["traffic_sign", "traffic_light", "road_arrow"]
		    },
		    {
		    	"line": ["lane", "road_boundary", "stop_line", "cross_walk", "no_parking_area"]
		    },
		    {
		    	"point": ["intersection"]
		    }
        ],
        "images": {},
        "annotations": {
        }
    }
    default_json["info"]["date_created"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return default_json

def fill_img_camear_info(json_dict, carid, img_name, sensor_file_path):
    img_entry = {
        "frame_name": carid + "_" + img_name,
        "lidar_calibration": [],
        "camera_info": []
    }
    # read sensor's yaml file to a dict
    with open(sensor_file_path, "r") as f:
        sensor_data = yaml.load(f, Loader=yaml.FullLoader)
        for lidar_config in sensor_data['lidar']:
            # check if string has "middle" in it
            if lidar_config["lidar_config"]["frame_id"].find("middle") != -1:
                img_entry["lidar_calibration"] = lidar_config["lidar_config"]["tovcs"]
                break
        for camera_config in sensor_data['camera']:
            img_entry["camera_info"].append({
                "frame_id": camera_config["camera_config"]["frame_id"],
                "width": camera_config["camera_config"]["width"],
                "height": camera_config["camera_config"]["height"],
                "calibration": {
                    "pose": camera_config["camera_config"]["pose"],
                    "tovcs": camera_config["camera_config"]["tovcs"],
                    "intrinsics": camera_config["camera_config"]["intrinsics"],
                    "distortion": camera_config["camera_config"]["distortion"]
                }
            })

    json_dict["images"] = img_entry

    return json_dict

def fill_2d_anno(json_dict, anns, cam_name):
    for instance in anns["instances"]:
        # chekc if key exist
        if instance["category"] not in json_dict["annotations"].keys():
            json_dict["annotations"][instance["category"]] = []

        if instance["category"] in ["traffic_sign", "traffic_light", "road_arrow"]:
            is_tfl = True if instance["category"] == "traffic_light" else False
            new_anno_entry = create_rect_entry(instance, cam_name, is_tfl)
        elif instance["category"] in ["lane", "road_boundary", "stop_line", "cross_walk"]:
            is_lane = True if instance["category"] == "lane" else False
            is_road_boundary = True if instance["category"] == "road_boundary" else False
            new_anno_entry = create_line_entry(instance, cam_name, is_lane, is_road_boundary)
        elif instance["category"] in ["intersection"]:
            new_anno_entry = create_point_entry(instance, cam_name)

        json_dict["annotations"][instance["category"]].append(new_anno_entry)
    return json_dict


def fill_3d_anno(json_dict, anns):
    if "obstacle" not in json_dict["annotations"].keys():
        json_dict["annotations"]["obstacle"] = []

    for instance in anns["frames"][0]["items"]:
        new_anno_entry = create_3dbbox_entry(instance)
        json_dict["annotations"]["obstacle"].append(new_anno_entry)

    return json_dict

def create_3dbbox_entry(instance):

    activity = instance["labelsObj"]["activity"] if instance["labelsObj"] is not None else None
    visibility = instance["labelsObj"]["visibility"] if instance["labelsObj"] is not None else None
    res = {
        "id": instance["id"],
        "category": instance["category"],
        "activity": activity,
        "visibility": visibility,
        "pointCount": instance["pointCount"]["lidar"],
        "truncated": [],
        "position": instance["position"],
        "dimension": instance["dimension"],
        "quaternion": instance["quaternion"],
        "taillight": {
					"left": {
						"occlusion": "",
						"status": ""
					},
					"right": {
						"occlusion": "",
						"status": ""
					},
					"brake": {
						"occlusion": "",
						"status": ""
					}

				},
        "wheel": {
					"left_front": {
						"occlusion": "",
                        "bbox": [
                            {
                                "x": 999999,
                                "y": 999999
                            },
                            {
                                "x": 999999,
                                "y": 999999
                            }
                        ]
					},
					"left_middle": {
						"occlusion": "",
                        "bbox": [
                            {
                                "x": 999999,
                                "y": 999999
                            },
                            {
                                "x": 999999,
                                "y": 999999
                            }
                        ]
					},
					"left_back": {
						"occlusion": "",
                        "bbox": [
                            {
                                "x": 999999,
                                "y": 999999
                            },
                            {
                                "x": 999999,
                                "y": 999999
                            }
                        ]
					},
					"right_front": {
						"occlusion": "",
                        "bbox": [
                            {
                                "x": 999999,
                                "y": 999999
                            },
                            {
                                "x": 999999,
                                "y": 999999
                            }
                        ]
					},
					"right_middle": {
						"occlusion": "",
                        "bbox": [
                            {
                                "x": 999999,
                                "y": 999999
                            },
                            {
                                "x": 999999,
                                "y": 999999
                            }
                        ]
					},
					"right_back": {
						"occlusion": "",
                        "bbox": [
                            {
                                "x": 999999,
                                "y": 999999
                            },
                            {
                                "x": 999999,
                                "y": 999999
                            }
                        ]
					}
				},
        "wheel_point": {
					"left_front": {
						"occlusion": "",
						"point": {
							"x": 999999,
							"y": 999999
                 		}
					},
					"left_back": {
						"occlusion": "",
						"point": {
							"x": 999999,
							"y": 999999
                 		}
					},
					"right_front": {
						"occlusion": "",
						"point": {
							"x": 999999,
							"y": 999999
                 		}
					},
					"right_back": {
						"occlusion": "",
						"point": {
							"x": 999999,
							"y": 999999
                 		}
					},
					"front": {
						"occlusion": "",
						"point": {
							"x": 999999,
							"y": 999999
                 		}
					},
					"back": {
						"occlusion": "",
						"point": {
							"x": 999999,
							"y": 999999
                 		}
					}
				}
    }
    # replace "."  with “_”
    res["category"] = res["category"].replace(".", "_")

    return res

def create_rect_entry(instance, cam_name, is_tfl):
    x = instance["children"][0]["cameras"][0]["frames"][0]["shape"]["x"]
    y = instance["children"][0]["cameras"][0]["frames"][0]["shape"]["y"]
    w = instance["children"][0]["cameras"][0]["frames"][0]["shape"]["width"]
    h = instance["children"][0]["cameras"][0]["frames"][0]["shape"]["height"]

    category = ""
    occlusion = ""
    truncated = ""
    if instance["attributes"]:
        category = instance["attributes"]["type"] if "type" in instance["attributes"].keys() else "unknown"
        occlusion = instance["attributes"]["occlusion"] if "occlusion" in instance["attributes"].keys() else "0"
        truncated = instance["attributes"]["truncated"] if "truncated" in instance["attributes"].keys() else "0"
    res = {
        "id": instance["id"],
        "cam_name": cam_name,
        "category": category,
        "occlusion": occlusion,
        "truncated": truncated,
        "bbox": [{
                    "x": x,
                    "y": y
                    },
                 {
                    "x": x+w,
                    "y": y+h
                 }
                 ]
    }
    if is_tfl:
        direction_cn = instance["attributes"]["方向"] if "方向" in instance["attributes"].keys() else None
        direction = instance["attributes"]["direction"] if "direction" in instance["attributes"].keys() else direction_cn
        res["master_slave"] = 0
        color = instance["attributes"]["color"] if "color" in instance["attributes"].keys() else None
        res["color"] = color
        res["direction"] = direction
    return res
def create_line_entry(instance, cam_name, is_lane, is_road_boundary):
    points = []
    for point in instance["children"][0]["cameras"][0]["frames"][0]["shape"]["points"]:
        tmp_p = {
            "x": point["x"],
            "y": point["y"],
            "z": 0,
            "occ": 1 if "userData" in point.keys() else 0
        }

        points.append(tmp_p)
    res = {
        "cam_name": cam_name,
        "id": instance["id"],
        "points": points
    }
    if is_lane:
        res["category"] = instance["attributes"]["linetype"]
        res["color"] = instance["attributes"]["color"]
    if is_road_boundary:
        res["texture"] = ""

    return res

def create_point_entry(instance, cam_name):
    # cateName = "conflux" if instance["categoryName"] == "交汇点" else "split"
    if instance["attributes"]["id"]=='0':
        cateName = "conflux"
    elif instance["attributes"]["id"] == "1":
        cateName = "split"
    else:
        raise ValueError("F**")
    # if instance["categoryName"] != "交汇点":
    #     print(instance["categoryName"])
    res = {
        "id": instance["id"],
        "cam_name": cam_name,
        "category": cateName,
        "point": instance["children"][0]["cameras"][0]["frames"][0]["shape"],
        "constitute": []
    }
    return res

def correct_traffic_light(json_dict):
    if "traffic_light" not in json_dict["annotations"].keys():
        return json_dict

    ins = json_dict["annotations"]["traffic_light"]
    visited = [0] * len(ins)
    for i in range(len(ins)):
        if visited[i] == 1:
            continue
        visited[i] = 1
        # correct master-slave relationship, if a bbox cover other bbox, the bigger bbox is master and smaller box is slave
        for j in range(i+1, len(ins)):
            master_slave_state = check_master_slave(ins[i]["bbox"], ins[j]["bbox"])
            if master_slave_state == 1:
                ins[j]["master_slave"] = 1
                ins[j]["id"] = ins[i]["id"]
                visited[j] = 1
            elif master_slave_state == 2:
                ins[i]["master_slave"] = 1
                ins[i]["id"] = ins[j]["id"]


    json_dict["annotations"]["traffic_light"] = ins
    return json_dict


def check_master_slave(bbox1, bbox2):
    """
    return 0 if bbox is not iside of each other
    return 1 if bbox2 is inside bbox1
    return 2 if bbox1 is inside bbox2
    """
    if bbox1[0]["x"] < bbox2[0]["x"] and bbox1[0]["y"] < bbox2[0]["y"] and bbox1[1]["x"] > bbox2[1]["x"] and bbox1[1]["y"] > bbox2[1]["y"]:
        return 1
    elif bbox2[0]["x"] < bbox1[0]["x"] and bbox2[0]["y"] < bbox1[0]["y"] and bbox2[1]["x"] > bbox1[1]["x"] and bbox2[1]["y"] > bbox1[1]["y"]:
        return 2
    else:
        return 0

def correct_vehicle_in_vehicle(json_dict):
    vehicle_in_vehicle_list = []
    if "obstacle" not in json_dict["annotations"].keys():
        return json_dict
    for idx, item in enumerate(json_dict["annotations"]["obstacle"]):
        if item["category"] == "vehicle_vehicle_in_vehicle":
            vehicle_in_vehicle_list.append(idx)
    if len(vehicle_in_vehicle_list) == 0:
        return json_dict

    total_list = json_dict["annotations"]["obstacle"]

    visited = [0] * len(vehicle_in_vehicle_list)
    for idx, target in enumerate(vehicle_in_vehicle_list):
        if visited[idx] == 1:
            continue
        visited[idx] = 1
        master_idx = find_3d_master(target, vehicle_in_vehicle_list, total_list)
        if master_idx != -1:
            visited[master_idx] = 1
            master_item = vehicle_in_vehicle_list[master_idx]
            json_dict["annotations"]["obstacle"][target]["id"] = json_dict["annotations"]["obstacle"][master_item]["id"]


    if sum(visited) != len(vehicle_in_vehicle_list):
        raise ValueError(f"missmatch, vehicle_in_vehicle_list: {len(vehicle_in_vehicle_list)}, counter: {sum(visited)} ")
    return json_dict

def find_3d_master(target, vehicle_in_vehicle_list, total_list):
    max_ratio = -1
    max_idx = -1
    for idx, item in enumerate(vehicle_in_vehicle_list):
            ratio = check3DboxIOU(target, item, total_list)
            if ratio > max_ratio:
                max_ratio = ratio
                max_idx = idx

    return max_idx

def check3DboxIOU(item1, item2, total_list):
    bbox1 = [total_list[item1]["position"]["x"] - total_list[item1]["dimension"]["x"]/2,
             total_list[item1]["position"]["x"] + total_list[item1]["dimension"]["x"]/2,
             total_list[item1]["position"]["y"] - total_list[item1]["dimension"]["y"]/2,
             total_list[item1]["position"]["y"] + total_list[item1]["dimension"]["y"]/2,
             total_list[item1]["position"]["z"] - total_list[item1]["dimension"]["z"]/2,
             total_list[item1]["position"]["z"] + total_list[item1]["dimension"]["z"]/2
             ]
    bbox2 = [total_list[item2]["position"]["x"] - total_list[item2]["dimension"]["x"]/2,
             total_list[item2]["position"]["x"] + total_list[item2]["dimension"]["x"]/2,
             total_list[item2]["position"]["y"] - total_list[item2]["dimension"]["y"]/2,
             total_list[item2]["position"]["y"] + total_list[item2]["dimension"]["y"]/2,
             total_list[item2]["position"]["z"] - total_list[item2]["dimension"]["z"]/2,
             total_list[item2]["position"]["z"] + total_list[item2]["dimension"]["z"]/2
             ]
    if AincludeB(bbox2, bbox1):
        # return area ratio
        area_box1 = total_list[item1]["dimension"]["x"] * total_list[item1]["dimension"]["y"] * total_list[item1]["dimension"]["z"]
        area_box2 = total_list[item2]["dimension"]["x"] * total_list[item2]["dimension"]["y"] * total_list[item2]["dimension"]["z"]
        return area_box2 / area_box1
    else:
        return -1


def AincludeB(bbox1, bbox2):
    # xyz
    if bbox1[0] < bbox2[0] and bbox1[1] > bbox2[1] and bbox1[2] < bbox2[2] and bbox1[3] > bbox2[3] and bbox1[4] < bbox2[4] and bbox1[5] > bbox2[5]:
        return True
    return False