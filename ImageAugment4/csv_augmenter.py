from PIL import Image
import numpy as np
import os
import random
import glob
from augment_images import image_augmenter
from shutil import copyfile
import re
from get_distribution import return_distribution
from pathlib import Path

def multiple_replace(dict, text):
  # Create a regular expression  from the dictionary keys
  regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

  # For each match, look-up corresponding value in dictionary
  return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 

#####edits to make
#main src dir
#for each domain
#for all src files
#need src dir for crops and labels- src_files, relative
#need distribution for each domain to sample from- create txt_file

#csv_augmenter
#remove imgs < 5

replacer = {
  "images":"labels",
  ".jpg":".txt"
}

cropped = "/scratch/public/cropped_turbines/"
domains = ["EM", "NW", "SW"]

augmented_out_folder = "/scratch/public/augmented_images/"

my_out_shape = (608,608)


for domain in domains:

  src_img_dir = f"{cropped}images/{domain}"

  #Cropped images
  cropped_imgs = glob.glob(src_img_dir + "/*.jpg")
  #Relative labels
  cropped_labels = [multiple_replace(replacer, src_img) for src_img in cropped_imgs]

  num_imgs, width_turbines, height_turbines = return_distribution(domain)

  my_res_folder = f"/scratch/public/augmented_images/{domain}/"

  #Change to src_files
  for i in range(0,200):

    random.seed(42)

    #windmill_file = src_imgs[i]
    #src_name = Path(windmill_file).stem

    my_out_fname  = f"src_{domain}_mask{i}"
    print(my_out_fname)

    #Can pass in all sources and all relatives
    image_augmenter(cropped_imgs,width_turbines, height_turbines,my_out_shape,cropped_labels, my_res_folder,my_out_fname, i)

