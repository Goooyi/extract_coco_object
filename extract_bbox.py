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
#Add your drawed bbox folder path
bbox_output_path = '/code/gn0/extract_coco_object/bbox_img'
#Add your cropped instance folder path
crop_output_path = '/code/gn0/extract_coco_object/crop_instance'
#Store original images into another folder
original_img_path = '/code/gn0/extract_coco_object/ori_img'
# settings
save_ori = False
save_seg = False
save_bbox = False
save_crop = True
save_binary_mask = True # only if save_crop is True
expanded_width = 40
expanded_height = 40

coco = COCO(ann_file)
# catIds = coco.getCatIds(catNms=['barrier', 'bendy', 'stop_line', 'crosswalk', 'RA_left_right', 'TFL_red']) #Add more categories ['person','dog']
catIds = coco.getCatIds(catNms=['crosswalk']) #Add more categories ['person','dog']


for catId in catIds:
	imgIds = coco.getImgIds(catIds=catId)
	for i in range(len(imgIds)):
		# create a sub folder for each catId
		img = coco.loadImgs(imgIds[i])[0]
		category = coco.loadCats(catId)[0]
		annIds = coco.getAnnIds(imgIds=img['id'], catIds=catId, iscrowd=0)
		anns = coco.loadAnns(annIds)

		file_name = os.path.join(data_dir,img['file_name'])

		original_img = cv2.imread(file_name)
	 	# create a folder for current image name
		img_name = img['file_name'].split("/")[-1]

		if save_ori:
			cv2.imwrite(os.path.join(original_img_path,img_name),original_img)
		if save_seg:
			if not os.path.exists(os.path.join(seg_output_path, str(category["name"]))):
				os.makedirs(os.path.join(seg_output_path, str(category["name"])))

			mask = coco.annToMask(anns[0])
			for i in range(1, len(anns)):
				mask += coco.annToMask(anns[i])
			color_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
			color_mask[mask == 1] = [0, 0, 255]
			draw_mask = cv2.addWeighted(src1=original_img,alpha=1,src2=color_mask,beta=1,gamma=0)
			cv2.imwrite(os.path.join(seg_output_path, str(category["name"]), img_name),draw_mask)
		if save_crop:
			image_folder_name = ".".join(img_name.split(".")[0:2])
			if not os.path.exists(os.path.join(crop_output_path, str(category["name"]), image_folder_name)):
				os.makedirs(os.path.join(crop_output_path, str(category["name"]), image_folder_name))
			for idx, ann in enumerate(anns):
				x, y, w, h = ann['bbox']
				x = int(x)
				y = int(y)
				w = int(w)
				h = int(h)
				if w <= 0: # only happens for stop line
					w = expanded_width
				if h <= 0: # only happens for stop line
					h = expanded_height
				x_tmp = min(img["width"], x+w)
				y_tmp = min(img["height"], y+h)
				crop = original_img[y:y_tmp, x:x_tmp]
				cv2.imwrite(os.path.join(crop_output_path, str(category["name"]), image_folder_name, str(idx)+'.jpg'), crop)
				if save_binary_mask:
					if not os.path.exists(os.path.join(crop_output_path, str(category["name"]), image_folder_name + "_binary_mask")):
						os.makedirs(os.path.join(crop_output_path, str(category["name"]), image_folder_name + "_binary_mask"))
					# first appl Bilateral Filtering to reduce noise
					blur = cv2.bilateralFilter(crop, 9, 75, 75)
					# bgr to gray
					blur = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
					# then apply Otsu Binarization
					instance_mask = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
					# global thresholding sice road marking is white

					cv2.imwrite(os.path.join(crop_output_path, str(category["name"]), image_folder_name + "_binary_mask", str(idx)+'.jpg'), instance_mask)
		if save_bbox:
			if not os.path.exists(os.path.join(bbox_output_path, str(category["name"]))):
				os.makedirs(os.path.join(bbox_output_path, str(category["name"])))
			color_mask = np.zeros((img["height"], img["width"], 3), dtype=np.uint8)
			for idx, ann in enumerate(anns):
				x, y, w, h = ann['bbox']
				x = int(x)
				y = int(y)
				w = int(w)
				h = int(h)
				color_mask[y:y+h, x:x+w] = [0, 0, 255]
			draw_bbox = cv2.addWeighted(src1=original_img,alpha=1,src2=color_mask,beta=1,gamma=0)
			cv2.imwrite(os.path.join(bbox_output_path, str(category["name"]), img_name),draw_bbox)


		# I = cv2.imread(file_name)
		# plt.imshow(I)
		# coco.showAnns(anns)
		# plt.show()

print("Done")