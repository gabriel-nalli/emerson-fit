# Tratamento local — 9 de setembro de 2026

Aplicado: p3 (duplo bíceps) nos dois topos; p2 (três quartos) nas duas artes Sobre.
Processamento exclusivamente com Pillow e numpy; nenhuma geração, reconstrução
de rosto/corpo, alteração de tatuagens ou mudança de proporções.

## Alterações

- Máscara com contração subpixel e redução do excesso luminoso junto à borda,
  estimado pela direção interior da máscara. A amostra interior só estabelece
  um limite de luminância: não é copiada para a borda. Correção suavizada como
  mapa de exposição, preservando a cor original e protegendo a região facial.
- Removidos flat-field/deband do tratamento. Ajuste moderado de exposição,
  redução do verde, cor ligeiramente mais quente e redução suave do ruído de cor.
- Ampliação com alfa pré-multiplicado e nitidez em luminância, limitada a 5 níveis
  por pixel e aos extremos locais, excluindo o contorno semitransparente.
- Fundo escuro baseado na arte de academia já existente neste projeto.
- Topo desktop centrado em 70%, Sobre desktop em 30%. Topo mobile com espaço
  sob a prova social e enquadramento cabeça–cintura. Sobre mobile com cabeça
  a 159 px (16% de 992 px) na arte e retrato centrado.

## Limitações

p1 foi inspecionada, mas não usada nem alterada. A emenda diagonal atravessa
camiseta e calça; não obtive uma solução confiável para eliminá-la preservando
os detalhes. Não repeti deband, flat-field ou preenchimento borrado da borda.
Parte da luz lateral real permanece no rosto, deliberadamente protegida.
A resolução/compressão do WhatsApp ainda limita o detalhe; a nitidez não inventa
informação ausente nem equivale a uma nova fotografia em alta resolução.

## Arquivos escritos

Substituídos em `public/wp-content/uploads/2024/11/`:

- `ng-car12ol1.webp` — 1920×878
- `ng-carol1-mi12ble.webp` — 800×1884
- `bg-biocarol13.jpg` — 1920×992 (JPEG 97, sem subamostragem de cor)
- `bg-biocarol-mobile-1-1.webp` — 800×992

Auxiliares em `_brief-imagens/`:

- `tratar-local.py`: pipeline reproduzível. Sem argumentos gera candidatos;
  `--aplicar` substitui as quatro saídas. Backup criado somente se ausente.
- `verificar-render.mjs`: Chrome local/CDP para screenshots do site real.
- `RESULTADO.md`: este relatório.
- `verificacao/backup/`: cópias dos quatro arquivos antes do tratamento.
- `verificacao/candidatos/`: quatro cópias do resultado final.
- `verificacao/p2-tratado.png`, `p3-tratado.png`: recortes tratados com alfa.
- `verificacao/comparacao.jpg`: comparação das quatro artes, antes/depois.
- `verificacao/topo-desktop.png`, `topo-mobile.png`, `sobre-desktop.png`,
  `sobre-mobile.png`: screenshots finais inspecionados visualmente.
- `verificacao/render.json`: dimensões dos elementos, URLs, HTTP e erros JS.
- Outras prévias de inspeção em `verificacao/`: entradas, fundo, antes, depois,
  topo-antes e detalhes intermediários; não são usadas pelo site.

## Verificação

Chrome headless local em `http://localhost:5175/`, usando o servidor Emerson já
ativo: desktop 1440×900 e mobile 430×932. Screenshots das quatro seções abertos
e inspecionados após a última alteração. Quatro imagens retornaram HTTP 200,
sem exceções JS capturadas, largura do documento igual à viewport. Dimensões e
decodificação dos quatro arquivos validadas por Pillow.

HTML/CSS e arquivos originais de entrada não foram alterados. Nenhum arquivo
do projeto `carol-santos-personal` foi aberto ou modificado nesta tarefa.
