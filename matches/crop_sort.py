import os


#dir with hand marks labels
hm_dir_name = "./marked_imgs/my_marks_2/"
hm_dir = os.listdir(hm_dir_name)

IMG_SIZE_1 = 640
IMG_SIZE_2 = 320
k = IMG_SIZE_1 / IMG_SIZE_2

n_file = 1
# Redacting labels files
for file_name in hm_dir:
    # file_name = "frame0 00 1500.txt"
    print(f"--> Redacting {n_file} file")
    with open(hm_dir_name + file_name, 'r') as f:
        lable_list = []
        for line in f.readlines():
            lable_list.append(line.split())
        indexes = []
        i = 0
        # 640 to 320 px: x,y,w,h value increase 2 times
        # y is shifting by 30 px
        for x in lable_list:
            for q in range(1, 5):
                x[q] = float(x[q]) * k

            if (float(x[1]) > 1
            or float(x[2]) > 1 + 30/IMG_SIZE_2
            or float(x[2]) < 30/IMG_SIZE_2
            ):
                indexes.append(i)
            i += 1
        indexes.reverse()
        for i in indexes:
            lable_list.pop(i)
        
        # save to new file
        with open(f'marked_imgs/my_crop_marks/crop_{file_name}', 'w') as fc:
            for line in lable_list:
                for x in line:
                    fc.write(str(x) + ' ')
                fc.write('\n')
        
        n_file += 1