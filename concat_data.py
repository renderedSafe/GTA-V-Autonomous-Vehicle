# concat_data.py

import numpy as np
from random import shuffle

starting_num = 18
ending_num = 57
concat_data = np.load('1.controller-waypoint-{}.npy'.format(starting_num))
file_num = 18
for i in range(starting_num + 1, ending_num + 1):

    train_data = np.load('1.controller-waypoint-{}.npy'.format(i))
    print('Loaded training_data-{}.npy'.format(i))
    print(np.shape(train_data))
    concat_data = np.concatenate((concat_data, train_data))
    if len(concat_data) >= 1000:
        # saving the file, adding one to the savefile number, and emptying the storage list
        print('Reached {} samples in this file, starting another'.format(len(concat_data)))
        # shuffle(concat_data)
        np.save('concat-WASD_training_data-{}.npy'.format(file_num), concat_data)
        file_num += 1
        concat_data = np.load('1.controller-waypoint-{}.npy'.format(file_num + 1))

print('Reached the end, samples in last file: {}'.format(len(concat_data)))
shuffle(concat_data)
np.save('concat-controller-waypoint-training-data-{}.npy'.format(file_num), concat_data)



