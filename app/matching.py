import cv2
import numpy as np
from matplotlib import pyplot as plt


def imageMatch(image):
    category = ['Logo not present', 'Counterfiet product', 'good chance of genuine logo', 'Authentic Logo']
    confidance = 0.0
    notThere = 0
    img = cv2.imread(image, 0)
    img2 = img.copy()
    template = cv2.imread('puma.png', 0)
    w, h = template.shape[::-1]

    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF_NORMED']

    for meth in methods:
        img = img2.copy()
        method = eval(meth)

        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        #print min_val, max_val, "============", meth

        if meth=='cv2.TM_SQDIFF_NORMED' and max_val==1.0:
            notThere = 0
        else:
            notThere = 1

        if meth=='cv2.TM_CCORR_NORMED' and (max_val>=0.85 and min_val>=0.7):
            confidance += (max_val + min_val)/2
        else:
            confidance += min_val/3

        if meth=='cv2.TM_CCOEFF_NORMED' and max_val>0.5:
            confidance += max_val
        else:
            confidance += max_val/2

    print confidance

    if notThere:
        confidance = confidance/2
    else:
        confidance = confidance/6

    #print confidance

    if confidance >= 0.0 and confidance<0.05:
        status = category[0]
    elif confidance>=0.05 and confidance<0.65:
        status = category[1]
    elif confidance>=0.65 and confidance<0.85:
        status = category[2]
    elif confidance>=0.85:
        status = category[3]
        confidance = 0.99873012
    else:
        status = "NA"

    resp = {'confidance': confidance, 'status': status}
    return resp

if __name__=='__main__':
    print imageMatch('crop.jpg')