import numbers
import tensorflow as tf
import cv2
import numpy as np
import math
import pytesseract
from collections import Counter

class camera_data():
    def __init__(self) -> None:
        pass

    def data_analysis(data_list):
        data_collect = []
        numbers = []

        data_items = Counter(data_collect)
        best_number = data_items.most_common(n = len(data_list))

        for ln in best_number:
            numbers.append(ln[0])
        
        return numbers

    def camera_detection():
        cap = cv2.VideoCapture(0)
        r_nu_count = []
        b_nu_count = []
        while(1):
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\tesseract'

            ret, img_color = cap.read()
            hsvFrame = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)

            hImg,wIng,_ = img_color.shape

            red_lower = np.array([160, 90, 114], np.uint8)
            red_upper = np.array([180, 255, 255], np.uint8)
            red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

            blue_lower = np.array([0, 201, 255], np.uint8)
            blue_upper = np.array([140, 255, 255], np.uint8)
            blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

            kernal = np.ones((5, 5), "uint8")

            # For red color
            red_mask = cv2.dilate(red_mask, kernal)

            # For blue color
            blue_mask = cv2.dilate(blue_mask, kernal)
            
                                    
            cong = r'--oem 3 --psm 6 outputbase digits'
            box_red = pytesseract.image_to_boxes(red_mask,config=cong)
            box_blue = pytesseract.image_to_boxes(blue_mask,config=cong)

            # 빨간색 박스
            contours_red, hierarchy = cv2.findContours(red_mask,
                                                cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)
            red_rect = 0

            # 파란색 박스
            contours_blue, hierarchy = cv2.findContours(blue_mask,
                                                cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)
            blue_rect = 0

        

            for pic, contour in enumerate(contours_blue):
                area = cv2.contourArea(contour)
                if(area > 300):
                    x, y, w, h = cv2.boundingRect(contour)
                    img_color = cv2.rectangle(img_color, (x, y), 
                                            (x + w, y + h), 
                                            (255, 0, 0), 2)
                    blue_rect +=1

            for b in box_blue.splitlines():
                b =b.split(' ')
                
                x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])

                cv2.rectangle(img_color, (x,hImg-y),(w,hImg-h),(255,0,0),3)
                cv2.putText(img_color,b[0],(x,hImg-y+25),cv2.FONT_HERSHEY_COMPLEX,1,(255,50,50),2)
                b_nu_count.append(b[0])

            
            
            red_rect = 0
            
            for pic, contour in enumerate(contours_red):
                area = cv2.contourArea(contour)
                if(area > 300):
                    x, y, w, h = cv2.boundingRect(contour)
                    img_color = cv2.rectangle(img_color, (x, y), 
                                            (x + w, y + h), 
                                            (0, 0, 255), 2)
                    red_rect +=1

            for b in box_red.splitlines():
                b =b.split(' ')
                
                x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])

                cv2.rectangle(img_color, (x,hImg-y),(w,hImg-h),(0,0,255),3)
                cv2.putText(img_color,b[0],(x,hImg-y+25),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)
                r_nu_count.append(b[0])

    
            r_data_collect = []
            b_data_collect = []

            # cv2.imshow('bgr', img_color)
            cv2.imshow('red', red_mask)
            cv2.imshow('blue', blue_mask)
            # cap.release()

            if contours_red and not contours_blue:
                for ln in r_nu_count:
                        r_data_collect.append(ln[0])
        
                return ['red'], [r_data_collect],red_rect,blue_rect

            if not contours_red and contours_blue:
                for ln in b_nu_count:
                        b_data_collect.append(ln[0])

                return ['blue'], [b_data_collect],red_rect,blue_rect
            

            # if not contours_red and not contours_blue:
            #     # print('nothing')
            #     # cv2.imshow('not', img_color)
                
            if contours_red and contours_blue:
            
                for ln in r_nu_count:
                    r_data_collect.append(ln[0])


                for ln in b_nu_count:
                    b_data_collect.append(ln[0])

                return ['red','blue'], [r_data_collect,b_data_collect],red_rect,blue_rect

    def trans_data():
        r_data_collect = []
        b_data_collect = []
        i=0
        while(True):
            i+=1
            color, data_list,red_rect,blue_rect = camera_data.camera_detection()

            if len(color) == 1 :
                if color[0] == 'red':
                    if len(r_data_collect) < 5:
                        # color, data_list = camera_detection()
                        for ln in data_list[0]:
                            r_data_collect.append(ln)

                    else:
                        data_items = Counter(r_data_collect)
                        r_best_number = data_items.most_common(n = red_rect)
                        r_data_collect = []
                        numbers = []
           
                        for ln in r_best_number:
                            numbers.append(ln[0])
           
                        return color[0],[numbers]
                else:
                    if len(b_data_collect) < 5:
                        # color, data_list = camera_detection()
                        for ln in data_list[0]:
                            b_data_collect.append(ln)

                    else:
                        b_data_items = Counter(b_data_collect)
                        b_best_number = b_data_items.most_common(n = blue_rect)
                        b_data_collect = []
                        numbers = []
                        
                        for ln in b_best_number:
                            numbers.append(ln[0])

                        return color[0],[numbers]
            else:
                if len(r_data_collect) < 5 and len(b_data_collect) < 5:
         
                    if len(r_data_collect) > len(b_data_collect) :
                 
                        for ln in data_list[1]:
                            b_data_collect.append(ln)

                  
                    if len(r_data_collect) < len(b_data_collect) :

                        for ln in data_list[0]:
                            r_data_collect.append(ln)
                  
                    if len(r_data_collect) == len(b_data_collect) :
                        for ln in data_list[0]:
                            r_data_collect.append(ln)
                     
                    
                elif len(r_data_collect) >=5 and len(b_data_collect) < 5:
                    if len(r_data_collect) >=5:
                        for ln in data_list[1]:
                            b_data_collect.append(ln)

                else:
                    r_data_items = Counter(r_data_collect)
                    r_best_number = r_data_items.most_common(n = red_rect)
                    r_data_collect = []
                    r_numbers = []
                
                    for ln in r_best_number:
                        r_numbers.append(ln[0])

                    b_data_items = Counter(b_data_collect)
                    b_best_number = b_data_items.most_common(n = blue_rect)
                    b_data_collect = []
                    b_numbers = []
        
                    for ln in b_best_number:
                        b_numbers.append(ln[0])

                    return [color[0],color[1]],[r_numbers,b_numbers]

    def main():
        while(1):
            color, number = camera_data.trans_data()
            print(color, number)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            else:
                return color,number


