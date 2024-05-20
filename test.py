import cv2
from ultralytics import YOLO
from paddleocr import PaddleOCR

# Charger le modèle YOLO
model_yolo = YOLO('best.pt')

# Charger le modèle OCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Charger l'image
image_path = 'temp/319309273_6118836224899374_1526423061814566126_n.jpg'
image = cv2.imread(image_path)

# Détecter les objets avec YOLO
results_yolo = model_yolo(image)

# Parcourir les résultats de YOLO
for result_yolo in results_yolo:
    boxes = result_yolo.boxes.xyxy
    # Parcourir les boîtes englobantes
    for box in boxes:
        x1, y1, x2, y2 = box
        # Extraire la ROI de l'image
        roi = image[int(y1):int(y2), int(x1):int(x2)]
        # Appliquer l'OCR à la ROI
        result = ocr.ocr(roi, cls=True)
        if result is not None:
             for idx in range(len(result)):
                res = result[idx]
                if res is not None:
                     for line in res:
                         print(line[1][0])