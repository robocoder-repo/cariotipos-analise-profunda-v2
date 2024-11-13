# Analisador de Cariótipo

Este projeto é um analisador de cariótipo automatizado desenvolvido em Python. Ele utiliza técnicas de processamento de imagem e visão computacional para detectar, contar e analisar cromossomos em imagens de cariótipos.

## Funcionalidades

- Detecção automática de cromossomos em imagens de cariótipos
- Contagem precisa do número de cromossomos
- Análise detalhada de cada cromossomo, incluindo:
  - Área
  - Perímetro
  - Razão de aspecto
  - Índice centromérico
  - Classificação (Telocêntrico, Acrocêntrico, Submetacêntrico, Metacêntrico)
- Análise estatística dos cromossomos detectados
- Identificação de possíveis anomalias cromossômicas
- Visualização dos cromossomos detectados

## Requisitos

- Python 3.7+
- OpenCV
- NumPy
- SciPy

## Instalação

1. Clone este repositório:
   ```
   git clone https://github.com/ezrafchev/analisador-cariotipo.git
   cd analisador-cariotipo
   ```

2. Instale as dependências:
   ```
   pip install opencv-python numpy scipy
   ```

## Uso

Execute o script principal fornecendo o caminho para a imagem do cariótipo:

```
python karyotype_analyzer.py caminho/para/sua/imagem.png
```

O script irá analisar a imagem e fornecer um relatório detalhado sobre os cromossomos detectados. Além disso, ele salvará uma imagem com os cromossomos detectados e numerados como 'detected_chromosomes.png'.

## Saída

O script fornece as seguintes informações:

1. Número total de cromossomos detectados
2. Possível interpretação do número de cromossomos (normal, deleção, duplicação)
3. Detalhes de cada cromossomo detectado
4. Análise estatística dos cromossomos
5. Identificação de cromossomos potencialmente anormais

## Limitações

- O desempenho do analisador pode variar dependendo da qualidade da imagem de entrada
- A precisão da detecção e classificação dos cromossomos pode ser afetada por sobreposições ou distorções na imagem

## Contribuições

Contribuições para melhorar este projeto são bem-vindas. Por favor, sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
