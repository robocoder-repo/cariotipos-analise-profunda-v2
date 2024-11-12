# Karyotype Analyzer

Este é um aplicativo simples para Windows que analisa cariótipos através de imagens inseridas em qualquer formato comum (PNG, JPG, BMP).

## Funcionalidades

- Carrega imagens de cariótipos
- Processa a imagem para detectar cromossomos
- Conta o número de cromossomos detectados
- Fornece uma saída básica sobre o cariótipo
- Gera imagens intermediárias para visualização do processo

## Requisitos

- Python 3.7+
- OpenCV
- NumPy

## Instalação

1. Clone este repositório:
   ```
   git clone https://github.com/ezrafchev/karyotype-analyzer.git
   cd karyotype-analyzer
   ```

2. Instale as dependências:
   ```
   pip install opencv-python numpy
   ```

## Uso

1. Execute o aplicativo:
   ```
   python karyotype_analyzer.py <caminho_da_imagem>
   ```

2. O script irá processar a imagem e fornecer uma saída com o número de cromossomos detectados.

3. Imagens intermediárias e o resultado final serão salvos no diretório atual.

## Limitações

- Este é um aplicativo básico e pode não ser preciso para uso clínico ou profissional.
- A detecção de cromossomos depende muito da qualidade da imagem de entrada e do contraste entre os cromossomos e o fundo.
- O aplicativo não distingue entre diferentes tipos de cromossomos ou anomalias específicas.
- A contagem atual pode não ser precisa para todos os tipos de imagens de cariótipo.

## Possíveis Melhorias Futuras

1. Implementar técnicas mais avançadas de processamento de imagem para melhorar a detecção de cromossomos.
2. Adicionar capacidade de distinguir entre diferentes tipos de cromossomos.
3. Implementar uma interface gráfica para facilitar o uso.
4. Adicionar capacidade de detectar anomalias cromossômicas específicas.
5. Melhorar a robustez do algoritmo para lidar com diferentes qualidades de imagem e preparações de cariótipo.
6. Implementar testes unitários e de integração para garantir a confiabilidade do código.

## Contribuições

Contribuições são bem-vindas! Por favor, abra uma issue para discutir mudanças importantes antes de fazer um pull request.

## Licença

Este projeto está licenciado sob a MIT License.
