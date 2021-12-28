import json , csv
import cv2
import os
import numpy as np

def GTInference_scaphoid(Img_data):
    img = cv2.imread(Img_data['img_path'])
    annot = returnannot_fracture(Img_data['scaphoid_annot'])
    low_x, low_y,up_x ,up_y = annot
    for idx in range(low_x, up_x+1):
        for y in [low_y, up_y]:
            img[y][idx][1] = 255
    for idx in range(low_y, up_y+1):
        for x in [low_x, up_x]:
            img[idx][x][1] = 255
    img[0][0][2] = 255
    img[0][1][2] = 255
    img[0][2][2] = 255
    save_path = './Inference'
    Img_name = Img_data['name']
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    cv2.imwrite(os.path.join(save_path,f'{Img_name}.jpg'), img)

def GTInference_fracture(Img_data):
    img = cv2.imread(Img_data['img_crop_path'])
    try:
        annot = returnannot_fracture(Img_data['fracture_annot'])
        x_center, y_center, long_side , short_side, angle = annot
        center = np.array([x_center, y_center])
        angle = -angle/180*np.pi
        print(img.shape)
        print(angle)
        low_x = x_center-long_side//2
        up_x = x_center+long_side//2
        low_y = y_center-short_side//2
        up_y = y_center+short_side//2
        rotation = np.array([[np.cos(angle), -np.sin(angle)],
                                        [np.sin(angle),  np.cos(angle)]])
        for idx in range(low_x, up_x+1):
            for y in [low_y, up_y]:
                new_x, new_y = np.around(np.matmul(np.array([idx, y]) - center, rotation) + center)
                img[int(new_y)][int(new_x)][2] = 255
        for idx in range(low_y, up_y+1):
            for x in [low_x, up_x]:
                new_x, new_y = np.around(np.matmul(np.array([x, idx]) - center, rotation) + center)
                img[int(new_y)][int(new_x)][2] = 255
    except FileNotFoundError:
        pass
    finally:
        img[0][0][2] = 255
        img[0][1][2] = 255
        img[0][2][2] = 255
        save_path = './Inference'
        Img_name = Img_data['name']
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        cv2.imwrite(os.path.join(save_path,f'{Img_name}_fracture.bmp'), img)

def returnannot_scaphoid(annot_path):
    with open(annot_path) as fp:
        annot = json.load(fp)[0]["bbox"]
    annot = [int(annot[0]), int(annot[1]), int(annot[2]), int(annot[3])]
    return annot

def returnannot_fracture(annot_path):
    with open(annot_path) as csvfile:
        annot = list(csv.reader(csvfile))
        x_center, y_center, long_side , short_side, angle = annot[1]
    
    return int(x_center), int(y_center), int(long_side), int(short_side), int(angle)

if __name__ == '__main__':
    with open('./3Fold.json') as f:
        data = json.load(f)
    Img_data = data['fold_0']['train'][130]
    # annot = returnannot_scaphoid(Img_data['scaphoid_annot'])
    # GTInference_scaphoid(Img_data)
    
    
    GTInference_fracture(Img_data)