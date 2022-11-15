def diameters():
    import os
    import csv


    DIR = "./marked_imgs/stats_4/dim_devi/"
    # DIR = "./marked_imgs/crop_stats/"
    IMAGE_SIZE = 640
    CORR_FACTOR = 1.0
    CAP = 1.0
    STEP = 0.01
    one_file = False
    FILE = "cropstat_25_65.csv"

    if one_file:
        dir = [FILE]
    else:
        dir = os.listdir(DIR)

    df = open("diameters.csv", "w")
    file_writer = csv.writer(df, delimiter=' ', lineterminator='\r')

    while CORR_FACTOR <= CAP:
        print("CORR_FACTOR:", CORR_FACTOR)
        file_writer.writerow(["CORR_FACTOR:", CORR_FACTOR])
        file_writer.writerow(["name", 'D4', 'D10', "neg", "good"])
        for FILE in dir:
            PATH = DIR + FILE

            file = []
            with open(PATH, "r") as f:
                for x in f:
                    file.append(x.strip().split())

            D_hm = []
            D_nm = []
            for line in file[1:-2]:
                # print(FILE, line)
                if float(line[7]) < 2:
                    try:
                        D_hm.append(float(line[15]))
                        D_nm.append(float(line[20]) * CORR_FACTOR)
                    except:
                        break

            D_dif = []
            j = 0
            neg = []
            good = []
            while j < len(D_hm):
                if D_nm[j] != "2":
                    dif = round(D_hm[j] - D_nm[j], 4)
                    D_dif.append(dif)
                    if dif <= 0:
                        neg.append(dif)
                    else:
                        good.append(dif)
                    j += 1
            sum = [0, 0, 0] #neg, good, all
            for x in neg:
                sum[0] += x
            for x in good:
                sum[1] += x

            dD4_list = []
            dD10_list = []
            i = 0
            for dhm in D_hm:
                if i < len(D_nm):
                    dD = abs(dhm - D_nm[i])
                    if dD <= 10/640:
                        dD10_list.append(dD)
                        if dD <= 4/640:
                            dD4_list.append(dD)
                    i += 1
                else:
                    break

            dD4_res = round(len(dD4_list)/len(D_hm), 3) if len(D_hm)>0 else "None"
            dD10_res = round(len(dD10_list)/len(D_hm), 3) if len(D_hm)>0 else "None"

            file_writer.writerow([
                                FILE, str(dD4_res), str(dD10_res), 
                                round(sum[0]/len(neg), 4) if len(neg)>0 else None, 
                                round(sum[1]/len(good), 4) if len(good)>0 else None,
                                len(neg) if len(neg)>0 else None,
                                len(good) if len(good)>0 else None
            ])
        
        file_writer.writerow([" "])
        CORR_FACTOR += STEP

    df.close()

# most popular diameter
def most_pop_diam(label_file):
    diameters = []
    with open(label_file, 'r') as f:
        for line in f:
            index, x, y, w, h = list(map(float, line.split()))
            diameters.append(int((w**2 + h**2)**(1/2)*640))
    d = 0
    all_d = len(diameters)
    for x in diameters:
        d += x
    avg_d = round((d / all_d), 2)
    return [avg_d, diameters]
           

def main():
    label_file = "/home/axuji/Projects/FrothProject/yolov5-master/runs/detect/exp26/labels/frame0:00:00.00.txt"
    print(most_pop_diam(label_file))

if __name__ == "__main__":
    main()
