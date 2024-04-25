import os
import glob
import shutil
import json

from tqdm import tqdm
from utils import create_default_json, fill_img_camear_info, fill_2d_anno, fill_3d_anno, correct_traffic_light,correct_vehicle_in_vehicle,unixTime2Date

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

print(names[:3])