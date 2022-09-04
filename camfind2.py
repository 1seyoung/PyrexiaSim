import tensorflow as tf
import cv2
import numpy as np
import pytesseract


class camera_data():
    def __init__(self) -> None:
        pass

    def camera_detection():
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        r_nu_count = []
        b_nu_count = []
        while(True):
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

            red_mask_noise = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernal)
            blue_mask_noise = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernal)
            # # For red color
            # red_mask = cv2.dilate(red_mask_noise, kernal)

            # # For blue color
            # blue_mask = cv2.dilate(blue_mask_noise, kernal)

            
                                    
            cong = r'--oem 3 --psm 6 outputbase digits'
            box_red = pytesseract.image_to_boxes(red_mask_noise,config=cong)
            box_blue = pytesseract.image_to_boxes(blue_mask_noise,config=cong)

           
            # 파란색 박스
            contours_blue, _ = cv2.findContours(blue_mask,
                                                cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)
            blue_rect = 0

            for _, contour in enumerate(contours_blue):
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
                print(f'blue_data',b[0])
                b_nu_count.append(b[0])


             # 빨간색 박스
            contours_red, _ = cv2.findContours(red_mask,
                                                cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)
            red_rect = 0
            
            for _, contour in enumerate(contours_red):
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
                print(f'red_data',b[0])
                r_nu_count.append(b[0])

            cv2.imshow('bgr',img_color)
            cv2.imshow('red',red_mask_noise)
            cv2.imshow('blue',blue_mask_noise)
            if cv2.waitKey(10) == ord('q'):
                break
            
            r_data_collect = []
            b_data_collect = []

            
            if contours_red and not contours_blue:
                for ln in r_nu_count:
                        r_data_collect.append(ln[0])
        
                return ['red'], [r_data_collect]

            elif not contours_red and contours_blue:
                for ln in b_nu_count:
                        b_data_collect.append(ln[0])

                return ['blue'], [b_data_collect]
            

            elif not contours_red and not contours_blue:
                pass
             
                
            # elif contours_red and contours_blue:
            else:
                for ln in r_nu_count:
                    r_data_collect.append(ln[0])


                for ln in b_nu_count:
                    b_data_collect.append(ln[0])

                return ['red','blue'], [r_data_collect,b_data_collect]

        cap.release()

    def main():
        while(True):
            color, number = camera_data.camera_detection()
            print(color, number)

            print(f'trans', color, number)
            
            if len(color) == 1 :
                if len(number[0]) > 0:
                    if color[0] == 'red':
                        return [color[0]],[number[0]]
                    else:
                        return [color[0]],[number[0]]
                else:
                    pass
            else:
                if len(number[0]) > 0  and len(number[1]) >0:
                    return [color[0],color[1]],[number[0],number[1]]
                else:
                    print("둘다 한번에 읽히지않음")
                    pass

