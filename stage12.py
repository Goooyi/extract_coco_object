import os
import glob
import shutil
import json

from tqdm import tqdm
from utils import create_default_json, fill_img_camear_info, fill_2d_anno, fill_3d_anno, correct_traffic_light,correct_vehicle_in_vehicle,unixTime2Date

bad_count01 = 0
bad_count02 = 0

frame_set = set()

carid = "001"
sensor_file_path = "/code/gn0/extract_coco_object/sensor.yaml"
# reading all files name in one folder
root = '/data/dataset/aXcellent/manu-label/axera_manu_v1.0/'
img_path = root + 'IMAGE/FRONT_WIDE_rect'
obstacle_path = root + 'ANNOTATION'
lane_path = root + 'ANNOTATION_LANE'
roadmark_path = root + 'ANNOTATION_ROADMARK'
traffic_path = root + 'ANNOTATION_TRAFFIC'
anno_paths = [obstacle_path, lane_path, roadmark_path, traffic_path]
subfolder_2d = ["FRONT_WIDE_rect", "FRONT_rect"]

# backup_raw_folder = "/backup/raw/v1/xcap001/"
backup_raw_folder = "/data/dataset/aXcellent/manu-label/manu_label_data"
output_path = "/data/dataset/aXcellent/manu-label/v1/xcap001/"

files = glob.glob(os.path.join(img_path, '*.jpg'))
names = []
for i, file in enumerate(files):
    # if i > 1000:
    #     break
    name = file.split('/')[-1].strip('.jpg')
    names.append(name)
    names.sort()

back_up_folder = backup_raw_folder
# list all folder name in back_up_folder
bag_ids = os.listdir(back_up_folder)
bag_ids.sort()

for i in tqdm(range(len(names))):
    name = names[i]
    new_json = create_default_json()
    # every image definitely have one json file
    new_json = fill_img_camear_info(new_json, carid, name, sensor_file_path)

    for path in anno_paths:
        # find if same name appears in current path
        if path.endswith('ANNOTATION'):
            if os.path.exists(os.path.join(path, name + '.json')):
                if os.path.exists(os.path.join(path, name + '.json')):
                    with open(os.path.join(path, name + '.json'), 'r') as f:
                        anns = json.load(f)

                    new_json = fill_3d_anno(new_json, anns)
                    new_json = correct_vehicle_in_vehicle(new_json)
        else:
            for subfolder in subfolder_2d:
                if os.path.exists(os.path.join(path, subfolder, name + '.json')):
                    with open(os.path.join(path, subfolder, name + '.json'), 'r') as f:
                        anns = json.load(f)

                    cam_name = subfolder.split('_rec')[0]
                    new_json = fill_2d_anno(new_json, anns, cam_name)

    # correct master-slave relationship of traffic_light
    new_json = correct_traffic_light(new_json)

    bag_id, bag_date = unixTime2Date(name.split('.')[0])
    # find if a folder named as bag_id exists in target folder
    # print(bag_date, bag_id)
    # back_up_folder = os.path.join(backup_raw_folder, bag_date)
    # find the nearest bag_id to our bag_id
    target = 0
    for idx, bid in enumerate(bag_ids):
        if bag_id <= bid:
            target = idx - 1
            break
    if target < 0:
        raise ValueError("F** for")
    if target == 0 and bag_id >= bag_ids[-1]:
        target = -1
    bag_id = bag_ids[target]
    # date_folder = os.path.json(output_path,bag_date)
    # list all folder name in date_folder
    real_bag_id = bag_ids[target]
    real_bag_id_candidate = bag_ids[target - 1]
    real_bag_id_candidate_01 = bag_ids[target - 2]

    should_exist_00 = os.path.join(back_up_folder, real_bag_id, "FRONT", name + ".jpg")
    should_exist_01 = os.path.join(back_up_folder, real_bag_id_candidate, "FRONT", name + ".jpg")
    should_exist_02 = os.path.join(back_up_folder, real_bag_id_candidate_01, "FRONT", name + ".jpg")

    found = False
    candidate = [should_exist_00, should_exist_01, should_exist_02]
    for idx, path in enumerate(candidate):
        if os.path.exists(path):
            found = True
            if idx == 0:
                break
            elif idx == 1:
                bad_count01 += 1
                if os.path.exists(os.path.join(output_path, bag_date, real_bag_id, "ANNOTATION_manu", name + ".json")):
                    bad_count02 += 1
                    os.remove(os.path.join(output_path, bag_date, real_bag_id, "ANNOTATION_manu", name + ".json"))
                real_bag_id = real_bag_id_candidate
                break
            else:
                real_bag_id = real_bag_id_candidate_01
                break
    if not found:
        raise ValueError(f"F** not found for {name}, suppose bag_id is {real_bag_id} {real_bag_id_candidate} {real_bag_id_candidate_01}")

    bag_id = real_bag_id

    # save json
    final_outpath = os.path.join(output_path, bag_date, bag_id, "ANNOTATION_manu")
    #create folder for final_outpath with parent if not exit:
    if not os.path.exists(final_outpath):
        os.makedirs(final_outpath)
    # save json
    # with open(os.path.join(output_path, bag_date, bag_id, "ANNOTATION_manu", name + '.json'), 'w') as f:
    #     json.dump(new_json, f)

print(f"{bad_count01} {bad_count02}")