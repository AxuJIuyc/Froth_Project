import cv2


yolo_img_path = "/home/axuji/Projects/FrothProject/yolov5-master/runs/detect/exp26/frame0:00:08.00.jpg"
# yolo_img_path = "/home/axuji/Projects/FrothProject/matches/marked_imgs/img_alignment/0frame0:00:08.00.jpg"
yolo_label_path = "/home/axuji/Projects/FrothProject/yolov5-master/runs/detect/exp26/labels/frame0:00:00.00.txt"
hand_label_path = "/home/axuji/Projects/FrothProject/matches/marked_imgs/my_marks_2/frame0 00 0800.txt"
# hand_label_path = "/home/axuji/Projects/FrothProject/matches/marked_imgs/img_alignment/frame0 00 0800.txt"
save_path = "/home/axuji/Projects/FrothProject/matches/marked_imgs/img_alignment/2.jpg"
color = (255,255,255)
line_thickness = 0
names = "bubble"


img = cv2.imread(yolo_img_path)

with open(hand_label_path, "r") as hlf:
    for line in hlf:
        index, x, y, w, h = list(map(float, line.split()))
        p1, p2 = (int((x - w/2)*640), int((y - h/2)*640)), (int((x + w/2)*640), int((y + h/2)*640))
        cv2.rectangle(img, p1, p2, (200,0,0), 0, cv2.LINE_AA)

cv2.imwrite(save_path, img)
print('complete')

