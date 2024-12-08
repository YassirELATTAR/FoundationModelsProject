# import torchtoolbox.transform as transforms
from torch.utils.data import Dataset, DataLoader, Subset
import pandas as pd
import os
from PIL import Image
import cv2
import numpy as np
import torchvision.transforms.functional as F
import torch
class Derm_Dataset(Dataset):
    def __init__(self, df: pd.DataFrame, root, train=False,val=False,test=False,transforms=None,binary=False,data_percent=1):
        """
		Class initialization
		Args:
			df (pd.DataFrame): DataFrame with data description
			train (bool): flag of whether a training dataset is being initialized or testing one
			transforms: image transformation method to be applied
			meta_features (list): list of features with meta information, such as sex and age

		"""
        if train==True:
            self.df = df[df['split']=='train']
            self.df = self.df.sample(frac=1, random_state=42).reset_index(drop=True)
            half_rows = int(len(self.df) * data_percent)
            self.df=self.df.head(half_rows)
        elif val==True:
            self.df = df[df['split'] == 'val']
        elif test==True:
            self.df = df[df['split'] == 'test']
        self.transforms = transforms
        self.root=root
        self.binary=binary

    # import torchsnooper
    # @torchsnooper.snoop()
    def __getitem__(self, index):
        filename = self.df.iloc[index]['image']
        # im_path = '/home/share/Eval_Data/ISIC_2019_Training/'+filename+'.jpg'

        im_path = str(self.root)+str(filename)
        # Use PIL to load the image directly in RGB format
        try:
            x = Image.open(im_path).convert('RGB')
        except IOError:
            print('Error opening file:', im_path)
            x = None  # Or handle the error as appropriate for your application

        # print(x)
        # Apply transformations if any
        if x is not None and self.transforms:
            x = self.transforms(x)
            if self.binary==True:
                y = self.df.iloc[index]['binary_label']
            else:
                y = self.df.iloc[index]['label']
        # Here we need to change x as image and question pair and y as answer. 
        # Need to make a custom class for the new multimodal dataset
        return x,y,filename

    def __len__(self):
        return len(self.df)
