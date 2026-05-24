Nautilus v119 / App v119

Alterações desta versão:
- Renomeada a opção “Dados da Ficha” para “Cadastrar/Editar Equipamentos”.
- Adicionado fluxo de cadastro de equipamentos com botão “Adicionar equipamento”.
- O formulário antigo de “Dados da ficha” foi preservado e passa a abrir somente ao adicionar ou editar um equipamento.
- Equipamentos salvos aparecem em lista abaixo do botão principal, com botão “Editar” ao lado de cada item.
- O campo “Equipamento” em “Novo Registro” agora é somente seleção: não permite digitação manual.
- A lista do campo “Equipamento” em “Novo Registro” passa a exibir os equipamentos cadastrados em “Cadastrar/Editar Equipamentos”.
- Ao gerar a Folha 01 / A-1 de um equipamento, os dados cadastrais do equipamento selecionado são usados no cabeçalho da folha.
- Dados antigos de ficha são migrados de forma retrocompatível para a nova lista de equipamentos quando houver equipamento cadastrado.

Módulo alterado:
- Nautilus / Cadastro de Equipamentos / Novo Registro / Documento Oficial.

Módulos preservados:
- LDS offline
- Importação XLSX/XLSM
- Compartilhamento LDS
- Cards LDS
- Modal de progresso LDS
- Launcher/tela inicial
- Horas
- Relatórios
- Dashboard
- Notas / Bloco de notas
- Backup
- PDFs
- Topbar
- Navegação geral
- app_documento_oficial_impressao_direta_forcada.html

Observações técnicas:
- Alteração isolada no módulo de equipamentos e integração do campo “Equipamento”.
- Não houve alteração na base IndexedDB da LDS.
- Persistência continua via dados locais do app, com leitura retrocompatível de fichas antigas.
- O dropdown de equipamentos funciona mesmo quando não há equipamentos cadastrados.
- A versão visual do app/menu foi atualizada para v61.
- Cache offline atualizado para v61.

Histórico recente:
- v48: módulo LDS offline com IndexedDB e busca corrigida.
- v49: Bloco de Notas com altura automática, sem rolagem interna na nota, botão expandir/recolher e persistência individual.
- v50: LDS com botão Compartilhar em cada card de resultado.
- v51: LDS com compartilhamento refinado nos cards.
- v53: LDS com importação única e modal de progresso bloqueante.
- v54: ícone de compartilhar LDS ajustado para estilo ChatGPT.


Registro v56:
- Horas de Funcionamento: atualização de horas agora possui campos Anos, Dias e Horas, com resultado convertido automaticamente para total em horas.
- Quando apenas Horas é preenchido, o resultado replica o mesmo valor em horas.
- Backup/importação corrigidos para preservar e restaurar dados de Horas de Funcionamento.
- README/changelog, cache e versão visual atualizados para v56.

Registro v55:
- “Dados da Ficha” renomeado para “Cadastrar/Editar Equipamentos”.
- Cadastro/listagem/edição de equipamentos implementado.
- “Novo Registro” passa a aceitar somente equipamento selecionado da lista cadastrada.
- Folha 01 / A-1 passa a usar os dados do equipamento selecionado.
- README/changelog, cache e versão visual atualizados para v55.


v57 - Horas de funcionamento: unificação adicionar/editar equipamentos e nova tela adicionar/editar bigramas.

v60 - Correções: restaurado nome Livro Histórico em módulos internos; ajuste menu Bigramas.

v61 - Correção efetiva da v60:
- Restaurada a opção “Adicionar/Editar Bigramas” no menu de Horas de funcionamento, logo abaixo de “Adicionar/Editar Equipamentos”.
- Corrigido o botão “Excluir” da tela “Adicionar/Editar Bigramas”, com remoção do item correto, atualização imediata da lista e persistência.
- Mantido “Nautilus” apenas como branding/nome do app/PWA/instalação.
- Preservado “Livro Histórico” em módulos internos, incluindo “Imprimir Livro Histórico” e relatórios/documentos do módulo.
- Modal de bigramas ajustado para respeitar a topbar/linha amarela.
- Versão visual, README/changelog, service worker/cache e ZIP atualizados para v61.


v62 - Correção do menu Livro Histórico e exclusão de Bigramas.

Nautilus v64 / App v64
Alterações desta versão:
- Adicionado botão “Fechar” no modal “Adicionar/Editar Bigramas” em Horas de funcionamento.
- Ajustado espaçamento no Bloco de Notas para listas de notas arquivadas.
- Ajustado espaçamento no Bloco de Notas para listas de notas excluídas/lixeira.
- Preservados os botões Salvar, Editar e Excluir dos bigramas e demais módulos do app.
- Versão visual, cache e pacote ZIP incrementados para v64.

- v66: removido botão fechar superior duplicado em Adicionar/Editar Bigramas.


v68 - LDS agora exibe 'Aplicação em outros Equipamentos' com associação automática por NSN.

v70 - LDS: corrigida a seção 'Aplicação em outros Equipamentos' para consultar a base real IndexedDB da aba Configured Items Tree, removendo dependência de cache inexistente, normalizando NSN e evitando falso 'Nenhuma outra aplicação encontrada'. Versão visual/cache/ZIP atualizados para v70.


v71 - LDS: otimizada a seção 'Aplicação em outros Equipamentos' com índice/cache por NSN da aba Configured Items Tree, busca limitada à coluna NSN, remoção dos rótulos Functional Mark/Parent Functional Mark nos resultados e versionamento/ZIP atualizados para v71.
v72 - LDS: removidos traços/linhas vazias da seção 'Aplicação em outros Equipamentos' e texto de compartilhamento LDS compactado em formato técnico para WhatsApp, preservando performance e compatibilidade offline/mobile.
v73 - Histórico: cards de Ver Histórico passam a exibir todas as informações diretamente no card, sem botão/ícone Visualizar e sem repetir Equipamento no corpo do card. Versão visual/cache/ZIP atualizados para v73.


v74 - LDS: restaurado o formato anterior do compartilhamento dos cards e ajustada a seção de aplicações relacionadas para exibir o título 'N° DE IDENTIFICAÇÃO' com apenas os valores válidos, sem rótulos Functional Mark/Parent Functional Mark. Versão visual/cache/ZIP atualizados para v74.

v75 - LDS: restaurado o título correto da seção 'Aplicação em outros Equipamentos:' nos cards, desfazendo a substituição indevida por 'N° DE IDENTIFICAÇÃO', mantendo a lista de códigos e a busca NSN otimizada. Versão visual/cache/ZIP atualizados para v75.


v76 - Imprimir Livro Histórico: geração DOCX ajustada para seguir o modelo PDF enviado, com paginação/código de folha no topo, maior aproveitamento vertical por página, espaçamentos mais compactos e área de assinaturas preservada. Versão visual/cache/ZIP atualizados para v76.


v77 - Bloco de Notas: corrigida altura automática durante edição inline, evitando corte/rolagem interna e card reduzido após salvar; incluído botão Salvar ao lado da lixeira, visível somente em modo edição. Versão visual/cache/ZIP atualizados para v77.

v78 - Bloco de Notas: correção real do modo edição validada, mantendo textarea com autoaltura durante digitação, botão Salvar visível somente em edição, saída da edição apenas ao salvar e card sem corte após renderização. Versão visual/cache/ZIP atualizados para v78.

v79 - Bloco de Notas: corrigida de fato a passagem do estado de edição para a renderização dos botões, fazendo o botão Salvar aparecer somente em edição ao lado da lixeira; reforçada autoaltura real do textarea e manutenção do card expandido após salvar. Versão visual/cache/ZIP atualizados para v79.
v81 - Bloco de Notas: corrigido o autoajuste em tempo real durante a edição inline; a nota cresce conforme novas linhas/quebras aparecem e não encolhe durante a digitação. Mantidos botão Salvar, IndexedDB, navegação, LDS, PDFs e demais módulos sem alteração fora do escopo. Versão visual/cache/ZIP atualizados para v81.


v82 - Bloco de Notas: corrigido o ponto de entrada no modo edição. Ao clicar em uma nota, a altura atual do card é capturada antes da renderização, aplicada como altura mínima da edição, e a textarea recebe altura via setProperty com !important para não ser sobrescrita por CSS anterior. A nota não deve reduzir nem esconder texto ao clicar em editar; continua podendo crescer em tempo real. ZIP limpo, sem ZIP interno indevido.

v84 - Bloco de Notas: adicionados botões para marcadores e caixas de seleção/checklist. Checkboxes marcados agora riscam o texto da linha e exibem um botão ✕ para apagar somente a linha concluída. Mantido editor leve, compatível com mobile/offline, sem alterar LDS, Horas de Funcionamento, topbar, launcher ou IndexedDB fora do escopo. Versão visual/cache/ZIP atualizados para v84.


v85 - Correção complementar: botões de Marcadores e Checklist agora aparecem também na barra inferior das notas como botões ativáveis, aplicando/removendo formatação em textos já digitados; checklist mantém texto riscado ao marcar e botão ✕ para remover a linha. Em Horas de Funcionamento, a reordenação de Bigramas agora altera a ordem real salva, com botão “Reordenar Bigramas” para mostrar/ocultar controles. A lista de Equipamentos foi reforçada com Editar/Excluir no mesmo padrão dos Bigramas, exclusão em tempo real e campos de anos/dias/horas com seleção automática. Versão visual/cache/ZIP atualizados para v85.


v86 - Ajuste visual das notas: botões de Marcadores e Checklist ficam somente com ícones, harmônicos com os demais botões; checklist renderizado com checkbox em coluna fixa e todo o texto do parágrafo alinhado fora da área da caixa, inclusive em quebras de linha. Versão/cache/ZIP atualizados para v86.


v87 - Ajuste real das cores dos botões ativos das notas: Fixar, Marcadores e Checklist agora usam azul padrão Nautilus, removendo preto e amarelo do estado selecionado.


v89 - Bloco de Notas: a categoria Outras agora preserva a posição das notas ao editar, salvar, aplicar Marcadores/Checklist, marcar checkbox ou excluir linha; a ordem não é mais baseada em updatedAt.


v89 - Bloco de Notas: removido o título “Buscar notas”, adicionada lupa no campo de busca e indicador visual de arrastar com reordenação mobile persistente tipo Keep.


v90 - Notas: remoção real do visual novo de arrastar e remoção da data/hora de última alteração da interface. Mantida busca com lupa e ordem estável.


v92 - Notas: refinado o visual do checklist; checkbox sem borda/fundo extra, alinhado à primeira linha, e X de exclusão menor, sem borda e sem fundo.


Versão v92: restauração isolada da opção Adicionar Bigrama no menu Livro Histórico.


v94 - Horas de Funcionamento: opção Adicionar/Editar Equipamentos agora abre o gerenciamento real com adicionar, editar e excluir; exclusão atualiza em tempo real. Menu inicial não exibe mais Adicionar Bigrama fora do Livro Histórico.


v97 - Notas: removido crescimento artificial do card ao entrar em edição; versionamento visual/cache atualizado; LDS passa a importar, indexar e buscar a coluna Reference Number.


v98 - LDS: busca por Reference Number corrigida no importador e na busca real, com normalização de NSN, aliases de cabeçalho e fallback de varredura direta para referências numéricas.


v99 - LDS: texto explicativo atualizado para incluir Reference Number; card de busca limpo removendo rótulo interno desnecessário.


v119 - Horas de Funcionamento: campos de anos, dias e horas agora selecionam todo o valor ao tocar/clicar e substituem imediatamente o valor antigo ao digitar.


v119 - Corrigido comportamento seguro dos campos anos/dias/horas: primeiro dígito substitui o valor antigo sem cursor no meio e sem tela branca.


v119 - Notas: cursor no ponto tocado e ajuste único acima do teclado, sem scroll contínuo.


v119 - Notas: checklist com caixas reais no modo edição, sem conversão para colchetes; validação de sintaxe JS antes da entrega.


v119 - Notas: checklist com caixas reais na edição preservando quebra de linha, wrap e largura do card.
