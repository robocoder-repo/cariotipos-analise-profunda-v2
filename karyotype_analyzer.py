import cv2
import numpy as np
import sys
from scipy import stats
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from jcvi.graphics.karyotype import Karyotype
from wgdi.ks import calculate_ks

def generate_sequence(chromosome_details):
    sequences = []
    for chrom in chromosome_details:
        seq_length = int(chrom['area'] / 10)  # Exemplo: usar área como base para o comprimento da sequência
        seq = Seq(''.join(np.random.choice(['A', 'T', 'C', 'G'], size=seq_length)))
        record = SeqRecord(seq, id=f"chromosome_{chrom['number']}", description=f"Classification: {chrom['classification']}")
        sequences.append(record)
    return sequences

def visualize_karyotype(chromosome_details):
    k = Karyotype()
    for chrom in chromosome_details:
        k.add_chromosome(f"chr{chrom['number']}", chrom['area'] / 1000)  # Usar área como tamanho do cromossomo
    k.draw()
    k.savefig("karyotype_visualization.png")

def calculate_ks_values(sequences):
    ks_values = calculate_ks(sequences)
    return ks_values

def generate_pdf_report(chromosome_details, ks_values):
    doc = SimpleDocTemplate("karyotype_report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Relatório de Análise de Cariótipo", styles['Title']))
    
    # Tabela de detalhes dos cromossomos
    data = [['Número', 'Área', 'Perímetro', 'Razão de Aspecto', 'Índice Centromérico', 'Classificação']]
    for chrom in chromosome_details:
        data.append([chrom['number'], f"{chrom['area']:.2f}", f"{chrom['perimeter']:.2f}", 
                     f"{chrom['aspect_ratio']:.2f}", f"{chrom['centromeric_index']:.2f}", chrom['classification']])
    
    t = Table(data)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                           ('FONTSIZE', (0, 0), (-1, 0), 14),
                           ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                           ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                           ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                           ('FONTSIZE', (0, 1), (-1, -1), 12),
                           ('TOPPADDING', (0, 1), (-1, -1), 6),
                           ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    content.append(t)

    content.append(Paragraph("Valores Ks", styles['Heading2']))
    ks_data = [['Par de Cromossomos', 'Valor Ks']]
    for pair, value in ks_values.items():
        ks_data.append([f"{pair[0]} - {pair[1]}", f"{value:.4f}"])
    
    ks_table = Table(ks_data)
    ks_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                  ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                  ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                  ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                  ('FONTSIZE', (0, 0), (-1, 0), 14),
                                  ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                  ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                  ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                                  ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                  ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                                  ('FONTSIZE', (0, 1), (-1, -1), 12),
                                  ('TOPPADDING', (0, 1), (-1, -1), 6),
                                  ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                                  ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    content.append(ks_table)

    doc.build(content)

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
    
    # Watershed para separar cromossomos unidos
    unknown = cv2.subtract(binary, sure_fg)
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(image, markers)
    
    # Encontrar contornos
    contours = []
    for label in np.unique(markers):
        if label == 0 or label == -1:
            continue
        mask = np.zeros(gray.shape, dtype="uint8")
        mask[markers == label] = 255
        cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours.extend(cnts)
    
    # Filtrar contornos
    min_area = 20
    max_area = 10000
    min_aspect_ratio = 1.02
    chromosomes = [cnt for cnt in contours if min_area < cv2.contourArea(cnt) < max_area]
    chromosomes = [cnt for cnt in chromosomes if cv2.boundingRect(cnt)[3] / cv2.boundingRect(cnt)[2] > min_aspect_ratio]
    
    chromosome_count = len(chromosomes)
    
    # Análise detalhada dos cromossomos
    chromosome_details = []
    for i, cnt in enumerate(chromosomes):
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = h / w
        
        # Calcular o índice centromérico
        mask = np.zeros(gray.shape, dtype="uint8")
        cv2.drawContours(mask, [cnt], -1, 255, -1)
        chromosome_image = cv2.bitwise_and(gray, gray, mask=mask)
        profile = np.sum(chromosome_image[y:y+h, x:x+w], axis=1)
        centromere_pos = np.argmin(profile)
        centromeric_index = centromere_pos / h
        
        # Classificar o cromossomo
        if centromeric_index <= 0.125:
            classification = "Telocêntrico"
        elif 0.125 < centromeric_index <= 0.25:
            classification = "Acrocêntrico"
        elif 0.25 < centromeric_index <= 0.375:
            classification = "Submetacêntrico"
        else:
            classification = "Metacêntrico"
        
        chromosome_details.append({
            'number': i+1,
            'area': area,
            'perimeter': perimeter,
            'aspect_ratio': aspect_ratio,
            'centromeric_index': centromeric_index,
            'classification': classification
        })
    
    # Visualizar cromossomos detectados
    vis_image = image.copy()
    for i, cnt in enumerate(chromosomes):
        cv2.drawContours(vis_image, [cnt], -1, (0, 255, 0), 2)
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.putText(vis_image, str(i+1), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.imwrite('detected_chromosomes.png', vis_image)

    # Gerar sequências
    sequences = generate_sequence(chromosome_details)

    # Visualizar cariótipo
    visualize_karyotype(chromosome_details)

    # Calcular valores Ks
    ks_values = calculate_ks_values(sequences)

    # Gerar relatório PDF
    generate_pdf_report(chromosome_details, ks_values)

    result = f"Número de cromossomos detectados: {chromosome_count}\n"
    result += f"Detalhes dos cromossomos salvos em 'karyotype_report.pdf'\n"
    result += f"Visualização do cariótipo salva em 'karyotype_visualization.png'"

    return result

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python karyotype_analyzer.py <caminho_da_imagem>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = analyze_karyotype(image_path)
    print(result)
    print("Visualização salva como 'detected_chromosomes.png'")
    print("Relatório detalhado salvo como 'karyotype_report.pdf'")
    print("Visualização do cariótipo salva como 'karyotype_visualization.png'")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python karyotype_analyzer.py <caminho_da_imagem>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = analyze_karyotype(image_path)
    print(result)
    print("Visualização salva como 'detected_chromosomes.png'")
