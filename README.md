# Emerson Consultoria Fit

Landing page de consultoria online do personal trainer Emerson Ferreira (Campinas-SP).
Site estático em HTML/CSS/JS servido por Vite.

- `index.html` — página única com todas as seções
- `public/wp-content/...` — CSS, JS, fontes e imagens
- `forms/gerar-formulario.gs` — script do Google Apps que gera o formulário de briefing do cliente
- `_brief-imagens/` — materiais e scripts reproduzíveis do tratamento das imagens
  - `hero-bg/` — recorte e integração das artes do topo e da seção Sobre
  - `antes-depois/` — montagem das artes de antes e depois
  - `mockup/` — composição das fotos nas telas dos celulares

## Rodando

```
npm install
npm run dev     # servidor local
npm run build   # gera dist/ para deploy estático
```

## Conteúdo

Textos, planos, depoimentos e FAQ vêm do formulário de briefing respondido pelo cliente.
