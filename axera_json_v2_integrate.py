import os
import json
import shutil
import tqdm
from utils import create_default_json, fill_img_camear_info,unixTime2Date,change_ownership_and_permissions
import time

# record start time
start_time = time.time()
file_count = 0
frame_count = 0
copy_count = 0
total_file_size = 0

# TODO:由于目前再转移数据，当前版本是全量检查+合并，后期数据多了改成增量
frame_set = set()

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

carid = "001"
sensor_file_path = "/code/gn0/extract_coco_object/v2_xcap001_calibration.yaml"
# 初期保存的地方，目前正在往target转
source_path = "/backup/v2_extract/"
# 目标存储地方，正在被转, 所以单个帧的文件夹，不再source_path就在target_path，过两天转完了就全在target_path了
target_path = "/data/dataset/aXcellent/manu-label/v2/xcap001/"

# 以上原因，先整合两个目录
bag_ids_source = os.listdir(source_path)
bag_ids_target = []
for sub_folder in os.listdir(target_path):
    if not os.path.isdir(os.path.join(target_path, sub_folder)):
        continue
    to_extend = os.listdir(os.path.join(target_path, sub_folder))
    bag_ids_target.extend(to_extend)
bag_ids_source.remove("delete")
bag_ids = bag_ids_source + bag_ids_target
bag_ids = list(set(bag_ids))
bag_ids.sort()

# 标注商对单个类目比如lane的标注位置，需要把同一帧的整合, 遍历这个文件夹的所有子目录
annotation_path = "/backup/manu_label_v2/ANNOTATION/april"

for anno_folder_idx, category_folder in enumerate(tqdm.tqdm(os.listdir(annotation_path))):
    if category_folder.startswith("obstacle"):
        # 障碍物下面只有LIDAR_VCS文件夹
        sub_anno_folder = ["LIDAR_VCS"]
    else:
        # 其他类目下面还有FRONT_WIDE_rect和FRONT_rect
        sub_anno_folder = ["FRONT_WIDE_rect", "FRONT_rect"]

    category_folder = os.path.join(annotation_path, category_folder)
    if not os.path.isdir(category_folder):
        continue
    for sub_camera in sub_anno_folder:
        cam_category_folder = os.path.join(category_folder, sub_camera)
        if not os.path.isdir(cam_category_folder):
            continue
        for json_name in tqdm.tqdm(os.listdir(cam_category_folder)):
            file_count += 1
            frame_name = json_name.split(".json")[0]
            # 找到bag_id对应的包文件夹
            bag_id, bag_date = unixTime2Date(frame_name.split('.')[0])
            # TODO 修改1分钟的逻辑
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
            real_bag_id_candidate_01 = bag_ids[target - 2]

            should_exist_00 = os.path.join("/backup/v2_extract", real_bag_id, "FRONT_rect", frame_name + ".jpg")
            should_exist_01 = os.path.join("/backup/v2_extract", real_bag_id_candidate, "FRONT_rect", frame_name + ".jpg")
            should_exist_02 = os.path.join("/backup/v2_extract", real_bag_id_candidate_01, "FRONT_rect", frame_name + ".jpg")
            should_exist_03 = os.path.join(target_path, bag_date, real_bag_id, "FRONT_rect", frame_name + ".jpg")
            should_exist_04 = os.path.join(target_path, bag_date, real_bag_id_candidate, "FRONT_rect", frame_name + ".jpg")
            should_exist_05 = os.path.join(target_path, bag_date, real_bag_id_candidate_01, "FRONT_rect", frame_name + ".jpg")

            found = False
            candidate = [should_exist_00, should_exist_01, should_exist_02, should_exist_03, should_exist_04, should_exist_05]
            for idx, path in enumerate(candidate):
                if os.path.exists(path):
                    found = True
                    if idx in [0, 3]:
                        break
                    elif idx in [1, 4]:
                        real_bag_id = real_bag_id_candidate
                        break
                    else:
                        real_bag_id = real_bag_id_candidate_01
                        break

            bag_id = real_bag_id

            if not found:
                raise ValueError(f"F** not found for {frame_name}, suppose bag_id is {real_bag_id} {real_bag_id_candidate} {real_bag_id_candidate_01}")

            # if os.path.isdir(os.path.join(source_path,bag_id)):
            #     output_json_path = os.path.join(source_path,bag_id)
                # if os.path.exists(os.path.join(target_path,bag_date,bag_id)):
                #     continue
            # else:
            #     continue
            #     output_json_path = os.path.join(target_path,bag_id)
            #     if not os.path.isdir(output_json_path):
            #         raise ValueError("F** folder not exist?")

            # create a new file if not created yet
            if frame_name not in frame_set:
                frame_count += 1
                frame_set.add(frame_name)
                new_json = create_default_json()
                new_json["info"]["description"] = "Integrated from each category of AXERA stage 2 annotations"
                new_json["info"]["contributor"] = "gaoyi"
                new_json = fill_img_camear_info(new_json,carid,frame_name,sensor_file_path)
            else:
                #load在/data/dataset下面保存的json文件
                with open(os.path.join(target_path,bag_date,bag_id,"ANNOTATION_manu", frame_name + '.json'), 'r') as f:
                        new_json = json.load(f)

            with open(os.path.join(cam_category_folder,frame_name + '.json'), 'r') as f:
                cur_json = json.load(f)
                # 合入cur_json
                for key in cur_json["annotations"].keys():
                    if key not in new_json["annotations"].keys():
                        new_json["annotations"][key] = cur_json["annotations"][key]
                    else:
                        new_json["annotations"][key].extend(cur_json["annotations"][key])

            # 在/data/dataset下保存最终有标注的帧文件
            save_path = os.path.join(target_path,bag_date)
            if not os.path.exists(os.path.join(save_path)):
                os.makedirs(os.path.join(save_path))
            # 判断，需要拷贝整个文件vs只需要修改json文件
            if not os.path.exists(os.path.join(save_path,bag_id)):
                # print(f"copy from {output_json_path} to {os.path.join(save_path,bag_id)}")
                # shutil.copytree(output_json_path, os.path.join(save_path,bag_id))
                os.makedirs(os.path.join(save_path,bag_id,"ANNOTATION_manu"))
            # 保存整个的json文件
            if not os.path.exists(os.path.join(save_path,bag_id,"ANNOTATION_manu")):
                os.makedirs(os.path.join(save_path,bag_id,"ANNOTATION_manu"))
            for sub_folder_candidate in sub_folder_candidates:
                    file_ending = ".pcd" if sub_folder_candidate.startswith("LIDAR") else ".jpg"
                    if sub_folder_candidate.startswith("ANNOTATION"):
                        file_ending = ".json"
                    if not os.path.exists(os.path.join(target_path, bag_date, bag_id, sub_folder_candidate, frame_name + file_ending)):
                        #copy single file
                        if os.path.exists(os.path.join("/backup/v2_extract", bag_id, sub_folder_candidate, frame_name + file_ending)):
                            # check file size in gb
                            total_file_size += os.path.getsize(os.path.join("/backup/v2_extract", bag_id, sub_folder_candidate, frame_name + file_ending)) / 1024 / 1024 / 1024
                            # print(f"copy from {os.path.join("/backup/v2_extract", bag_id, sub_folder_candidate, frame_name + file_ending)} to {os.path.join(target_path, bag_date, real_bag_id, sub_folder_candidate, frame_name + file_ending)}")
                            # make target parent folder if not exist
                            if not os.path.exists(os.path.join(target_path, bag_date, bag_id, sub_folder_candidate)):
                                os.makedirs(os.path.join(target_path, bag_date, bag_id, sub_folder_candidate))
                            shutil.copy(os.path.join("/backup/v2_extract", bag_id, sub_folder_candidate, frame_name + file_ending)
                                        , os.path.join(target_path, bag_date, bag_id, sub_folder_candidate, frame_name + file_ending))
                            copy_count += 1
            with open(os.path.join(save_path,bag_id,"ANNOTATION_manu",frame_name + '.json'), 'w') as f:
                json.dump(new_json, f)


# record end time
end_time = time.time()

# calculate execution time
execution_time = end_time - start_time

print("Total number of frames processed:", frame_count)
print(f"copy total {total_file_size} GB with {copy_count} files")
print(f"Script executed in {execution_time:.2f} seconds for totoal {file_count} files")