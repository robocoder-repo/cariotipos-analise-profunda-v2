






import cv2
import numpy as np
import sys

def analyze_karyotype(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return "Erro: Não foi possível carregar a imagem."

    # Pré-processamento
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    
    # Binarização
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Operações morfológicas
    kernel = np.ones((3,3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    # Transformação de distância
    dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist, 0.5*dist.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    
    # Encontrar contornos
    contours, _ = cv2.findContours(sure_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtrar contornos
    min_area = 30  # Reduzido para capturar cromossomos menores
    max_area = 5000  # Aumentado para incluir possíveis grupos de cromossomos
    min_aspect_ratio = 1.05  # Reduzido para capturar cromossomos mais arredondados
    chromosomes = [cnt for cnt in contours if min_area < cv2.contourArea(cnt) < max_area]
    chromosomes = [cnt for cnt in chromosomes if cv2.boundingRect(cnt)[3] / cv2.boundingRect(cnt)[2] > min_aspect_ratio]
    
    chromosome_count = len(chromosomes)
    
    # Visualizar cromossomos detectados
    vis_image = image.copy()
    cv2.drawContours(vis_image, chromosomes, -1, (0, 255, 0), 2)
    cv2.imwrite('detected_chromosomes.png', vis_image)
    
    # Salvar imagens intermediárias
    cv2.imwrite('gray.png', gray)
    cv2.imwrite('binary.png', binary)
    cv2.imwrite('sure_fg.png', sure_fg)
    
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
    print("Visualization saved as 'detected_chromosomes.png'")
    print("Intermediate images saved as 'gray.png', 'binary.png', and 'sure_fg.png'")






