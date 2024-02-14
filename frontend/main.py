import cv2 
import requests
from pyzbar.pyzbar import decode
import winsound

cap = cv2.VideoCapture(0)

def convert(code):
    return int(code.decode('utf-8'))

def get_product(code):
    try:
        response = requests.get(f"http://localhost:2000/product/{code}")
        result = response.json()

        return result['data']
    except Exception as err:
        print(err)


def main():
    while cap.isOpened():
        success,frame = cap.read()
        frame  = cv2.flip(frame,1)
        detectedBarcode = decode(frame)

        for barcode in detectedBarcode:
          temp = ""
          if barcode.data != "":
            result = str(convert(barcode.data))
            cv2.putText(frame, result, (50,50), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,255),2)

            print(f"{temp} != {result}")

            if (temp != result):
              temp = result
              winsound.Beep(1000, 200)

              data = get_product(result)
              if data is not None:
                print(f"{result}: {data['name']} Rp {data['price']}")
              else:
                print(f"{result}: Tidak ditemukan")

        cv2.imshow('scanner' , frame)

        if cv2.waitKey(1) == ord('q'):
            break

main()