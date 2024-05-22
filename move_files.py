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
v2_file_path = "/backup/manu_label_v2/"
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
                        , "ANNOTATION"]

# 先整合两个frame文件夹, 用来之后找到单帧frame具体放在哪个文件夹
source_frame_path = "/backup/v2_extract/"
target_frame_path = "/data/dataset/aXcellent/manu-label/v2/xcap001/"
bag_ids_source = os.listdir(source_frame_path)
bag_ids_target = []
for sub_folder in os.listdir(target_frame_path):
    if not os.path.isdir(os.path.join(target_frame_path, sub_folder)):
        continue
    to_extend = os.listdir(os.path.join(target_frame_path, sub_folder))
    bag_ids_target.extend(to_extend)
bag_ids_source.remove("delete")
bag_ids = bag_ids_source + bag_ids_target
# delete duplicate
bag_ids = list(set(bag_ids))
bag_ids.sort()

already_moved = set()

packets_path = []
for packet in tqdm.tqdm(os.listdir(v2_file_path)):
    if packet.startswith("ANNO"):
        continue
    else:
        packets_path.append(os.path.join(v2_file_path, packet))


for packet in tqdm.tqdm(packets_path):
    front_rect_path = os.path.join(packet, "FRONT_rect")
    front_wide_rect_path = os.path.join(packet, "FRONT_WIDE_rect")
    if not os.path.isdir(front_rect_path):
        raise ValueError("F** folder not exist?")
    if not os.path.isdir(front_wide_rect_path):
        raise ValueError("F** folder not exist?")
    for cur_anno_folder in [front_rect_path, front_wide_rect_path]:
        for jpg_name in tqdm.tqdm(os.listdir(cur_anno_folder)):
            file_count += 1
            frame_name = jpg_name.split(".jpg")[0]
            # 找到bag_id对应的包文件夹
            bag_id, bag_date = unixTime2Date(frame_name.split('.')[0])
            target = 0
            for idx, bid in enumerate(bag_ids):
                if bag_id <= bid:
                    target = idx - 1
                    break
            if target < 0:
                raise ValueError("F** for")
            if target == 0 and bag_id >= bag_ids[-1]:
                target = -1
            real_bag_id = bag_ids[target]
            real_bag_id_candidate = bag_ids[target - 1]

            should_exist_00 = os.path.join("/backup/v2_extract", real_bag_id, "FRONT_rect", frame_name + ".jpg")
            should_exist_01 = os.path.join(target_path, bag_date, real_bag_id, "FRONT_rect", frame_name + ".jpg")
            should_exist_02 = os.path.join("/backup/v2_extract", real_bag_id_candidate, "FRONT_rect", frame_name + ".jpg")
            should_exist_03 = os.path.join(target_path, bag_date, real_bag_id_candidate, "FRONT_rect", frame_name + ".jpg")

            candidate = [should_exist_00, should_exist_01, should_exist_02, should_exist_03]
            for idx, path in enumerate(candidate):
                if os.path.exists(path):
                    if idx in [1, 3]:
                        break
                    real_bag_id = real_bag_id_candidate if idx == 2 else real_bag_id
                    if real_bag_id in already_moved:
                        break
                    if not os.path.exists(os.path.join(target_path, bag_date, real_bag_id)):
                        # shutil.copytree(os.path.join("/backup/v2_extract", real_bag_id), os.path.join(target_path, bag_date, real_bag_id))
                        # print(f"copy from {os.path.join('/backup/v2_extract', real_bag_id)} to {os.path.join(target_path, bag_date, real_bag_id)}")
                        # copy_count += 1
                        os.makedirs(os.path.join(target_path, bag_date, real_bag_id))
                    for sub_folder_candidate in sub_folder_candidates:
                        file_ending = ".pcd" if sub_folder_candidate.startswith("LIDAR") else ".jpg"
                        if sub_folder_candidate.startswith("ANNOTATION"):
                            file_ending = ".json"
                        if not os.path.exists(os.path.join(target_path, bag_date, real_bag_id, sub_folder_candidate, frame_name + file_ending)):
                            #copy single file
                            if os.path.exists(os.path.join("/backup/v2_extract", real_bag_id, sub_folder_candidate, frame_name + file_ending)):
                                # check file size in gb
                                total_file_size += os.path.getsize(os.path.join("/backup/v2_extract", real_bag_id, sub_folder_candidate, frame_name + file_ending)) / 1024 / 1024 / 1024
                                # print(f"copy from {os.path.join("/backup/v2_extract", real_bag_id, sub_folder_candidate, frame_name + file_ending)} to {os.path.join(target_path, bag_date, real_bag_id, sub_folder_candidate, frame_name + file_ending)}")
                                # make target parent folder if not exist
                                if not os.path.exists(os.path.join(target_path, bag_date, real_bag_id, sub_folder_candidate)):
                                    os.makedirs(os.path.join(target_path, bag_date, real_bag_id, sub_folder_candidate))
                                shutil.copy(os.path.join("/backup/v2_extract", real_bag_id, sub_folder_candidate, frame_name + file_ending)
                                            , os.path.join(target_path, bag_date, real_bag_id, sub_folder_candidate, frame_name + file_ending))
                                copy_count += 1
                    already_moved.add(real_bag_id)
                    break


# record end time
end_time = time.time()

# calculate execution time
execution_time = end_time - start_time

print("Total number of frames processed:", frame_count)
print(f"Total {copy_count} files has been copied")
print(f"copied total {total_file_size} GB")
print(f"Script executed in {execution_time:.2f} seconds for totoal {file_count} files")