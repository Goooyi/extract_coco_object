import os
import glob
import shutil
import json

from tqdm import tqdm
from utils import create_default_json, fill_img_camear_info, fill_2d_anno, fill_3d_anno, correct_traffic_light,correct_vehicle_in_vehicle

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

output_path = "/code/gn0/extract_coco_object/tmp_stageConvert"

files = glob.glob(os.path.join(img_path, '*.jpg'))
names = []
for i, file in enumerate(files):
    if i > 100:
        break
    name = file.split('/')[-1].strip('.jpg')
    names.append(name)


for i in tqdm(range(len(names))):
    name = names[i]
    # create new json
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
                    new_json = correct_vehicle_in_vehicle(new_json, anns)
        else:
            for subfolder in subfolder_2d:
                if os.path.exists(os.path.join(path, subfolder, name + '.json')):
                    with open(os.path.join(path, subfolder, name + '.json'), 'r') as f:
                        anns = json.load(f)

                    cam_name = subfolder.split('_rec')[0]
                    new_json = fill_2d_anno(new_json, anns, cam_name)

    # correct master-slave relationship of traffic_light
    new_json = correct_traffic_light(new_json)

    # save json
    with open(os.path.join(output_path, name + '.json'), 'w') as f:
        json.dump(new_json, f)