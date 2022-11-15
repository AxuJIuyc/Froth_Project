import os
from math import sqrt
import csv

#dir with hand marks labels
hm_dir_name = "./marked_imgs/my_marks_2/" # <---- CHECK
hm_dir = os.listdir(hm_dir_name)

#dir with network marks labels
nm_dir_name = "./marked_imgs/yolo_marks_2/labels/" # <---- CHECK
nm_dir = os.listdir(nm_dir_name)

IMG_SIZE = 640 # <---- CHECK
DIAM_COEF = 0.7 # 1/sqrt(2)

# read data files
print("--> Reading data files")
full_stat = []
stat_file_num = 1

for hm_frame in hm_dir:
    label_file_2 = open(hm_dir_name + hm_frame, 'r') # my_marks
    print(hm_frame)
    for nm_frame in nm_dir:
        if hm_frame[-11:-9] == nm_frame[-12:-10] and hm_frame[-8:-6] == nm_frame[-9:-7]:
            label_file_1 = open(nm_dir_name + nm_frame, 'r') # yolo_marks
            print(nm_frame)
            break
    DIR_NAME = "marked_imgs/stats_9/" # <---- CHECK
    FILE_NAME = f"stat_{stat_file_num}_65.csv" # <---- CHECK
    PATH = DIR_NAME + FILE_NAME
    
    label_list_1 = []
    label_list_2 = []

    for line in label_file_1:
        label_list_1.append(line.split())
    for line in label_file_2:
        label_list_2.append(line.split())

    label_file_1.close()
    label_file_2.close()


    # Open statistic_file
    print(f'--> {stat_file_num} Open statistic file')
    statistic_file = open(PATH, "w")
    file_writer = csv.writer(statistic_file, delimiter=' ', lineterminator='\r')
    file_writer.writerow(["x_2", "y_2", "D_2,px", " ", "x_1", "y_1", "D_1,px", " ", "dx", "dy", "dD,px", " ", "abs(dx+dy)%", "dD,px"])

    # recording and comparing boxes marked with network and hands
    # for each box from list 2, the closest one from list 1 is searched
    print(f"--> {stat_file_num} Bbox comparison...")
    for type2, x2, y2, w2, h2 in label_list_2:
        x2, y2, w2, h2 = list(map(float, [x2, y2, w2, h2]))
        r2 = int(sqrt(w2**2 + h2**2)*IMG_SIZE*DIAM_COEF)
        memory = [2, 2, 2, 0]
        line = 0
        flag = 0
        for type1, x1, y1, w1, h1 in label_list_1:
            x1, y1, w1, h1 = list(map(float, [x1, y1, w1, h1]))
            r1 = int(sqrt(w1**2 + h1**2)*IMG_SIZE*DIAM_COEF)
            if type1 != -1 and abs(x2 - x1) < 20/IMG_SIZE and abs(y2 - y1) < 20/IMG_SIZE:
                buffer = [round(abs(x2-x1), 3), round(abs(y2-y1), 3), (abs(r2-r1)), line]
                if memory[0] + memory[1] > buffer[0] + buffer[1]:
                    memory = buffer
                    r1_c = r1
                    flag = 1
            line += 1
        line = memory[3]
        label_list_1[line][0] = -1 # type1
        if flag == 1:
            file_writer.writerow([round(x2, 3), round(y2, 3), r2, " ", 
                                *label_list_1[line][1:3], r1_c, " ", 
                                *memory[:3], " ", 
                                abs(memory[0] + memory[1] * 100), memory[2]
            ])
        else:
            file_writer.writerow([round(x2, 3), round(y2, 3), r2, " ", 
                                2, 2, 2, " ", 
                                *memory[:3], " ", 
                                abs(memory[0] + memory[1] * 100), memory[2]
            ])
    statistic_file.close()


    # parameter estimation
    print(f"--> {stat_file_num} Estimation of required parameters")
    with open(PATH, 'r+') as statistic_file:
        stat_list = list(statistic_file.readlines())
        
        # total boxes found
        all_boxes = len(stat_list) - 1
        # crossed boxes
        line = 0
        for box in stat_list[1:]:
            box = list(box.split())
            if box[5] != '2':
                line += 1
            else:
                continue
        cross_boxes = line

        # lied boxes
        lie_marks = round((1 - cross_boxes / len(label_list_1)) * 100, 3)

        # diameter comparison
        dr_count1 = 0
        dr_count2 = 0
        b20px1 = 0
        b20px2 = 0
        for boxes in stat_list[1:]:
            boxes = list(boxes.split())
            if boxes[5] != '2':
                if int(boxes[-1]) <= 4:
                    dr_count1 += 1
                if int(boxes[-1]) <= 10:
                    dr_count2 += 1
                if int(boxes[7]) >= 20:
                    b20px1 += 1
                    if int(boxes[2]) >= 20:
                        b20px2 += 1
        dr1 = round(dr_count1 / cross_boxes * 100, 3)
        dr2 = round(dr_count2 / cross_boxes * 100, 3)
        print(dr_count1, dr_count2, cross_boxes)
        tb = round(b20px2 / b20px1 * 100, 3)
        
        file_writer = csv.writer(statistic_file, delimiter=' ', lineterminator='\r')
        file_writer.writerow(["Boxes_list2", 
                            "Boxes_list1", 
                            "Cross_boxes", 
                            "Lie_boxes, %", 
                            "True_Boxes>20px, %", 
                            "dD<4px, %", 
                            "dD<10px, %", 
                        ])
        file_writer.writerow([all_boxes, 
                            len(label_list_1), 
                            cross_boxes, 
                            lie_marks,
                            tb, 
                            dr1, 
                            dr2, 
                        ])

    print("--> Calculation Complete")

    # crop a line with statistics in each file
    # and writing to a separate file
    with open(PATH, 'r') as f:
        last_line = []
        for line in f:
            continue
        last_line.append(stat_file_num)
        last_line.append(nm_frame)
        for x in line.strip().split():
            last_line.append(float(x))
        for i in range(2, 5):
            last_line[i] = int(last_line[i])

    full_stat.append(last_line)
    stat_file_num += 1
    
print("--> Writing to output file")
with open(DIR_NAME + 'full_stat.csv', 'w') as fs:
    file_writer = csv.writer(fs, delimiter=' ', lineterminator='\r')
    file_writer.writerow(["N", 
                        "File_Name", 
                        "Hand_Marks",
                        "Network_Marks",
                        "Cross_Marks",
                        "Lie_Marks, %",
                        "True_Marks>20px, %",
                        "dD<4px, %",
                        "dD<10px, %", 
                    ])
    for line in full_stat:
        file_writer.writerow(line)
    
print("--> Complete")    