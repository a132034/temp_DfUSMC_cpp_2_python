#LoadSmallMotionClip
#SaveReferenceImage
#FeatureExtractionAndTracking
#BundleAdjustment
#SavePointCloudPLY
#UndistortImages
#DenseMatching
#SaveDepthmapWTA
#SaveDepthmapFiltered
#SaveDepthmapRefined

import os
import cv2
import numpy as np

class DfUSMC:
    # load small motion clip을 생성자로 가져가면 될듯 한데
    
    images = []
    num_image = 0
    image_width = 0
    image_height = 0
    
    features = None
    num_feature = 0
    
    ud_mapx = None
    ud_mapy = None # undistorted->distorted mapping for dense matching
    
    du_mapx = None
    du_mapy = None # distorted->undistorted mapping for final visualization
    
    confidencemap = None
    depthmapWTA = None
    depthmapFiltered = None # outlier removal
    depthmapRefined = None
    depthmapConfidence = None
    
    cx = 0
    cy = 0
    f = 0
    k1 = 0
    k2 = 0
    f_new = 0
    poses = None
    inv_depths = None
    
    '''
    def __init__(self):
        pass
    def __del__(self):
        pass
    '''
    
    def load_small_motion_clip(self, path, refer_num=0):
        """
            path : video path  /  image folder path 
            refer_num : reference frame number in video 
        """
        #video
        if os.path.splitext(path)[1].lower() in (".avi", ".mov", ".mp4"):
            cap = cv2.VideoCapture(path)
            if cap.isOpened():
                num_image=cap.get(cv2.CAP_PROP_FRAME_COUNT)+1;
                print("num frame : ", num_image)
                num_image=np.min([30, num_image]) # limit 30 frames
            
                image_width=cap.get(cv2.CAP_PROP_FRAME_WIDTH);
                image_height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT);
                print("image size: ", image_width, " ", image_height)
                
                start = 0 
                end = num_image
                if refer_num <= 15:
                    start = refer_num
                else : 
                    end = refer_num
                count = 0
                for i in range(0, 30):
                    _, image = cap.read()
                               
                    if i > start and i < end:
                        self.images.append(image)
                        count+=1
                cap.release()
            num_image=count-1;
            print("we use ", num_image, " images in the beginning.")
            
        #image folder
        #else if False:# folder check
        
        else:
            print("path must be video path or image folder path")
            return
    
        print("load done")
        