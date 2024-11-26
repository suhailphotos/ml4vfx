import numpy as np
import pickle
import random
import os
from tqdm import tqdm
import cv2

DATADIR = "/Users/felipepesantez/Documents/development/datasets/Animal Image Dataset-Cats, Dogs, and Foxes"
CATEGORIES = ["dog","fox"]
IMG_SIZE = 50

training_data = []

def create_tr_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR, category)
        clas_num = CATEGORIES.index(category)

        for img in tqdm(os.listdir(path)):
            try:
                img_arr = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE)
                resized_arr = cv2.resize(img_arr, (IMG_SIZE, IMG_SIZE))
                training_data.append([resized_arr, clas_num])
            except Exception as e:
                pass

create_tr_data()
print(len(training_data))

random.shuffle(training_data)

X = []
y = []

for features, labels in training_data:
    X.append(features)
    y.append(labels)

X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

with open("X.pkl","wb") as Xfile:
    pickle.dump(X, Xfile)

with open("y.pkl","wb") as yfile:
    pickle.dump(y, yfile)
