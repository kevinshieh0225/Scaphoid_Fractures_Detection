import json
import os
import cv2
from GTInference import GTInference_scaphoid

def yolo_img_txt(data, exp_fold, state, key, txt_path):
    data_list = data[f'fold_{exp_fold}'][state]
    f = open(txt_path, 'w')
    for set in data_list:
        if os.path.exists(set[key]):
            img_path = set[key]
            f.write(f'{img_path}\n')
    f.close()

def yolo_annot_txt(data, exp_fold, state, annot_path):
    data_list = data[f'fold_{exp_fold}'][state]
    for typing in ['Fracture', 'Normal']:
        if not os.path.exists(os.path.join(annot_path, typing)):
            os.makedirs(os.path.join(annot_path, typing))
    for set in data_list:
        img = cv2.imread(set['img_path'])
        height, width, _ = img.shape
        low_x, low_y,up_x ,up_y = GTInference_scaphoid(set['scaphoid_annot'])

        x_center = (low_x+up_x)/2/width
        y_center = (low_y+up_y)/2/height
        yolo_w = (up_x-low_x)/width
        yolo_h = (up_y-low_y)/height

        filename = set['name']
        if(set['label'] == 1): typing = 'Fracture'
        else:typing = 'Normal'
        f = open(os.path.join(annot_path, typing, f'{filename}.txt'), 'w')
        text = f'0 {x_center} {y_center} {yolo_w} {yolo_h}'
        f.write(text)
        f.close()

if __name__ == '__main__':
    root = '/home/u7085556/git/Scaphoid_Fractures_Detection /dataset/'
    exp_fold = 2
    with open(os.path.join(root,'./3Fold.json')) as f:
        data = json.load(f)
        for state in ['train','val']:
            #yolo_annot_txt(data, exp_fold, state, os.path.join(os.path.join(root,'labels')))
            yolo_img_txt(data, exp_fold, state, 'img_path', os.path.join(os.path.join(root,f'{state}.txt')))
            