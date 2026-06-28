Nautilus V.Beta.34
Corrige a causa raiz do erro "Não foi possível baixar o Atlas agora" que podia ocorrer mesmo com internet funcionando: o app agora espera o leitor de PDF (carregado de um CDN externo) terminar de carregar antes de desistir, e preserva o PDF já baixado mesmo se essa etapa específica falhar. Veja CHANGELOG.txt para o histórico completo de mudanças.
