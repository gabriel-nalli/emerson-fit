/**
 * Gera o formulário "Briefing — Site de Personal Trainer".
 * Como usar:
 *   1. Abra https://script.google.com  ->  Novo projeto
 *   2. Apague o conteúdo e cole este arquivo inteiro
 *   3. Selecione a função "criarFormulario" e clique em Executar
 *   4. Autorize o acesso quando pedir
 *   5. Os links aparecem em "Registro de execução" (Ctrl+Enter)
 */

function criarFormulario() {
  var form = FormApp.create('Briefing — Site de Personal Trainer');

  form.setTitle('Briefing — Site de Personal Trainer');
  form.setDescription(
    'Preencha com as informações do seu trabalho para montarmos a sua página.\n\n' +
    'Leva cerca de 15 minutos. Você pode salvar e voltar depois.\n' +
    'Campos com * são obrigatórios. Se algum item não se aplica a você, escreva "não tenho".'
  );
  form.setProgressBar(true);
  form.setAllowResponseEdits(true);
  form.setCollectEmail(true);

  // ---------- helpers ----------
  function texto(titulo, ajuda, obrigatorio) {
    var i = form.addTextItem().setTitle(titulo);
    if (ajuda) i.setHelpText(ajuda);
    i.setRequired(!!obrigatorio);
    return i;
  }
  function paragrafo(titulo, ajuda, obrigatorio) {
    var i = form.addParagraphTextItem().setTitle(titulo);
    if (ajuda) i.setHelpText(ajuda);
    i.setRequired(!!obrigatorio);
    return i;
  }
  function secao(titulo, descricao) {
    form.addPageBreakItem().setTitle(titulo).setHelpText(descricao || '');
  }
  function foto(titulo, ajuda, obrigatorio) {
    try {
      var up = form.addFileUploadItem().setTitle(titulo);
      if (ajuda) up.setHelpText(ajuda);
      up.setRequired(!!obrigatorio);
      return up;
    } catch (e) {
      // Conta sem upload habilitado: pede link
      return texto(titulo, (ajuda ? ajuda + ' ' : '') +
        '(Cole aqui o link da foto no Google Drive/Dropbox com acesso liberado.)', obrigatorio);
    }
  }

  // ============ 1. DADOS BÁSICOS ============
  secao('1. Seus dados', 'Como você quer aparecer no site.');
  texto('Seu nome completo', 'Ex.: Caroline Santos', true);
  texto('Nome que deve aparecer no site (marca)', 'Ex.: Carol Santos — Personal', true);
  texto('Número do CREF', 'Ex.: 123456-G/SP', false);
  texto('Cidade e estado onde atende', 'Ex.: Campinas / SP', true);
  texto('@ do seu Instagram', 'Ex.: @usecarolsantos', true);
  texto('Link do seu Instagram', 'Cole o endereço completo do perfil', false);
  texto('WhatsApp para contato (com DDD)', 'Ex.: (19) 98431-9371 — é o número que vai receber os cliques dos botões', true);
  texto('E-mail de contato público', 'Ex.: contato@seudominio.com.br', true);
  texto('Já tem domínio (endereço do site)?', 'Ex.: seunome.com.br — se não tiver, escreva "não tenho"', false);

  // ============ 2. IDENTIDADE VISUAL ============
  secao('2. Identidade visual', 'Se não tiver algum destes itens, escreva "não tenho" — a gente resolve.');
  foto('Sua logo', 'De preferência em PNG com fundo transparente', false);
  texto('Cor principal da marca', 'Código hexadecimal (ex.: #E91E63) ou só descreva: "rosa", "verde escuro"...', false);
  texto('Cor secundária / de destaque', 'Usada nos botões. Opcional.', false);
  paragrafo('Sites ou perfis que você gosta como referência',
    'Cole 1 a 3 links de páginas com o visual que te agrada e diga o que gostou em cada uma.', false);

  // ============ 3. TOPO DA PÁGINA ============
  secao('3. Topo da página (primeira dobra)',
    'É a primeira coisa que a pessoa vê ao abrir o site.');
  texto('Frase de impacto principal (headline)',
    'Curta e forte. Ex.: "1 ano de resultados em 12 semanas"', true);
  paragrafo('Texto de apoio abaixo da frase principal',
    'De 2 a 4 linhas explicando o que você oferece. Ex.: "Transforme sua vida com treinos personalizados..."', true);
  texto('Número de alunos atendidos / prova social',
    'Ex.: "+300 alunos que tiveram sua transformação". Se preferir não usar número, escreva outra frase de credibilidade.', false);
  texto('Texto do botão principal', 'Ex.: "Ver planos", "Quero começar"', true);
  foto('Sua foto para o topo do site',
    'Foto de corpo inteiro ou meio corpo, boa iluminação, de preferência com fundo limpo. Horizontal ou vertical, alta resolução.', true);
  foto('Uma segunda foto sua (versão celular)',
    'Opcional. Uma foto mais vertical/fechada funciona melhor no celular.', false);

  // ============ 4. BENEFÍCIOS ============
  secao('4. Benefícios da sua consultoria',
    'Três motivos para a pessoa fechar com você. Título curto + explicação de 2 a 4 linhas.');
  texto('Benefício 1 — título', 'Ex.: "Plataforma de treinos"', true);
  paragrafo('Benefício 1 — descrição', '', true);
  texto('Benefício 2 — título', 'Ex.: "Treinos personalizados"', true);
  paragrafo('Benefício 2 — descrição', '', true);
  texto('Benefício 3 — título', 'Ex.: "Suporte exclusivo"', true);
  paragrafo('Benefício 3 — descrição', '', true);

  // ============ 5. ANTES E DEPOIS ============
  secao('5. Antes e depois',
    'Resultados de alunos. IMPORTANTE: só envie fotos que o aluno autorizou você a publicar.');
  var temAD = form.addMultipleChoiceItem();
  temAD.setTitle('Você quer ter a seção "Antes e depois" no site?')
       .setChoiceValues(['Sim, tenho fotos autorizadas', 'Sim, mas ainda vou conseguir as fotos', 'Não quero essa seção'])
       .setRequired(true);
  foto('Fotos de antes e depois', 'Pode enviar várias. Se puder, já envie as duas fotos do mesmo aluno lado a lado.', false);
  paragrafo('Legenda de cada resultado (opcional)',
    'Ex.: "Marina — 8 meses de consultoria online". Uma por linha.', false);

  // ============ 6. DEPOIMENTOS ============
  secao('6. Depoimentos de alunos', 'Três depoimentos deixam a página bem mais convincente.');
  texto('Depoimento 1 — nome do aluno', '', true);
  texto('Depoimento 1 — tipo de acompanhamento', 'Ex.: "Aluno de personal presencial" ou "Aluna de consultoria online"', false);
  paragrafo('Depoimento 1 — o que ele(a) escreveu', 'Pode copiar e colar do WhatsApp/Instagram.', true);
  foto('Depoimento 1 — foto do aluno', 'Opcional', false);
  texto('Depoimento 2 — nome do aluno', '', false);
  texto('Depoimento 2 — tipo de acompanhamento', '', false);
  paragrafo('Depoimento 2 — o que ele(a) escreveu', '', false);
  foto('Depoimento 2 — foto do aluno', 'Opcional', false);
  texto('Depoimento 3 — nome do aluno', '', false);
  texto('Depoimento 3 — tipo de acompanhamento', '', false);
  paragrafo('Depoimento 3 — o que ele(a) escreveu', '', false);
  foto('Depoimento 3 — foto do aluno', 'Opcional', false);

  // ============ 7. PLANOS ============
  secao('7. Seus planos e preços',
    'A página tem espaço para até 3 planos. Preencha os que você usa.');
  texto('Plano 1 — nome', 'Ex.: "Mensal"', true);
  texto('Plano 1 — preço cheio ("de")', 'Ex.: R$ 399,00 — deixe em branco se não quiser mostrar preço riscado', false);
  texto('Plano 1 — preço de venda ("por")', 'Ex.: R$ 230,00', true);
  texto('Plano 1 — valor equivalente por mês', 'Ex.: "R$ 230,00 por mês". Deixe em branco se não se aplica.', false);
  paragrafo('Plano 1 — o que está incluso',
    'Liste um item por linha. Ex.: treino personalizado / acesso ao app / suporte no WhatsApp', false);
  texto('Plano 2 — nome', 'Ex.: "Trimestral"', false);
  texto('Plano 2 — preço cheio ("de")', '', false);
  texto('Plano 2 — preço de venda ("por")', '', false);
  texto('Plano 2 — valor equivalente por mês', '', false);
  paragrafo('Plano 2 — o que está incluso', '', false);
  texto('Plano 3 — nome', 'Ex.: "Semestral"', false);
  texto('Plano 3 — preço cheio ("de")', '', false);
  texto('Plano 3 — preço de venda ("por")', '', false);
  texto('Plano 3 — valor equivalente por mês', '', false);
  paragrafo('Plano 3 — o que está incluso', '', false);
  texto('Texto dos botões dos planos', 'Ex.: "Assine agora", "Quero esse plano"', false);
  var destino = form.addMultipleChoiceItem();
  destino.setTitle('Para onde o botão de cada plano deve levar?')
         .setChoiceValues([
           'WhatsApp com mensagem pronta',
           'Link de pagamento (vou informar abaixo)',
           'Ainda não sei / decidir depois'
         ]).setRequired(true);
  paragrafo('Links de pagamento (se você marcou essa opção)',
    'Cole um link por linha, dizendo a qual plano corresponde.', false);

  // ============ 8. SOBRE VOCÊ ============
  secao('8. Sobre você', 'A parte que gera conexão. Escreva do seu jeito, sem se preocupar com a escrita — a gente ajusta.');
  texto('Título da seção', 'Ex.: seu nome, ou "Quem sou eu"', false);
  paragrafo('Sua apresentação',
    'Quem é você, sua formação e especializações, há quanto tempo trabalha com isso.', true);
  paragrafo('Sua história com o treino',
    'Como começou, o que te fez virar personal. É o trecho que mais aproxima o cliente.', false);
  paragrafo('O que você quer entregar para o aluno',
    'Seu objetivo com a consultoria, o tipo de suporte que oferece.', false);
  foto('Uma foto sua para essa seção', 'Pode ser mais informal, treinando ou atendendo.', false);

  // ============ 9. PERGUNTAS FREQUENTES ============
  secao('9. Perguntas frequentes',
    'As dúvidas que seus alunos mais mandam antes de fechar. Se quiser usar as perguntas padrão, escreva "usar padrão" na primeira.');
  texto('Pergunta 1', 'Ex.: "Os treinos são personalizados de acordo com o meu nível?"', true);
  paragrafo('Resposta 1', '', true);
  texto('Pergunta 2', '', false);
  paragrafo('Resposta 2', '', false);
  texto('Pergunta 3', '', false);
  paragrafo('Resposta 3', '', false);
  texto('Pergunta 4', '', false);
  paragrafo('Resposta 4', '', false);
  texto('Pergunta 5', '', false);
  paragrafo('Resposta 5', '', false);

  // ============ 10. ATENDIMENTO PRESENCIAL ============
  secao('10. Atendimento presencial', '');
  var pres = form.addMultipleChoiceItem();
  pres.setTitle('Você também atende presencialmente?')
      .setChoiceValues(['Sim', 'Não'])
      .setRequired(true);
  paragrafo('Texto sobre o presencial',
    'Ex.: como funciona, se as vagas são limitadas, onde você atende. Só preencha se respondeu "Sim".', false);

  // ============ 11. LOJA / PRODUTOS ============
  secao('11. Loja ou produtos próprios', 'Só preencha se você vende algo além da consultoria.');
  var loja = form.addMultipleChoiceItem();
  loja.setTitle('Você tem marca de produtos, loja ou e-book?')
      .setChoiceValues(['Sim', 'Não'])
      .setRequired(true);
  texto('Nome da marca / loja', 'Ex.: @usecarolsantos', false);
  texto('O que você vende', 'Ex.: "Roupas de treino, garrafinhas e muito mais."', false);
  texto('Link da loja', '', false);
  foto('Foto dos produtos', '', false);

  // ============ 12. FECHAMENTO ============
  secao('12. Últimos detalhes', '');
  paragrafo('Texto de rodapé',
    'Uma frase curta resumindo seu trabalho, que aparece no final da página. Pode deixar em branco.', false);
  paragrafo('Alguma coisa que você NÃO quer no site?',
    'Ex.: não quero mostrar preço, não quero fotos de antes e depois, não quero meu sobrenome...', false);
  paragrafo('Mais alguma informação importante?', 'Espaço livre.', false);
  texto('Prazo desejado / data que você precisa do site no ar', '', false);

  var url = form.getPublishedUrl();
  var edit = form.getEditUrl();

  Logger.log('=======================================');
  Logger.log('LINK PARA ENVIAR AOS PERSONAIS:');
  Logger.log(url);
  Logger.log('');
  Logger.log('LINK PARA VOCE EDITAR / VER RESPOSTAS:');
  Logger.log(edit);
  Logger.log('=======================================');

  return { publico: url, edicao: edit };
}
