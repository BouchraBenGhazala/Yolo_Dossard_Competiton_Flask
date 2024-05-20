from ultralytics import YOLO
import cv2
from paddleocr import PaddleOCR
import os


ocr = PaddleOCR(use_angle_cls=True, lang='en')

model = YOLO('Detectors/DossardDetector3.pt')


#function to extract text from region of interest detected
def extract_dossard(region_detected):
    texts = ocr.ocr(region_detected, cls=True)
    texts_extracted = []
    for text in texts:
        if text is not None:
            for line in text:
                if line[1][1] > 0.5:
                    try:
                        extracted_int = int(line[1][0])  # Try to convert to integer
                        texts_extracted.append(extracted_int)
                        print("line: " + str(extracted_int))
                    except ValueError:
                        print(f"Skipping non-integer text")
                        continue  # Skip non-integer text
                
                print("line: " + str(line[1][0]))

    return texts_extracted
          


#Function to detect bibs from images
def detect_dossard(image):
    
    results = model.predict(image)
    extracted_bibs = [] 

    # Read image file
    image = cv2.imread(image)

    for result in results:

        boxes = result.boxes

        if len(boxes) != 0:
            
            for box in boxes:

                print("Object type:", box.cls[0].item())
                print("Coordinates:", box.xyxy[0].tolist())
                print("Probability:", box.conf[0].item())

                conf = round(box.conf[0].item(), 2)
                if conf > 0.55 :

                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    # Crop the region from the original image
                    region = image[y1:y2, x1:x2]
                    extracted_texts = extract_dossard(region)

                    for extracted_bib in extracted_texts:
                        if extracted_bib is not None:
                            extracted_bibs.append(extracted_bib)
    
    return extracted_bibs

    