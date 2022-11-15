import os
from math import sqrt
import csv


class ComparisonLabels():    
    def __init__(self,
                dir2="./hm_dir_name",
                dir1="./nm_dir_name",
                DIR_NAME="./stats",
                CORR_FACTOR=1
            ):
        self.dir2 = dir2
        self.dir1 = dir1
        self.DIR_NAME = DIR_NAME
        self.CORR_FACTOR = CORR_FACTOR # diameter analysis correction factor

    def comparison_data(self, IMG_SIZE=640, tresh=65):
        # directories with comparison files:
        hm_dir = os.listdir(self.dir2)
        nm_dir = os.listdir(self.dir1)

        # read data files
        print("--> Reading data files")
        full_stat = []
        stat_file_num = 1
        for hm_frame in hm_dir:
            label_file_2 = open(self.dir2 + hm_frame, 'r') # my_marks
            print(hm_frame)
            for nm_frame in nm_dir:
                if hm_frame[-11:-9] == nm_frame[-12:-10] and hm_frame[-8:-6] == nm_frame[-9:-7]:
                    label_file_1 = open(self.dir1 + nm_frame, 'r') # yolo_marks
                    print(nm_frame)
                    break
            FILE_NAME = f"stat_{stat_file_num}_{tresh}.csv" # <---- CHECK
            PATH = self.DIR_NAME + FILE_NAME
            
            label_list_1 = []
            label_list_2 = []

            for line in label_file_1:
                label_list_1.append(line.split())
            for line in label_file_2:
                label_list_2.append(line.split())

            label_file_1.close()
            label_file_2.close()

            print(f'--> {stat_file_num} Open statistic file')
            self.nearest_object(label_list_2, label_list_1, PATH, stat_file_num, IMG_SIZE)
            
            print(f"--> {stat_file_num} Estimation of required parameters")
            self.req_assessment(label_list_1, IMG_SIZE, PATH)
            
            print("--> Writing to output file")
            self.union(full_stat, stat_file_num, nm_frame, PATH)
            
            stat_file_num += 1

    def diameter_deviation(self, IMG_SIZE_1=640, IMG_SIZE_2=320, tresh=65):
        # directories with comparison files:
        hnm_dir = os.listdir(self.dir2)
        hnm_dir.remove("dim_devi")
        hnm_dir.remove("full_stat.csv")
        chnm_dir = os.listdir(self.dir1)

        # read data files
        print("--> Reading data files")
        full_stat = []
        stat_file_num = 1
        for hnm_stat in hnm_dir:
            flag = 0
            label_file_2 = open(self.dir2 + hnm_stat, 'r') # my_marks
            print(hnm_stat)
            for chnm_stat in chnm_dir:
                if hnm_stat[5:7] == chnm_stat[5:7]:
                    label_file_1 = open(self.dir1 + chnm_stat, 'r') # yolo_marks
                    print(chnm_stat + "_crop")
                    flag = 1
                    break
            if flag == 0:
                continue
            
            FILE_NAME = f"cropstat_{stat_file_num}_{tresh}.csv" # <---- CHECK
            dir_name = self.DIR_NAME + "dim_devi/"
            PATH = dir_name + FILE_NAME
            
            label_list_1 = []
            label_list_2 = []

            for line in label_file_1:
                label_list_1.append(line.split())
            for line in label_file_2:
                label_list_2.append(line.split())

            label_file_1.close()
            label_file_2.close()
        
            self.write_objects(label_list_2[1:-2], label_list_1[1:-2], PATH, stat_file_num)
            
            print("--> Writing to output file")
            self.union(full_stat, stat_file_num, hnm_stat, PATH, flag='crop')
            stat_file_num += 1

        # union(full_stat, stat_file_num, nm_frame, PATH)
        

    # recording and comparing boxes marked with network and hands
    def write_objects(self, label_list_2, label_list_1, PATH="./statistic_file.csv", stat_file_num=1):
        # Open statistic_file
        statistic_file = open(PATH, "w")
        file_writer = csv.writer(statistic_file, delimiter=' ', lineterminator='\r')
        file_writer.writerow([
                            "x_hm", "y_hm", "D_hm", " ", 
                            "x_nm", "y_nm", "D_nm", " ", "dD, %", " ", 
                            "x_chm", "y_chm", "D_chm", " ", 
                            "x_cnm", "y_cnm", "D_cnm", " ", "dD_crop, %", " ",
                        ])

        # for each box from list 2, the closest one from list 1 is searched
        print(f"--> {stat_file_num} writing comparison...")   
        i = 0
        dDsum1 = 0
        dDsum2 = 0
        dDc1 = 0
        dDc2 = 0
        for params_list_2 in label_list_2:
            # print(params_list_2)
            dD2 = (float(params_list_2[2]) - float(params_list_2[7])) * 100
            if i < len(label_list_1):
                params_list_1 = label_list_1[i]
                dD1 = (float(params_list_1[2]) - float(params_list_1[7])) * 100
                file_writer.writerow([*params_list_2[:3], " ", *params_list_2[5:8], " ", dD2, " ",
                                    *params_list_1[:3], " ", *params_list_1[5:8], " ", dD1])
                if -50 < float(params_list_1[7]) < 50:
                    dDsum1 += float(params_list_1[7])
                    dDc1 += 1
                i += 1
            else:
                file_writer.writerow([*params_list_2[:3], " ", *params_list_2[5:8], " ", dD2, " "])
            if -50 < float(params_list_2[7]) < 50:
                dDsum2 += float(params_list_2[7])
                dDc2 += 1
            # x22, y22, d22, s20, x21, y21, d21
        file_writer.writerow(["avg_dD_hnm, %", "avg_dD_chnm, %"])
        file_writer.writerow([dDsum2/dDc2, dDsum1/dDc1])
        statistic_file.close()
    
    # recording and comparing boxes marked with network and hands
    def nearest_object(self, label_list_2, label_list_1, PATH="./statistic_file.csv", stat_file_num=1, IMG_SIZE=640):
        # Open statistic_file
        statistic_file = open(PATH, "w")
        file_writer = csv.writer(statistic_file, delimiter=' ', lineterminator='\r')
        file_writer.writerow(["x_hm", "y_hm", "D_hm,px", " ", "x_nm", "y_nm", "D_nm,px", " ", "dx", "dy", "dD,px", " ", "abs(dx+dy)%", "dD,px"])

        
        # for each box from list 2, the closest one from list 1 is searched
        print(f"--> {stat_file_num} Bbox comparison...")   
        for type2, x2, y2, w2, h2 in label_list_2:
            x2, y2, w2, h2 = list(map(float, [x2, y2, w2, h2]))
            r2 = int(sqrt(w2**2 + h2**2)*IMG_SIZE) #diameter
            memory = [2, 2, 2, 0]
            line = 0
            flag = 0
            for type1, x1, y1, w1, h1 in label_list_1:
                x1, y1, w1, h1 = list(map(float, [x1, y1, w1, h1]))
                r1 = int(sqrt(w1**2 + h1**2)*IMG_SIZE * self.CORR_FACTOR) #diameter
                if type1 != -1 and abs(x2 - x1) < 20/IMG_SIZE and abs(y2 - y1) < 20/IMG_SIZE:
                    buffer = [round(abs(x2-x1), 3), round(abs(y2-y1), 3), round(abs(r2-r1), 3), line]
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
                                    abs(memory[0] + memory[1] * 100), memory[2]])
            else:
                file_writer.writerow([round(x2, 3), round(y2, 3), r2, " ", 
                                    2, 2, 2, " ", 
                                    *memory[:3], " ", 
                                    abs(memory[0] + memory[1] * 100), memory[2]])
        statistic_file.close()

    # parameter estimation
    def req_assessment(self, label_list_1, IMG_SIZE=640, PATH="./stat_file.scv"):
        with open(PATH, 'r+') as statistic_file:
            stat_list = list(statistic_file.readlines())
            
            # total boxes found
            all_boxes = len(stat_list) - 1
            # crossed boxes
            line = 0
            for box in stat_list[1:]:
                box = list(box.split())
                if box[-1] != '200':
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
                if float(boxes[-1]) <= 4:
                    dr_count1 += 1
                if float(boxes[-1]) <= 10:
                    dr_count2 += 1
                if float(boxes[6]) >= 20:
                    b20px1 += 1
                    if float(boxes[2]) >= 20:
                        b20px2 += 1
            dr1 = round(dr_count1 / cross_boxes * 100, 6)
            dr2 = round(dr_count2 / cross_boxes * 100, 6)
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
    def union(self, full_stat=[], stat_file_num=1, nm_frame=1, PATH="./stat_file.csv", flag='full' ):
        with open(PATH, 'r') as f:
            last_line = []
            for line in f:
                continue
            last_line.append(stat_file_num)
            last_line.append(nm_frame)
            if flag == 'full':
                for x in line.strip().split():
                    last_line.append(float(x))
                for i in range(2, 5):
                    last_line[i] = int(last_line[i])
                full_stat.append(last_line)
                self.write_union(full_stat)
            elif flag == 'crop':
                for x in line.strip().split():
                    last_line.append(round(float(x), 6))
                last_line.append(last_line[-1] - last_line[-2])
                full_stat.append(last_line)
                self.write_crop_union(full_stat)
        

    def write_union(self, full_stat):
        with open(self.DIR_NAME + 'full_stat.csv', 'w') as fs:
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

    def write_crop_union(self, full_stat):
        with open(self.DIR_NAME + 'full_stat.csv', 'w') as fs:
            file_writer = csv.writer(fs, delimiter=' ', lineterminator='\r')
            file_writer.writerow(["N", 
                                "File_Name", 
                                "avg_dD_H_N_Marks, %",
                                "avg_dD_Crop_H_N_Marks, %",
                                "dif_dD"
                            ])               
            for line in full_stat:
                file_writer.writerow(line)  