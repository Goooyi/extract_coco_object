import matplotlib.pyplot as plt
import numpy as np
import time
import cv2
import os

from pycocotools.coco import COCO
from utils import *

#Add your coco dataset images folder path
data_dir = '/data/dataset/aXcellent/manu-label/axera_manu_v1.0/IMAGE'
ann_file='/code/gaoyi_dataset/coco/aXcellent_2d/annotations/axera_2d_1226_split_train.json'

#Add your output mask folder path
seg_output_path = '/code/gn0/extract_coco_object/seg_img'

#Add your cropped instance folder path
crop_output_path = '/code/gn0/extract_coco_object/crop_instance'

#Store original images into another folder
original_img_path = '/code/gn0/extract_coco_object/ori_img'

coco = COCO(ann_file)
# catIds = coco.getCatIds(catNms=['barrier', 'bendy', 'stop_line', 'crosswalk', 'RA_left_right', 'TFL_red']) #Add more categories ['person','dog']
catIds = coco.getCatIds(catNms=['stop_line']) #Add more categories ['person','dog']

for catId in catIds:
	imgIds = coco.getImgIds(catIds=catId)
	for i in range(len(imgIds)):
		# create a sub folder for each catId
		img = coco.loadImgs(imgIds[i])[0]
		category = coco.loadCats(catId)[0]
		annIds = coco.getAnnIds(imgIds=img['id'], catIds=catId, iscrowd=0)
		anns = coco.loadAnns(annIds)
		if not os.path.exists(os.path.join(seg_output_path, str(category["name"]))):
			os.makedirs(os.path.join(seg_output_path, str(category["name"])))
		mask = coco.annToMask(anns[0])
		for i in range(1, len(anns)):
			mask += coco.annToMask(anns[i])

		color_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
		color_mask[mask == 1] = [0, 0, 255]

		file_name = os.path.join(data_dir,img['file_name'])

		original_img = cv2.imread(file_name)
		draw_mask = cv2.addWeighted(src1=original_img,alpha=1,src2=color_mask,beta=1,gamma=0)
	 	# create a folder for current image name
		img_name = img['file_name'].split("/")[-1]
		if not os.path.exists(os.path.join(seg_output_path, str(category["name"]), img_name.split(".")[0])):
			os.makedirs(os.path.join(seg_output_path, str(category["name"]), img_name.split(".")[0]))

		cv2.imwrite(os.path.join(original_img_path,img_name),original_img)
		cv2.imwrite(os.path.join(seg_output_path, str(category["name"]), img_name),draw_mask)

		# I = cv2.imread(file_name)
		# plt.imshow(I)
		# coco.showAnns(anns)
		# plt.show()

print("Done")