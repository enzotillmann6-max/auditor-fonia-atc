# Decisões — Auditor de fonia ATC

## O que foi priorizado

O desenvolvimento foi feito em etapas, na ordem do pipeline (captura →
transcricao → regras → relatorio → modo avulso → config → README),
garantindo que cada parte estivesse funcionando de fato antes de avancar
para a proxima. A prioridade era assegurar que a maquina funcionasse de
ponta a ponta com dados reais, em vez de construir todos os modulos em
paralelo e só depois integrar.

## O que ficou de fora

Por causa do prazo, ficaram de fora melhorias pontuais em varias partes
do sistema, mas o maior ponto que ficou de fora foi automatizar mais o
processo como um todo. A ideia original era ter uma automacao mais
completa, que exigisse menos intervencao manual para rodar captura,
transcricao e geracao de relatorios em sequencia.

Os diferenciais do desafio (analise por LLM, painel web, radar ADS-B,
testes automatizados, empacotamento para rodar 24/7, retencao
configuravel) nao foram implementados nesta entrega; o MVP foi a
prioridade.

## O que seria feito com mais tempo

Com mais tempo, o sistema seria lapidado e o processo seria deixado mais
automatizado, reduzindo a necessidade de rodar cada modulo manualmente
e tornando a execucao mais direta.

## Falsos positivos na amostra

Na amostra de aproximadamente 1 hora capturada da Torre de Congonhas, o
motor de regras nao apontou nenhuma ocorrencia (0 ocorrencias). A fonia
capturada nesse periodo nao continha nenhum dos gatilhos de severidade
critica, alta, media ou baixa cobertos pelo motor de regras — nao houve,
portanto, falsos positivos a reportar nesta amostra. O motor de regras
foi validado separadamente com uma frase de teste ("a aeronave esta
arremetendo agora"), que disparou corretamente a categoria ARREMETIDA
com severidade alta.