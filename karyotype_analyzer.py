

import cv2
import numpy as np
import sys

def analyze_karyotype(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return "Erro: Não foi possível carregar a imagem."

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours based on area to remove small noise
    min_area = 100
    chromosomes = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    
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

