# Brief — tratamento das fotos do Emerson

Objetivo: deixar as fotos com cara **profissional** para a landing page
`~/Projects/emerson-fit` (export de Elementor, tema escuro, quase preto).

## Entradas

- `originais/` — 5 fotos JPEG cruas do WhatsApp (960–989 × 1280).
  `foto4-costas-ESPELHADA.jpeg` está espelhada (a tatuagem "Helena" aparece invertida).
  As outras NÃO estão espelhadas (o "GROWTH" da camiseta lê corretamente).
- `recortes/` — mesmas fotos já com fundo removido (PNG com alfa), geradas por
  `cutout.swift` usando `VNGenerateForegroundInstanceMaskRequest` (Vision, macOS).
  Mapeamento: p1=foto1 (em pé), p2 e p5=foto2 (são idênticas), p3=foto3, p4=foto4.
- `pipeline-atual.py` — o tratamento que está em uso hoje.

## Saídas exigidas (substituir no lugar, mesmos nomes)

Diretório: `~/Projects/emerson-fit/public/wp-content/uploads/2024/11/`

| Arquivo | Tamanho | Uso | Composição |
|---|---|---|---|
| `ng-car12ol1.webp` | 1920×878 | topo desktop | pessoa à **direita** (centro ≈70% da largura), texto à esquerda |
| `ng-carol1-mi12ble.webp` | 800×1884 | topo mobile | tronco (cabeça→cintura), grande, encostado embaixo |
| `bg-biocarol13.jpg` | 1920×992 | "Sobre" desktop | pessoa à **esquerda** (centro ≈30%), texto à direita |
| `bg-biocarol-mobile-1-1.webp` | 800×992 | "Sobre" mobile | retrato centrado, topo da cabeça ≈16% da altura |

Os nomes são os da Carol de propósito: o CSS já aponta para eles, não renomeie.
Referência de enquadramento: os arquivos originais em
`~/Projects/carol-santos-personal/public/wp-content/uploads/2024/11/`.

## O que precisa melhorar

1. **Fundo invisível** — o recorte tem que sumir no preto do site. Hoje sobra um
   halo claro em volta do ombro/braço. Erodir a máscara não resolveu bem;
   é preciso descontaminar a cor da borda (o fundo bege da academia sangra no
   contorno) antes de compor.
2. **Iluminação** — a foto original é de espelho de academia, luz amarelo-esverdeada
   e irregular. Em `foto1-em-pe` há uma **faixa diagonal de reflexo** atravessando o
   torso. O `deband()` atual (normalização da média por coluna) só ataca variação
   vertical, então a faixa diagonal permanece parcialmente.
3. **Cor da pele** — está puxando para o acinzentado/esverdeado. Precisa de tom
   natural e quente, sem estourar.
4. **Nitidez/ruído** — as fotos têm 1280px de altura e vão para 1920. Ampliação
   simples (LANCZOS) amolece. Precisa de sharpening melhor e controle de ruído.

## Restrições

- **Não alterar as feições dele.** É o site oficial de um cliente real — retoque de
  luz/cor sim, geração ou substituição de rosto/corpo não.
- Manter o visual do site: fundo quase preto, figura destacada, contraste alto.
- Só ferramentas locais: PIL 12.2 + numpy 2.4 + Swift/Vision. **Não há ImageMagick
  nem rembg instalados.**
- Trabalhar apenas dentro de `~/Projects/emerson-fit`. Não tocar em
  `~/Projects/carol-santos-personal` (é outro site, está no ar).

## Como verificar

```bash
cd ~/Projects/emerson-fit && npm run dev     # sobe o vite
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
  --disable-gpu --hide-scrollbars --virtual-time-budget=10000 \
  --window-size=1440,900 --screenshot=/tmp/top.png http://localhost:5175/
```

Olhe o screenshot antes de dar por pronto. Ao terminar, reporte com
`maestri ask "Claude Code #3" "<o que mudou e o que não deu>"`.
