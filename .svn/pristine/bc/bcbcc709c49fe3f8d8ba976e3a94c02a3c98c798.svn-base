import pickle
import os 

def read_obj(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)



def write_obj(obj, file_path):
    if not os.path.isdir(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)
