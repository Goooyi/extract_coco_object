import cv2
import yaml
import time
import numpy as np

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
            "version": "1.0",
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
		    	"line": ["lane", "road_boundary", "stop_line", "cross_walk"]
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
            new_anno_entry = create_line_entry(instance, cam_name, is_lane)
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
    res = {
        "id": instance["id"],
        "category": instance["category"],
        "activity": instance["labelsObj"]["activity"],
        "visibility": instance["labelsObj"]["visibility"],
        "pointCount": instance["pointCount"]["lidar"],
        "truncated": [],
        "position": instance["position"],
        "dimension": instance["dimension"],
        "quaternion": instance["quaternion"]
    }
    # replace "."  with “_”
    res["category"] = res["category"].replace(".", "_")

    return res

def create_rect_entry(instance, cam_name, is_tfl):
    x = instance["children"][0]["cameras"][0]["frames"][0]["shape"]["x"]
    y = instance["children"][0]["cameras"][0]["frames"][0]["shape"]["y"]
    w = instance["children"][0]["cameras"][0]["frames"][0]["shape"]["width"]
    h = instance["children"][0]["cameras"][0]["frames"][0]["shape"]["height"]

    res = {
        "id": instance["id"],
        "cam_name": cam_name,
        "category": instance["attributes"]["type"] if "type" in instance["attributes"].keys() else "unknown",
        "occlusion": instance["attributes"]["occlusion"] if "occlusion" in instance["attributes"].keys() else "0",
        "truncated": instance["attributes"]["truncated"] if "truncated" in instance["attributes"].keys() else "0",
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
        direction = instance["attributes"]["direction"] if "direction" in instance["attributes"].keys() else instance["attributes"]["方向"]
        res["master_slave"] = 0
        res["color"] = instance["attributes"]["color"]
        res["direction"] = direction
    return res
def create_line_entry(instance, cam_name, is_lane):
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

    return res

def create_point_entry(instance, cam_name):
    cateName = "conflux" if instance["categoryName"] == "交汇点" else "split"
    if instance["categoryName"] != "交汇点":
        print(instance["categoryName"])
    res = {
        "id": instance["id"],
        "cam_name": cam_name,
        "category": cateName,
        "point": instance["children"][0]["cameras"][0]["frames"][0]["shape"]
    }
    return res

def correct_traffic_light(json_dict):
    if "traffic_light" not in json_dict["annotations"].keys():
        return json_dict

    ins = json_dict["annotations"]["traffic_light"]
    for i in range(len(ins)):
        # correct master-slave relationship, if a bbox cover other bbox, the bigger bbox is master and smaller box is slave
        for j in range(i+1, len(ins)):
            master_slave_state = check_master_slave(ins[i]["bbox"], ins[j]["bbox"])
            if master_slave_state == 1:
                ins[i]["master_slave"] = 1
                ins[j]["id"] = ins[i]["id"]
            elif master_slave_state == 2:
                ins[j]["master_slave"] = 1
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

def correct_vehicle_in_vehicle(json_dict, anns):
    vehicle_in_vehicle_list = []
    if "obstacle" not in json_dict["annotations"].keys():
        return json_dict
    for idx, item in enumerate(json_dict["annotations"]["obstacle"]):
        if item["category"] == "vehicle_vehicle_in_vehicle":
            vehicle_in_vehicle_list.append(idx)
    if len(vehicle_in_vehicle_list) == 0:
        return json_dict

    pool = []
    for item in anns["frames"][0]["relations"]:
        found = False
        fromm = item["from"]
        too = item["to"]
        for poo in pool:
            if fromm in poo:
                found = True
                poo.append(too)
            elif too in poo:
                found = True
                poo.append(fromm)

        if not found:
            pool.append([fromm, too])

    counter = 0
    for idx in vehicle_in_vehicle_list:
        master_id = find_3d_master(json_dict["annotations"]["obstacle"][idx]["id"], anns["frames"][0]["relations"], pool)
        if master_id:
            json_dict["annotations"]["obstacle"][idx]["id"] = master_id
            counter += 1
    if counter != len(vehicle_in_vehicle_list):
        print("counter: ", counter)
        print("vehicle_in_vehicle_list: ", len(vehicle_in_vehicle_list))
        raise ValueError("missmatch")
    return json_dict

def find_3d_master(id, relations, pool):
    found_pool = False
    target_idx = None
    for idx, item in enumerate(pool):
        if id in item:
            found_pool = True
            target_idx = idx
            break
    if found_pool:
        return pool[target_idx][0]
    else:
        raise ValueError("missmatch")
