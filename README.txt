Livro Histórico v54 / App v54

Alterações desta versão:
- Ajuste visual do ícone de compartilhar nos cards LDS para símbolo de três pontos conectados no estilo ChatGPT.
- Alteração limitada ao ícone do botão; função de compartilhamento, texto compartilhado, busca, cards, IndexedDB e importação LDS preservados.
- LDS: removido o botão redundante “Atualizar LDS”.
- LDS: mantido apenas o botão “Importar LDS”.
- LDS: o botão “Importar LDS” agora cobre primeira importação e substituição completa da base existente.
- LDS: adicionada importação com modal bloqueante de progresso percentual por etapas.
- LDS: modal exibe etapa atual, percentual e barra de progresso durante leitura/processamento/indexação.
- LDS: navegação interna fica bloqueada durante a importação para evitar inconsistência.
- LDS: importação valida o XLSX antes de apagar a base anterior, reduzindo risco de perda por arquivo inválido.

Módulo alterado:
- LDS

Módulos preservados:
- Launcher/tela inicial
- Livro Histórico
- Livro Histórico DA
- Horas
- Relatórios
- Dashboard
- Notas / Bloco de notas
- Backup
- PDFs
- Topbar
- Navegação geral

Observações técnicas:
- A busca LDS, os cards e o compartilhamento LDS foram preservados.
- A estrutura IndexedDB foi mantida.
- O progresso é calculado por fases e por lotes durante a gravação, evitando atualização de DOM a cada registro.
- A versão visual do app/menu foi atualizada para v54.

Histórico recente:
- v48: módulo LDS offline com IndexedDB e busca corrigida.
- v49: Bloco de Notas com altura automática, sem rolagem interna na nota, botão expandir/recolher e persistência individual.
- v50: LDS com botão Compartilhar em cada card de resultado.
- v51: LDS com compartilhamento refinado nos cards.
- v53: LDS com importação única e modal de progresso bloqueante.


Correção v53:
- Corrigida a importação LDS no IndexedDB para evitar o erro “Failed to execute put on IDBObjectStore: The transaction is not active”.
- A gravação dos registros LDS agora é feita em lotes com uma nova transação readwrite por lote.
- O modal de progresso foi mantido, mas as atualizações de interface ocorrem fora das transações IndexedDB.
- Aceite de arquivo atualizado para XLSX/XLSM quando suportado pelo parser interno.
- Módulos preservados: Launcher, Livro Histórico, Livro Histórico DA, Horas, Relatórios, Dashboard, Notas, Backup, PDFs, Topbar, busca LDS, cards LDS e compartilhamento LDS.
- Versão visual do app/menu atualizada para v53.


Registro v54:
- Módulo alterado: LDS.
- Ajuste: ícone de compartilhar dos cards de resultado alterado para SVG inline local de três pontos conectados, sem texto e sem dependência externa.
- Módulos preservados: Launcher, Livro Histórico, Livro Histórico DA, Horas, Relatórios, Dashboard, Notas, Backup, PDFs, Topbar e navegação geral.
- Busca, importação, modal de progresso, IndexedDB, cards e texto compartilhado da LDS mantidos sem alteração funcional.
