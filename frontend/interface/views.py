from django.shortcuts import render
from django.http import JsonResponse
import cv2
import threading
import requests
from pyzbar.pyzbar import decode
import winsound

# Global variable to store the last scanned barcode
last_scanned_barcode = None

# Create your views here.
def scanner(request):
    try:
        global last_scanned_barcode
        if last_scanned_barcode is not None:
            product_data = get_product(last_scanned_barcode)
            last_scanned_barcode = None
            return JsonResponse({'product_data': product_data})

        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'scanning.html')

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def convert(code):
    return int(code.decode('utf-8'))

def get_product(code):
    try:
        response = requests.get(f"http://localhost:2000/product/{code}")
        result = response.json()
        return result['data']
    except Exception as err:
        print(err)

def barcode_scanner(frame):
    detectedBarcode = decode(frame)

    for barcode in detectedBarcode:
        if barcode.data != "":
            result = str(convert(barcode.data))
            winsound.Beep(1000, 200)
            data = get_product(result)
            if data is not None:
                print(f"{result}: {data['name']} Rp {data['price']}")
                global last_scanned_barcode
                last_scanned_barcode = result
            else:
                print(f"{result}: Tidak ditemukan")

# You can call barcode_scanner(frame) to scan barcodes from frames.
