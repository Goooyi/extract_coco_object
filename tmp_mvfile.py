import os
import tqdm

from_path = "/data/dataset/aXcellent/manu-label/v2/xcap001/"


for folder in tqdm.tqdm(os.listdir(from_path)):
    # sub_folder like "/data/dataset/aXcellent/manu-label/v1/xcap001/20231009"
    # 跳过已经是”年月日“形式的文件夹
    if "-" not in folder:
        continue
    sub_folder = os.path.join(from_path, folder)
    if os.path.isdir(sub_folder):
        new_parent_folder = sub_folder.split("/")[-1].split(".")[0].split("-")[:3]
        new_parent_folder = "".join(new_parent_folder)
        new_parent_folder = os.path.join(from_path, new_parent_folder)
        if not os.path.exists(new_parent_folder):
            os.makedirs(new_parent_folder)
        new_parent_folder = os.path.join(new_parent_folder, sub_folder.split("/")[-1])
        # print("move {} to {}".format(sub_folder, new_parent_folder))

        os.replace(sub_folder, new_parent_folder)