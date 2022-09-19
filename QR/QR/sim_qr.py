import pyzbar.pyzbar as pyzbar
import qrcode
import cv2
from sim_mongo import *


class sim_qrcode():
    def __init__(self) -> None:
        pass
    
    def create_qrcode(data): # personal_id == string
        qr_img1 = qrcode.make(data)
        img_save_path = 'qr_data/' + data + '.png'
        qr_img1.save(img_save_path)
        
    def scan_qrcode():
        cap = cv2.VideoCapture(0)
        
        qr_data = []

        i = 0
        while(cap.isOpened()):
            ret, img = cap.read()

            cv2.rectangle((0.0),(0, 500), (500,0), (500,500))

            if not ret:
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
            decoded = pyzbar.decode(gray)

            for d in decoded: 
                x, y, w, h = d.rect

                barcode_data = d.data.decode("utf-8")
                barcode_type = d.type

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                text = '%s (%s)' % (barcode_data, barcode_type)
                cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
                
                #print(barcode_data)
                
                if barcode_data not in qr_data:
                    qr_data.append(barcode_data)
                    print(type(barcode_data))
                    print('data {} appended'.format(barcode_data))
                    
                result = sim_mongo.data_search(qr_data)
                print(result)

            cv2.imshow('img', img)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()