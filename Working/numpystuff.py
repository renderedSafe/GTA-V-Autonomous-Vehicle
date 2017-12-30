import numpy as np
import cv2
from PIL import Image
import math
import matplotlib.pyplot as plt
import scipy

batch = np.load('training_data-1.npy')
index = 59

img = batch[index][0]
user_input = batch[index][1]


# print(batch[index])
print('User input: {}'.format(user_input))
print('Shape of img data: {}'.format(np.shape(img)))


# img = img.swapaxes(0,2).swapaxes(0,1)

# ----------Uncomment for cv2 imshow display--------------------
# img = Image.fromarray(img, 'RGB')
# cv2.imshow('window', np.array(img))
# input()


# ---------Uncomment for matplotlib image  display---------------
plt.imshow(img)
plt.show()

