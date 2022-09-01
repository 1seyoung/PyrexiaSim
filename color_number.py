import tensorflow as tf
import cv2
import numpy as np
import math
import pytesseract


from collections import Counter
from numba import jit


class Color_number():

    @jit(nopython=True)
    def camera_detection(before_list):
        cap = cv2.VideoCapture(0)
        r_nu_count = []
        b_nu_count = []
        while(True):
            pytesseract.pytesseract.tesseract_cmd = r'C:\Users\1wkdy\tesseract'

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
                                                cv2.RETR_LIST,
                                                cv2.CHAIN_APPROX_SIMPLE)
            red_rect = 0

            # 파란색 박스
            contours_blue, hierarchy = cv2.findContours(blue_mask,
                                                cv2.RETR_LIST,
                                                cv2.CHAIN_APPROX_SIMPLE)

            blue_rect = 0

            contours_b = False
            contours_r = False

            if contours_red and not contours_blue:
                contours_r = True
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

            if contours_blue and not contours_red:
                contours_b = True
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
            
            if contours_red and contours_blue:
                contours_r = True
                contours_b = True
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

            if contours_red:
                color ='red'
                r_after_items = Counter(r_nu_count)
                r_before_items = Counter(before_list)

                after_number = r_after_items.most_common(n = red_rect)
                before_number = r_before_items.most_common(n = red_rect)

                if after_number == before_number:
                    pass
                else:
                    return color,after_number,contours_r,contours_b

            if contours_blue:
                color = 'blue'
                b_after_items = Counter(b_nu_count)
                b_before_items = Counter(before_list)
            
                after_number = b_after_items.most_common(n = blue_rect)
                before_number = b_before_items.most_common(n = blue_rect)

                if after_number == before_number:
                    pass
                else:
                    return color,after_number,contours_r,contours_b
        
                
            cv2.imshow('bgr', img_color)
            k = cv2.waitKey(1)
            if k == 27:
                break

            # if contours_red and contours_blue:
                
            #     cv2.imshow('bgr', img_color)
            #     k = cv2.waitKey(10)
            #     if k == 27:
            #         break

            # elif contours_red and not contours_blue:

            #     cv2.imshow('bgr', img_color)
            #     k = cv2.waitKey(10)
            #     if k == 27:
            #         break
            #     # cv2.imshow('red_mask',red_mask)
            # elif not contours_red and contours_blue:
                
            #     cv2.imshow('bgr', img_color)
            #     k = cv2.waitKey(10)
            #     if k == 27:
            #         break
            #     # cv2.imshow('blue_mask',blue_mask)
            # else:
            #     print("no color")
            #     cv2.imshow('bgr', img_color)
            #     k = cv2.waitKey(10)
            #     if k == 27:
            #         break
            #     # cv2.imshow('No_color', img_color)


        cap.release()
        # cv2.destroyAllWindows()
        
    @jit(nopython=True)
    def trans_data():
        r_data_list = []
        b_data_list = []
        r_data_collect = []
        b_data_collect = []
        i=0

        while(True):
            i+=1
            _, _,red_c, blue_c= Color_number.camera_detection(r_data_list)

            if red_c and not blue_c:
                print('red')
                if len(r_data_collect) < 5:
                    after_color, r_data_list,_,_ = Color_number.camera_detection(r_data_list)
                    for ln in r_data_list:
                        r_data_collect.append(ln[0])
                    

                    print(f'{i}r_데이터수집 : ',r_data_collect)
                else:
                    data_items = Counter(r_data_collect)
                    r_best_number = data_items.most_common(n = len(r_data_list))
                    r_data_collect = []
                    numbers_r = []
                    numbers_b = []
                    print('best number',r_best_number)
                    for ln in r_best_number:
                        numbers_r.append(ln[0])
                    color = 'red'
                    return numbers_r, numbers_b

            if not red_c and blue_c:
                print('blue')
                if len(b_data_collect) < 5:
                        after_color,b_data_list,_,_ = Color_number.camera_detection(b_data_list)
                        for ln in b_data_list:
                            b_data_collect.append(ln[0])

                        print(f'{i}b_데이터수집 : ',b_data_collect)
                else:
                    b_data_items = Counter(b_data_collect)
                    b_best_number = b_data_items.most_common(n = len(b_data_list))
                    b_data_collect = []
                    numbers_r = []
                    numbers_b = []
                    color = 'blue'
                    print('best number',b_best_number)
                    for ln in b_best_number:
                        numbers_b.append(ln[0])

                    return numbers_r, numbers_b

            if red_c and blue_c:
                print('red+blue')
                if len(r_data_collect) < 5:

                    after_color, r_data_list,_,_ = Color_number.camera_detection(r_data_list)

                    for ln in r_data_list:
                        r_data_collect.append(ln[0])

                    print(f'{i}r_데이터수집 : ',r_data_collect)

                if len(b_data_collect) < 5:

                    after_color_b,b_data_list,_,_ = Color_number.camera_detection(b_data_list)

                    for ln in b_data_list:
                        b_data_collect.append(ln[0])

                    print(f'{i}b_데이터수집 : ',b_data_collect)

                else:
                    
                    data_items = Counter(r_data_collect)
                    b_data_items = Counter(b_data_collect)

                    r_best_number = data_items.most_common(n = len(r_data_list))
                    
                    b_best_number = b_data_items.most_common(n = len(b_data_list))

                    r_data_collect = []
                    b_data_collect = []

                    numbers_r = []
                    numbers_b = []

                    print('best number',r_best_number)
        
                    print('b_best number',b_best_number)

                    for ln in r_best_number:
                        numbers_r.append(ln[0])
                    
                    for ln in b_best_number:
                        numbers_b.append(ln[0])

                    return numbers_r, numbers_b 


# numbers_r, numbers_b = Color_number.trans_data()
# print(numbers_b, numbers_r)
# # while(1):
#     numbers_r, numbers_b = Color_number.trans_data()
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         cv2.destroyAllWindows()
#         break