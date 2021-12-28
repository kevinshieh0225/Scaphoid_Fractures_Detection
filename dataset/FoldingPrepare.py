import os
import json
from sklearn.utils import shuffle
from sklearn.model_selection import KFold

def FoldingPrepare():
    name = []
    img_path = []
    img_crop_path = []
    label = []
    scaphoid_annot = []
    fracture_annot = []

    img_root = './images/'
    for n, directory in enumerate(reversed(os.listdir(img_root))):
        directory_path = os.path.join(img_root, directory)
        for filename in os.listdir(directory_path):
            img_path.append(os.path.join(directory_path, filename))
            label.append(n)
            img_name = filename.split('.')[0]
            name.append(img_name)
            img_crop_path.append(os.path.join(directory_path, f'{img_name}_fracture.bmp'))
            scaphoid_annot.append(f'./Annotations/Scaphoid_Slice/{img_name}.json')
            fracture_annot.append(f'./Annotations/Fracture_Coordinate/{img_name}.csv')

    name, img_path,img_crop_path, label, scaphoid_annot, fracture_annot= shuffle(name, img_path,img_crop_path, label, scaphoid_annot, fracture_annot, random_state=2)
    kf = KFold(n_splits=3, shuffle=True, random_state=100)
    Foldset = {}
    for n, (train_index, val_index) in enumerate(kf.split(img_path)):
        fold_name = f'fold_{n}'
        Foldset[fold_name] = {}
        for state in [['train', train_index], ['val', val_index]]:
            Foldset[fold_name][state[0]] = []
            for idx in state[1]:
                set = {
                    'name':name[idx],
                    'img_path':img_path[idx], 
                    'img_crop_path':img_crop_path[idx], 
                    'label':label[idx], 
                    'scaphoid_annot':scaphoid_annot[idx], 
                    'fracture_annot':fracture_annot[idx]
                }
                Foldset[fold_name][state[0]].append(set)
        # normal = 0
        # fracture = 0
        # for label in val_index:
        #     if(label_path[label]):
        #         fracture += 1
        #     else:
        #         normal += 1
        # print(f'Normal: {normal}\tFracture: {fracture}')

    with open('3Fold.json', 'w') as f:
        json.dump(Foldset, f)

if __name__  == '__main__':
    FoldingPrepare()

        