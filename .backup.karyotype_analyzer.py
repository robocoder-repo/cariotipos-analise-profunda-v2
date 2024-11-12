


import cv2
import numpy as np
import sys

def analyze_karyotype(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return "Erro: Não foi possível carregar a imagem."

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Apply morphological operations to separate touching chromosomes
    kernel = np.ones((3,3), np.uint8)
    binary = cv2.erode(binary, kernel, iterations=1)
    binary = cv2.dilate(binary, kernel, iterations=1)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours based on area and aspect ratio to remove small noise and non-chromosome shapes
    min_area = 50
    max_area = 5000
    min_aspect_ratio = 1.5
    chromosomes = [cnt for cnt in contours if min_area < cv2.contourArea(cnt) < max_area]
    chromosomes = [cnt for cnt in chromosomes if cv2.boundingRect(cnt)[3] / cv2.boundingRect(cnt)[2] > min_aspect_ratio]
    
    chromosome_count = len(chromosomes)
    
    result = f"Detected {chromosome_count} chromosomes."
    if chromosome_count == 46:
        result += " This appears to be a normal human karyotype."
    elif chromosome_count < 46:
        result += " This may indicate chromosomal deletion or loss."
    elif chromosome_count > 46:
        result += " This may indicate chromosomal duplication or gain."
    
    return result

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python karyotype_analyzer.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = analyze_karyotype(image_path)
    print(result)


