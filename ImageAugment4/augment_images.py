from PIL import Image
import numpy as np
import os
import random

def image_augmenter(windmill_file, txt_files, out_shape, relative, results_dir, out_fname):

  if not os.path.exists(results_dir):
    os.makedirs(results_dir)

  masked_pixels = np.zeros(out_shape,dtype=bool)
  canvas = Image.new(mode='RGB', size=out_shape,color=(255,255,255))

  txt_fname = os.path.join(results_dir, out_fname + ".txt")
  txt_f = open(txt_fname, "w")

  imgs = 0
  c = 0

  random.seed(42)

  while imgs < 5 and c < len(txt_files):
    my_txt_file = txt_files[c]

    with open(my_txt_file, "r") as f:
      lst = [float(x) for x in f.read().split()]
    
    c+=1

    out_ht = 608
    out_w = 608

    classes = [i for i in lst[::5]]
    x_ctrs = [round(i*out_w,1) for i in lst[1::5]]
    y_ctrs = [round(i*out_ht,1) for i in lst[2::5]]
    widths = [round(i*out_w) for i in lst[3::5]]
    heights = [round(i*out_ht)  for i in lst[4::5]]

    location = []
    size = []
    rotation = []

    for i in range(len(x_ctrs)):
      location.append((x_ctrs[i],y_ctrs[i]))
      size.append((widths[i],heights[i]))
      rotation.append(random.randint(0,3)*90)

    for j in range(len(location)):
      #8 sources
      rand_index = random.randint(0, len(windmill_file)-1)
      windmill = Image.open(windmill_file[rand_index])

      with open(relative[rand_index], "r") as f:
        rel_lst = [float(x) for x in f.read().split()]

      rel_class = rel_lst[0]
      rel_x_ctr = rel_lst[1]
      rel_y_ctr = rel_lst[2]
      rel_width = rel_lst[3]
      rel_height = rel_lst[4]

      loc_x = location[j][0]
      loc_y = location[j][1]
      size_x = size[j][0]
      size_y = size[j][1]
      #size_x_add = size_x/2
      #size_y_add = size_y/2
      curr_rotation = rotation[j]

      imwidth, imheight = windmill.size

      #avg_ratio = ((size_x/imwidth) + (size_y /imheight)) / 2
      avg_ratio = ((size_x/(rel_width*imwidth)) + (size_y /(rel_height * imheight))) / 2
      new_size = (int(imwidth * avg_ratio), int(imheight*avg_ratio))
      size_x_add = new_size[0]/2
      size_y_add = new_size[1]/2

      my_corners = [int(loc_x-size_x_add)+5, int(loc_x+size_x_add)-5, int(loc_y-size_y_add)+5, int(loc_y+size_y_add)-5]
      my_pixel_vals = masked_pixels[int(loc_y-size_y_add)+5:int(loc_y+size_y_add)-5,int(loc_x-size_x_add)+5:int(loc_x+size_x_add)-5]
      
      if curr_rotation == 90 or curr_rotation == 270:
        my_corners = [int(loc_x-size_y_add)+5, int(loc_x+size_y_add)-5, int(loc_y-size_x_add)+5, int(loc_y+size_x_add)-5]
        my_pixel_vals = masked_pixels[int(loc_y-size_x_add)+5:int(loc_y+size_x_add)-5,int(loc_x-size_y_add)+5:int(loc_x+size_y_add)-5]

      if not all((i <= 608 and i >= 0) for i in my_corners) or any(my_pixel_vals.flatten()):
        #Try different rotation
        if curr_rotation % 180 == 0:
          my_corners = [int(loc_x-size_y_add)+5, int(loc_x+size_y_add)-5, int(loc_y-size_x_add)+5, int(loc_y+size_x_add)-5]
          my_pixel_vals = masked_pixels[int(loc_y-size_x_add)+5:int(loc_y+size_x_add)-5,int(loc_x-size_y_add)+5:int(loc_x+size_y_add)-5]
        else:
          my_corners = [int(loc_x-size_x_add)+5, int(loc_x+size_x_add)-5, int(loc_y-size_y_add)+5, int(loc_y+size_y_add)-5]
          my_pixel_vals = masked_pixels[int(loc_y-size_y_add)+5:int(loc_y+size_y_add)-5,int(loc_x-size_x_add)+5:int(loc_x+size_x_add)-5]
        curr_rotation += 90
        if not all((i <= 608 and i >= 0) for i in my_corners) or any(my_pixel_vals.flatten()):
          print("OVERLAP")
          continue

      
      #my_corners_x = my_corners[0:2]
      #my_corners_y = my_corners[2:]

      #my_corner_vals = []
      #for i in my_corners_y:
      #  for j in my_corners_x:
      #    my_corner_vals.append(masked_pixels[i][j])



      #Given they are rectangles not rotated- can just check if any of corners
      #if any(my_pixel_vals.flatten()):
      #  print("OVERLAP IN IMAGES")
      #  continue

      if curr_rotation == 360:
        curr_rotation = 0
      
      new_windmill = windmill.copy()
      new_windmill = new_windmill.resize(new_size)
      new_windmill = new_windmill.rotate(curr_rotation,expand=True,fillcolor=(255,255,255))

      new_location = (int(loc_x - size_x_add), int(loc_y - size_y_add))

      #my_x_ctr = (new_location[0]+rel_x_ctr * new_size[0]) / out_shape[1]
      #my_y_ctr = (new_location[1]+rel_y_ctr * new_size[1]) / out_shape[0]
      my_width = (rel_width * new_size[0]) / out_shape[1]
      my_height = (rel_height * new_size[1]) / out_shape[0]

      imgs +=1

      ###MAIN EDITS for rotate bounding box
      if curr_rotation == 90 or curr_rotation == 270:
        #rotates for mask as needed
        new_location = (int(loc_x - size_y_add), int(loc_y - size_x_add))
        canvas.paste(im=new_windmill,box=new_location)
        masked_pixels[int(loc_y-size_x_add)+10:int(loc_y+size_x_add)-10,int(loc_x-size_y_add)+10:int(loc_x+size_y_add)-10] = True
        # Rotate bounding box
        # (x, (rot/180)(height-2y)+y)
        # (h, w)
        my_y_scalar = ((curr_rotation - 90)/ 180) * (1 - 2 * rel_y_ctr) + rel_y_ctr
        my_x_scalar = ((curr_rotation - 270) / -180) * (1 - 2 * rel_x_ctr) + rel_x_ctr
        my_x_ctr = (new_location[0]+my_y_scalar * new_size[1]) / out_shape[1]
        my_y_ctr = (new_location[1]+my_x_scalar * new_size[0]) / out_shape[1]
        txt_f.write("{my_class} {x_ctr} {y_ctr} {width} {height}\n".format(my_class="0", x_ctr=my_x_ctr,y_ctr=my_y_ctr,width=my_height,height=my_width))
      else:
        #0 or 180
        canvas.paste(im=new_windmill,box=new_location)
        masked_pixels[int(loc_y-size_y_add)+10:int(loc_y+size_y_add)-10,int(loc_x-size_x_add)+10:int(loc_x+size_x_add)-10] = True
        #Rotate bounding box
        # (((rot-90)/180)(width-2y)+y, x)
        # (w, h)
        my_y_scalar = ((curr_rotation)/ 180) * (1 - 2 * rel_y_ctr) + rel_y_ctr
        my_x_scalar = ((curr_rotation)/ 180) * (1 - 2 * rel_x_ctr) + rel_x_ctr
        my_x_ctr = (new_location[0]+my_x_scalar * new_size[0]) / out_shape[1]
        my_y_ctr = (new_location[1]+my_y_scalar * new_size[1]) / out_shape[0]
        txt_f.write("{my_class} {x_ctr} {y_ctr} {width} {height}\n".format(my_class="0", x_ctr=my_x_ctr,y_ctr=my_y_ctr,width=my_width,height=my_height))
  
  masked_pixels = np.stack((masked_pixels, masked_pixels, masked_pixels), axis=2)
  mask = Image.fromarray((masked_pixels*255).astype(np.uint8))
  #mask = mask.rotate(angle=rotation,expand=False)
  #canvas = canvas.rotate(rotation,expand=False,fillcolor=(255,255,255))

  #display(mask)
  #display(canvas)

  txt_f.close()

  fpath = os.path.join(results_dir, out_fname + ".jpg")
  canvas.save(fpath)
  mask_fpath = os.path.join(results_dir,'_'.join([out_fname, '_mask2.png']))
  mask.save(mask_fpath)

  return [canvas, mask]
