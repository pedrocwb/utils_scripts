import os
import cv2

datadir = 'C:\\Users\\pedro.moreira\Desktop\\NFE\\\data\\curitiba_img'
for i, img in enumerate(os.listdir(datadir)):
    img = cv2.imread(os.path.join(datadir, img))
    cv2.imwrite(datadir + "/Prefeitura_Curitiba_%d.jpg" % i, img)