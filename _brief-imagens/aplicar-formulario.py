import re, html, urllib.parse
p='index.html'; s=open(p,encoding='utf-8').read()
WA='https://wa.me/5519993919090'
def wa(msg): return WA+'?text='+urllib.parse.quote(msg)
def rep(old,new,count=1,flags=0,regex=False):
    global s
    if regex: old=old.replace(' ','[ \xa0]')
    if not regex:
        old=re.escape(old).replace('\\ ','[ \xa0]'); new=new.replace('\\','\\\\')
    n=len(re.findall(old,s,flags))
    assert n==count, f'esperado {count}, achei {n}: {old[:70]!r}'
    s=re.sub(old,new,s,flags=flags)

# ---------- head ----------
rep('<title>Consultoria Emerson Fit','<title>Emerson Consultoria Fit | Consultoria Online de Treino | Campinas-SP')

# ---------- hero ----------
rep('1 ANO DE RESULTADOS EM 12 SEMANAS','A ENGENHARIA DO TREINO IDEAL, DESENHADA PARA A SUA ROTINA.')
rep('Transforme sua vida com treinos personalizados! O plano certo para você atingir seus objetivos de maneira eficiente. Com a consultoria online, você tem a flexibilidade de treinar onde e quando quiser, com treinos criados especialmente para suas necessidades e com um personal à sua disposição, garantindo o suporte que você precisar.',
    'Conquiste o corpo dos seus sonhos com um plano feito exclusivamente para você. Treino 100% individualizado, correção da execução por vídeo e suporte direto no WhatsApp: em casa ou na academia, em 30 minutos ou 1 hora por dia, com um programa sustentável que encaixa na sua rotina sem fazer você desistir no primeiro mês.')
rep('+20 ALUNOS QUE TIVERAM SUA TRANSFORMAÇÃO','+100 ALUNOS QUE TIVERAM SUA TRANSFORMAÇÃO')
rep('EMERSON FIT | CONSULTORIA ON-LINE | ','EMERSON CONSULTORIA FIT | CONSULTORIA ON-LINE | CAMPINAS-SP | ',count=16)

# ---------- benefícios ----------
rep(r'Plataforma de treinos(\s*)</span></h3><p class="elementor-icon-box-description">\s*Uma plataforma de treinos\s*online exclusiva, onde todos os\s*exercícios têm vídeos\s*explicativos. Além disso, você\s*pode treinar onde preferir, em\s*casa ou na academia\.</p>',
    r'Flexibilidade para a sua rotina\1</span></h3><p class="elementor-icon-box-description">\nO treino se adapta à sua vida, não o contrário. Seja para treinar 30 minutos ou 1 hora por dia, em casa ou na academia, o programa é sustentável e encaixa no seu dia a dia sem fazer você desistir no primeiro mês.</p>',regex=True)
rep(r'Treino Personalizados(\s*)</span></h3><p class="elementor-icon-box-description">\s*Treinos montados de acordo\s*com as suas restrição e\s*dificuldades, reduzindo riscos\s*de lesões e aumentando a\s*perfomance do seu treino\.</p>',
    r'Treino 100% individualizado\1</span></h3><p class="elementor-icon-box-description">\nAnamnese estratégica do seu histórico, rotina e objetivos. Treino desenhado para a sua realidade, com correção dos padrões de movimento para você evoluir sem dores articulares e sem risco desnecessário de lesão.</p>',regex=True)
rep(r'Suporte Exclusivo(\s*)</span></h3><p class="elementor-icon-box-description">\s*Preço acessível, suporte e feedback constante, sempre disponível para esclarecer dúvidas e ajustar o plano conforme a sua evolução\.</p>',
    r'Suporte direto no WhatsApp\1</span></h3><p class="elementor-icon-box-description">\nAnálise e correção da execução dos exercícios por vídeo, feedbacks periódicos e ajustes de carga conforme a sua evolução. Suporte de segunda a sexta, direto comigo.</p>',regex=True)

# ---------- antes e depois: 2 imagens -> 5 ----------
a=s.find('<div class="elementor-element elementor-element-5186a298'); b=s.find('<div class="elementor-element elementor-element-6ef3ae6b'); 
# fim do segundo widget: fecha após </img></div></div>
assert a>0 and b>a
b_end=s.find('</div></div>',s.find('asgasgasg.webp',b))+len('</div></div>')
def widget(n,w,h,alt):
    return ('<div class="elementor-element elementor-element-5186a298 ad-item elementor-widget__width-initial elementor-widget-mobile__width-inherit elementor-widget-tablet__width-inherit elementor-invisible elementor-widget elementor-widget-image" data-id="5186a298" data-element_type="widget" data-settings="{&quot;_animation&quot;:&quot;fadeInUp&quot;}" data-widget_type="image.default"><div class="elementor-widget-container">\n'
            f'<img loading="lazy" decoding="async" width="{w}" height="{h}" src="/wp-content/uploads/2024/11/antes-depois-{n}.webp" class="attachment-full size-full" alt="{alt}" /></div></div>')
legenda='<div class="elementor-element ad-legenda elementor-widget elementor-widget-text-editor" data-element_type="widget" data-widget_type="text-editor.default"><div class="elementor-widget-container"><p>Em apenas 1 mês e 10 dias, saímos de 61,70 kg para 64,55 kg: um ganho líquido de +2,85 kg de massa com extrema qualidade. Metodologia EF: resultados comprovados e medíveis.</p></div></div>'
novo=legenda+widget(1,1000,1000,'Antes e depois: de 61,70 kg para 64,55 kg em 40 dias')+widget(2,896,1195,'Antes e depois de aluna da Consultoria EF')+widget(3,896,1195,'Antes e depois de aluna da Consultoria EF')+widget(4,896,1195,'Antes e depois de aluna da Consultoria EF')+widget(5,896,1195,'Antes e depois de aluna da Consultoria EF')
s=s[:a]+novo+s[b_end:]

# ---------- depoimentos ----------
rep(r'Gustavo<br>Aluno de Personal Presencial(\s*)</span></h3><p class="elementor-icon-box-description">\s*“Através dos seus treinos,.*?melhorar no corpo\.”</p>',
    r'Aluno da Consultoria EF<br>Consultoria Online · 40 dias\1</span></h3><p class="elementor-icon-box-description">\n“Confesso que no começo eu achava que ia demorar meses e meses pra ver alguma diferença expressiva. Mas em apenas 1 mês e 10 dias na Consultoria EF, o resultado veio muito além do que eu esperava!”</p>',regex=True,flags=re.S)
rep(r'Lauany<br>Aluna de Consultoria Online(\s*)</span></h3><p class="elementor-icon-box-description">\s*“Depois que comecei.*?meu processo\.”</p>',
    r'Laís<br>Aluna da Consultoria EF\1</span></h3><p class="elementor-icon-box-description">\n“Quero agradecer você Emerson, por toda dedicação e parceria durante essa caminhada. Hoje me sinto muito mais forte, disposta e com um condicionamento físico que nunca imaginei ter. Obrigada por cada treino, cada incentivo e por não deixar eu desistir nos dias difíceis. Sua dedicação e profissionalismo fazem toda diferença na minha evolução!”</p>',regex=True,flags=re.S)
rep(r'Pamela<br>Aluna de Consultoria Online(\s*)</span></h3><p class="elementor-icon-box-description">\s*“Gosto muito da atenção dada.*?Emerson’’</p>',
    r'Verônica<br>Aluna da Consultoria EF\1</span></h3><p class="elementor-icon-box-description">\n“Minha experiência com o personal Emerson tem sido excelente! Tive uma evolução incrível, com treinos muito bem elaborados e adequados para mim. Ele está sempre à disposição para tirar dúvidas, é muito atencioso, paciente e me motiva a cada etapa. Um excelente profissional, que faz toda a diferença nesse processo!”</p>',regex=True,flags=re.S)

# ---------- planos ----------
rep('de <s>R$399,00</s> por:','Adesão e Transição · 30 dias')
rep(' R$230,00</h2>',' R$100,00</h2>')
rep('de <s>R$870,00</s> por:','Desenvolvimento e Performance · 90 dias')
rep('>R$600,00</h2>','>R$280,00</h2>')
rep('R$200,00 POR MÊS','R$93,33 POR MÊS · MAIS RECOMENDADO')
rep('de <s>R$1420,00</s> por:','Alta Performance e Transformação · 180 dias')
rep('>R$900,00</h2>','>R$400,00</h2>')
rep('R$150,00 POR MÊS','R$66,67 POR MÊS')
# botões dos planos -> WhatsApp com mensagem
planos=[('365b0910','Plano Mensal (R$ 100,00)'),('523b1f35','Plano Trimestral (R$ 280,00)'),('3d502196','Plano Semestral (R$ 400,00)')]
for wid,nome in planos:
    i=s.find(f'data-id="{wid}"'); j=s.find('href="#"',i); assert 0<j-i<600, wid
    s=s[:j]+f'href="{wa("Olá Emerson! Quero começar a consultoria online no "+nome+". Como faço para iniciar a anamnese?")}" target="_blank" rel="noopener"'+s[j+len('href="#"'):]
# incluso em cada plano: inserir lista abaixo do preço (antes do botão)
inclusos={'365b0910':['Anamnese estratégica (histórico, rotina e objetivos)','Treino 100% individualizado para a sua realidade','Correção da execução dos exercícios por vídeo','Suporte direto via WhatsApp de segunda a sexta'],
          '523b1f35':['Todos os benefícios do Plano Mensal','Treino renovado e reestruturado a cada 30 a 45 dias','Acompanhamento contínuo de evolução (fotos e métricas)','Ajustes dinâmicos conforme sua evolução física'],
          '3d502196':['Todos os benefícios do Plano Trimestral','Periodização completa em fases (força, hipertrofia e deload)','Suporte e acompanhamento contínuo prioritário','Máximo rendimento sem interrupções na sua evolução']}
for wid,itens in inclusos.items():
    i=s.find(f'<div class="elementor-element elementor-element-{wid}')
    lista='<div class="elementor-element plano-inclusos elementor-widget"><ul>'+''.join(f'<li>{x}</li>' for x in itens)+'</ul></div>'
    s=s[:i]+lista+s[i:]

# ---------- sobre ----------
rep('<h3 class="elementor-image-box-title">EMERSON FIT</h3>','<h3 class="elementor-image-box-title">EMERSON FERREIRA</h3>')
a=s.find('<p class="elementor-image-box-description">Olá! Sou Emerson'); assert a>0; b=s.find('</p>',a)
sobre=('<p class="elementor-image-box-description">Olá. Me chamo Emerson Ferreira e atuo no direcionamento de estratégias de treinamento físico de alta precisão. Atendo em Campinas-SP e online para todo o Brasil.'
 '<br><br>Minha atuação combina fundamentação teórica em biomecânica com quase 10 anos de experiência prática diária no acompanhamento do treinamento de força. O objetivo do meu trabalho é mapear suas necessidades individuais, corrigir padrões de movimento e estruturar um planejamento eficiente para que você alcance seus objetivos com a máxima segurança e clareza metodológica.'
 '<br><br>O que eu entrego para você:<br>'
 '• <b>Segurança e longevidade:</b> um treino desenhado para você evoluir sem dores articulares ou riscos desnecessários de lesão.<br>'
 '• <b>Clareza e direcionamento:</b> saber exatamente o porquê de cada exercício, série e repetição no seu planejamento.<br>'
 '• <b>Acolhimento da sua realidade:</b> uma rotina realista, adaptada ao seu trabalho, viagens e disponibilidade de tempo.<br>'
 '• <b>Evolução estética real:</b> desenvolvimento muscular e definição moldados pela correta aplicação de força no músculo-alvo.<br>'
 '• <b>Consciência corporal e autonomia:</b> aprendizado definitivo sobre como executar movimentos de forma eficiente para o resto da vida.<br>'
 '• <b>Consistência sem sofrimento:</b> a construção de uma rotina sustentável que se encaixa no seu dia a dia a longo prazo.')
s=s[:a]+sobre+s[b:]

# ---------- contato ----------
rep('href="#" tabindex="-1"><img loading="lazy" decoding="async" width="512" height="512" src="/wp-content/uploads/2024/11/9d30c130.svg"',
    f'href="{wa("Olá Emerson! Vim pelo site e quero saber mais sobre a consultoria.")}" target="_blank" rel="noopener" tabindex="-1"><img loading="lazy" decoding="async" width="512" height="512" src="/wp-content/uploads/2024/11/9d30c130.svg"')
rep('<h3 class="elementor-image-box-title"><a href="#">Atendimento por Whatsapp</a></h3>',
    f'<h3 class="elementor-image-box-title"><a href="{wa("Olá Emerson! Vim pelo site e quero saber mais sobre a consultoria.")}" target="_blank" rel="noopener">Atendimento por WhatsApp</a></h3>')
rep('Atendiomento por E-mail','Atendimento por E-mail')
rep('mailto:SEU_EMAIL','mailto:emersonheloisa90@gmail.com',count=2)
rep('Envie um e-mail para SEU_EMAIL','Envie um e-mail para emersonheloisa90@gmail.com')
rep('Confiras as dúvidas mais frequentes de meus alunos','Confira as dúvidas mais frequentes dos meus alunos')

# ---------- FAQ ----------
faq=[('Interessado no acompanhamento presencial?','O acompanhamento presencial é focado na correção minuciosa da sua execução biomecânica, garantindo que você aplique a máxima intensidade nos treinos com total segurança e eficiência. As vagas são estritamente limitadas para garantir a qualidade e a atenção individualizada em cada sessão. Ao entrar em contato, você verifica as possibilidades e horários disponíveis para alinharmos a sua rotina.'),
 ('Nunca treinei (ou estou há muito tempo parado). O treino vai ser adaptado para o meu nível e rotina?','Com certeza! O treino é 100% individualizado. Na nossa anamnese, avalio seu histórico, limitações físicas, disponibilidade de dias e tempo e os equipamentos aos quais você tem acesso. O objetivo é criar uma rotina sustentável e segura que se encaixe na sua vida, e não o contrário.'),
 ('Como funciona o acompanhamento no dia a dia e o suporte para tirar dúvidas?','Você terá suporte direto comigo via WhatsApp para enviar vídeos executando os exercícios, tirar dúvidas de postura ou pedir adaptações. Além disso, faremos feedbacks periódicos para avaliar sua evolução, ajustar cargas e garantir que você continue progredindo com máxima segurança na execução.'),
 ('E se eu não tiver acesso a uma academia completa ou precisar treinar em casa?','Sem problemas! A consultoria adapta a montagem da ficha aos recursos que você tem disponíveis, seja em academia de bairro, condomínio, ao ar livre ou em casa com equipamentos básicos e peso do corpo. O segredo está na seleção estratégica dos exercícios e no controle de intensidade.'),
 ('Em quanto tempo começo a ver os primeiros resultados físicos e de desempenho?','Nas primeiras 2 a 3 semanas você já nota melhora significativa na disposição, na postura, na qualidade do sono e na execução dos movimentos. Mudanças estéticas consolidadas (perda de gordura e ganho de massa magra) ficam bem visíveis a partir de 6 a 8 semanas de consistência nos treinos e alinhamento da rotina.'),
 ('Se eu sentir dores ou desconforto em algum exercício, o treino pode ser alterado?','Com certeza. A prioridade absoluta é a sua saúde articular e o seu bem-estar. Se algum movimento causar desconforto ou dor atípica, faremos a substituição imediata do exercício ou o ajuste na biomecânica de execução para garantir um estímulo eficiente e sem risco.')]
a=s.find('<div class="elementor-toggle"><div class="elementor-toggle-item">'); assert a>0; k=s.find('nutricionista.'); assert k>0
b=s.find('</div></div></div>',k); assert b>0; b+=len('</div></div>')  # itens já fecham content+item
tmpl_start=s.find('<div class="elementor-toggle-item">',a); tmpl_end=s.find('<div class="elementor-toggle-item">',tmpl_start+10)
tmpl=s[tmpl_start:tmpl_end]  # primeiro item completo
items=''
for i,(q,r) in enumerate(faq,1):
    t=tmpl.replace('1141',f'11{40+i}').replace('data-tab="1"',f'data-tab="{i}"')
    t=re.sub(r'(<a class="elementor-toggle-title" tabindex="0">).*?(</a>)',lambda m:m.group(1)+q+m.group(2),t,flags=re.S)
    t=re.sub(r'(<div id="elementor-tab-content-\d+"[^>]*>).*?(</div></div>)$',lambda m:m.group(1)+'<p>'+r+'</p>'+m.group(2),t,flags=re.S)
    items+=t
s=s[:a]+'<div class="elementor-toggle">'+items+s[b:]

# ---------- loja (cliente não tem): remover container 2d7654f3 ----------
a=s.find('<div class="elementor-element elementor-element-2d7654f3'); assert a>0
depth=0; i=a
while True:
    m=re.compile(r'<div\b|</div>').search(s,i); tok=m.group(0); i=m.end()
    depth+= 1 if tok=='<div' else -1
    if depth==0: break
s=s[:a]+s[i:]
assert 'CONFIRA NOSSA MARCA' not in s

# ---------- rodapé ----------
rep('Transforme sua vida com treinos personalizados! Escolha entre consultoria online para flexibilidade total ou personal presencial para um acompanhamento ainda mais próximo. O plano certo para você atingir seus objetivos de maneira eficiente.',
    'Transformando vidas através do movimento, com treinos personalizados e foco na sua melhor versão. Consultoria online para todo o Brasil e acompanhamento presencial em Campinas-SP.')
rep('SEU_WHATSAPP','(19) 99391-9090')
rep('SEU_EMAIL','emersonheloisa90@gmail.com')
rep('href="SEU_INSTAGRAM"','href="https://www.instagram.com/emersonferreira.fit" target="_blank" rel="noopener"')
rep('Consultoria Emerson Fit | Todos os direitos reservados 2026 ©','Emerson Consultoria Fit | CREF em atualização | Todos os direitos reservados 2026 ©')

# ---------- CSS extra ----------
css='''<style id="emerson-form-overrides">
.elementor-element-13db0c38 .ad-legenda{width:100%;max-width:760px;text-align:center;color:#fff;font-family:"Exo",sans-serif;font-size:1.05em;line-height:1.5;margin:0 auto 1.5em}
.elementor-element-13db0c38 .ad-legenda p{margin:0}
.elementor-element-13db0c38 .ad-item{width:30%;max-width:30%;--container-widget-width:30%;margin:0.5em}
.elementor-element-13db0c38 .ad-item img{width:100%;height:auto}
@media (max-width:1024px){.elementor-element-13db0c38 .ad-item{width:46%;max-width:46%}}
@media (max-width:767px){.elementor-element-13db0c38 .ad-item{width:100%;max-width:100%;margin:0.5em 0}}
.plano-inclusos{width:100%;margin:0.75em 0 1.25em}
.plano-inclusos ul{list-style:none;margin:0;padding:0;text-align:left}
.plano-inclusos li{color:#fff;font-family:"Exo",sans-serif;font-size:0.95em;line-height:1.35;padding:0.3em 0 0.3em 1.4em;position:relative}
.plano-inclusos li::before{content:"✓";color:#cefb69;position:absolute;left:0;font-weight:700}
</style>
</head>'''
s=s.replace('</head>',css,1)
open(p,'w',encoding='utf-8').write(s)
print('ok', len(s))
