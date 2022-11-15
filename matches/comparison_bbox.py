import comparison_data


#dir with hand marks labels
hm_dir_name = "./marked_imgs/my_marks_2/" # <---- CHECK

#dir with hand marks crop_labels
chm_dir_name = "./marked_imgs/my_crop_marks/" # <---- CHECK
# chm_dir = os.listdir(chm_dir_name)

#dir with network marks labels
nm_dir_name = "./marked_imgs/yolo_marks_2/labels/" # <---- CHECK

#dir with network marks crop_labels
cnm_dir_name = "./marked_imgs/yolo_crop_marks/labels/" # <---- CHECK
# cnm_dir = os.listdir(cnm_dir_name)

IMG_SIZE_1 = 640 # <---- CHECK
IMG_SIZE_2 = 320 # <---- CHECK
CORR_FACTOR = 1

# dir for statistic files
DIR_NAME = "marked_imgs/stats_6/" # <---- CHECK

compar = comparison_data.ComparisonLabels(hm_dir_name, nm_dir_name, DIR_NAME, CORR_FACTOR)
compar.comparison_data()

#dir with hnm_stat
# hnm_dir_name = "./marked_imgs/stats_5/" # <---- CHECK

#dir with chnm_stat
# chnm_dir_name = "./marked_imgs/crop_stats/" # <---- CHECK

# compar = comparison_data.ComparisonLabels(hnm_dir_name, chnm_dir_name, DIR_NAME)
# compar.diameter_deviation()

print("--> Complete")    