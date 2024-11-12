# Karyotype Analyzer

Este é um aplicativo simples para Windows que analisa cariótipos através de imagens inseridas em qualquer formato comum (PNG, JPG, BMP).

## Funcionalidades

- Carrega imagens de cariótipos
- Analisa a imagem para detectar e contar cromossomos
- Fornece uma saída científica básica sobre o cariótipo

## Requisitos

- Python 3.7+
- OpenCV
- NumPy
- PyQt5

## Instalação

1. Clone este repositório:
   ```
   git clone https://github.com/ezrafchev/karyotype-analyzer.git
   cd karyotype-analyzer
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install opencv-python numpy PyQt5
   ```

## Uso

1. Execute o aplicativo:
   ```
   python karyotype_analyzer.py
   ```

2. Na interface gráfica:
   - Clique em "Load Image" para carregar uma imagem de cariótipo
   - Clique em "Analyze Karyotype" para processar a imagem e obter resultados

3. Os resultados serão exibidos na interface, incluindo:
   - Número de cromossomos detectados
   - Interpretação básica do cariótipo

## Limitações

- Este é um aplicativo básico e pode não ser preciso para uso clínico ou profissional
- A detecção de cromossomos depende da qualidade da imagem e do contraste
- Não distingue entre diferentes tipos de cromossomos ou anomalias específicas

## Contribuições

Contribuições são bem-vindas! Por favor, abra uma issue para discutir mudanças importantes antes de fazer um pull request.

## Licença

Este projeto está licenciado sob a MIT License.
