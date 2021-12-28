import json, csv
import os
import cv2
from GTInference import returnannot_scaphoid, returnannot_fracture
from yoloformat import yolo_img_txt
import numpy as np

def img_crop(data, exp_fold, state, root):
    data_list = data[f'fold_{exp_fold}'][state]
    for set in data_list:
        img = cv2.imread(os.path.join(root, set['img_path']))
        low_x, low_y,up_x ,up_y = returnannot_scaphoid(os.path.join(root, set['scaphoid_annot']))
        # print(low_x, low_y,up_x ,up_y)
        # low_x, low_y,up_x ,up_y = setSquareBoundingBox(low_x, low_y,up_x ,up_y)
        crop_img = img[low_y:up_y, low_x:up_x]
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        equ = cv2.equalizeHist(gray)
        
        #square
        h,w = equ.shape
        if h > w:
            right_com = h - w
            equ = cv2.copyMakeBorder(equ, 0, 0, 0, right_com, cv2.BORDER_CONSTANT)
        else:
            down_com = w - h
            equ = cv2.copyMakeBorder(equ, 0, down_com, 0, 0, cv2.BORDER_CONSTANT)
        equ = cv2.cvtColor(equ, cv2.COLOR_GRAY2BGR)
        cv2.imwrite(os.path.join(root, set['img_crop_path']), equ)

def setSquareBoundingBox(low_x, low_y,up_x ,up_y):
    if (up_x - low_x) > (up_y - low_y):
        up_y = low_y + (up_x - low_x)
    else:
        up_x = low_x + (up_y - low_y)
    # print(low_x, low_y,up_x ,up_y)
    return low_x, low_y,up_x ,up_y

def rotated_yolo_annot_txt(data, exp_fold, state, annot_path):
    data_list = data[f'fold_{exp_fold}'][state]
    for typing in ['Fracture', 'Normal']:
        if not os.path.exists(os.path.join(annot_path, typing)):
            os.makedirs(os.path.join(annot_path, typing))
    for set in data_list:
        filename = set['name']
        label = set['label']
        if(label == 1): typing = 'Fracture'
        else:typing = 'Normal'
        f = open(os.path.join(annot_path, typing, f'{filename}_fracture.txt'), 'w')
        if(label == 1):
            img = cv2.imread(set['img_crop_path'])
            height, width, _ = img.shape
            print(height,width)
            x_center, y_center, long_side , short_side, angle = returnannot_fracture(set['fracture_annot'])
            
            x_center  /= width
            y_center /= height
            long_side /= width
            short_side /= height
            cos = np.cos(angle/180*np.pi)
            sin = np.sin(angle/180*np.pi)
            text = f'0 {x_center} {y_center} {long_side} {short_side} {cos} {sin}'
            f.write(text)
        
        f.close()

if __name__ == '__main__':
    root = '/home/u7085556/git/Scaphoid_Fractures_Detection /dataset/'
    exp_fold = 0
    with open(os.path.join(root,'./3Fold.json')) as f:
        data = json.load(f)
        for state in ['train','val']:
            img_crop(data, exp_fold, state, root)
            # yolo_img_txt(data, exp_fold, state, 'img_crop_path', os.path.join(os.path.join(root,f'{state}_fracture.txt')))
            rotated_yolo_annot_txt(data, exp_fold, state, os.path.join(os.path.join(root,'labels')))
            