# Image-Augmentation

sample_txts.py- From a directory containing txt files (in YOLOv3 format- contain location/size information), it samples 100 of these txt files and saves into an output file

experiment2txts.txt- Sample output file from sample_txts.py

csv_augmenter.py- Accepts txt file containing YOLOv3 files, cropped wind turbines (and coinciding bounding box information in YOLOv3 format), then samples txt files and runs augment_images.py

augment_images.py- Samples wind turbines and places them in specified location/size (based on sampled txt file) with random rotation (while preventing overlap with border/each other), performs same transformations to make coinciding binary mask, calculates relative size/positioning data for YOLOv3 bounding box txt file

results9 folder- Contains output of running csv_augmenter.py- Several augmented images with coinciding binary masks and YOLOv3 bounding box txt files
