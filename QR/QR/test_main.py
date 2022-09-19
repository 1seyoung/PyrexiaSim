from sim_mongo import *
from sim_qr import *

def preprogress(worker_array): # worker_array = [[id, startingtime], ...]
    for i in range(len(worker_array)):
        sim_qrcode.create_qrcode(worker_array[i][0])
        sim_mongo.data_insert(worker_array[i][0], worker_array[i][1])

def main():
    sim_qrcode.scan_qrcode()
    
if __name__ == "__main__":
	try:
		main()
	except:
		raise