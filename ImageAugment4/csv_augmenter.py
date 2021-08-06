from PIL import Image
import numpy as np
import os
import random
import glob
from augment_images import image_augmenter
from shutil import copyfile

my_src_dir = "/hdd/dataplus2021/ct260/windmills/cropped"
src_files = glob.glob(my_src_dir + "/*.png")

#my_txt_dir = "/hdd/dataplus2021/share/data/synthetic_labels"
#all_txt_files = glob.glob(my_txt_dir + "/*.txt")
#my_txt_files = random.sample(all_txt_files, 10)
with open("experiment2txts.txt", "r") as f:
  my_txt_files = f.read().split()

#new_txt_dir = "/hdd/dataplus2021/fcw/ImageAugment3/results3/"

#Maintains order
my_rel_dir = "/hdd/dataplus2021/fcw/ImageAugment3/box_txt_files/"
my_relative = [ my_rel_dir + x[x.rfind("/")+1:].replace(".png", ".txt") for x in src_files]


#Need to edit box since I change it
#for txt_file in my_txt_files:
#  fname = txt_file.split("synthetic_labels/")[1]
#  copyfile(txt_file, new_txt_dir+fname)

#my_file = "wnd_xview_bkg_sd0_8.txt"
#my_src = "windmill.png"


#Should be experiments1

#Change to src_files
for i in range(len(src_files)):
  #my_src_file = src_files[i]
  my_txt_file = my_txt_files[i]
  print(my_txt_file)

  #with open(my_txt_file, "r") as f:
  #    lst = [float(x) for x in f.read().split()]

  #out_ht = 608
  #out_w = 608

  #classes = [i for i in lst[::5]]
  #x_ctrs = [round(i*out_w,1) for i in lst[1::5]]
  #y_ctrs = [round(i*out_ht,1) for i in lst[2::5]]
  #widths = [round(i*out_w) for i in lst[3::5]]
  #heights = [round(i*out_ht)  for i in lst[4::5]]

  #(x_center, y_center)
  #my_location = []
  #(width, height)
  #my_size = []
  #my_rotation = []
  #my_src_files = []
  #my_rel_files = []
  #for i in range(len(x_ctrs)):
  #  my_location.append((x_ctrs[i],y_ctrs[i]))
  #  my_size.append((widths[i],heights[i]))
  #  my_rotation.append(random.randint(0,3)*90)
  #  rand_index = random.randint(0, len(x_ctrs)-1)
  #  my_src_files.append(src_files[rand_index])
  #  my_rel_files.append(my_relative[rand_index])

  random.seed(42)

  txt_files = [my_txt_file]
  for k in range(0,10):
    txt_files.append(my_txt_files[random.randint(len(src_files), len(my_txt_files)-1)])

  my_out_shape = (608,608)
  my_res_folder = "results10"

  txt_file_address = my_txt_file[my_txt_file.find("sd"):my_txt_file.find(".txt")]
  #src_address = my_src_file[my_src_file.find("cropped/")+len("cropped/"):my_src_file.find(".png")]
  #my_out_fname  = src_address + "_" + txt_file_address
  my_out_fname  = "source_" + txt_file_address
  print(my_out_fname)

  #NEED TO DECLARE
  #Choose naming convention
  #Can declare relative dir
  #my_relative = my_rel_dir + src_address + ".txt"

  #Can pass in all sources and all relatives

  image_augmenter(src_files,txt_files,my_out_shape,my_relative, my_res_folder,my_out_fname)

