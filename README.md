# Krux Experimental

Minha versão de testes do Krux Mobile para Android, baseada na `26.06.beta1.A_02`. Alterei as regras de backup porque o aplicativo pode manter dados de carteira no armazenamento privado. A versão de origem também é destinada a testes com carteiras fictícias. [Lançamento original](https://github.com/selfcustody/KruxMobileApp/releases/tag/26.06.beta1.A_02).

## O que alterei

Desativei o backup no manifesto. Para o Android 12 em diante, acrescentei regras explícitas de exclusão para o backup em nuvem e a transferência entre aparelhos. Cada regra cobre os nove domínios de armazenamento enumerados no XML. [Diferença no manifesto](alteracoes/manifesto.patch) · [Regras de extração](alteracoes/auditoria_exclusao_backup.xml).

Comparei os dois APKs. As 36 entradas de DEX, bibliotecas nativas e assets permaneceram idênticas. O manifesto e a tabela de recursos mudaram. O Apktool também regravou caminhos de recursos. Conferi a assinatura e o alinhamento do pacote. O comportamento de uma restauração entre dois aparelhos ainda precisa de teste. [Resultado da comparação](metadados/validacao.json) · [Análise técnica](documentacao/ACHADOS.md).

## Download

O pré-lançamento reúne o APK, a soma SHA-256 e a comparação com o original. [Baixar a versão experimental](https://github.com/gentoober-one/krux-experimental/releases/tag/v26.06.beta1-android.0.2-exp.1).

| Identificação | Valor |
|---|---|
| Pacote | `selfcustody.github.io.krux` |
| Versão interna do Android | `26.06.0` (código `1024260600`) |
| Android mínimo | 7.0 (API 24) |
| SHA-256 do APK experimental | `633abbba7edc06f57372a6d7830d71334f7c18d2e0fcc9f0cea535658b25f17a` |
| SHA-256 do certificado experimental | `9fbbf468259d4f9d3f84e43eb689bd5ec910d9b9f1574479b70434451700254f` |

O Android identifica esta compilação pelo mesmo nome de pacote do Krux original e por outra assinatura. Para testar, use um aparelho ou emulador dedicado com o pacote livre. [Instalação](documentacao/INSTALACAO.md).

## Reconstrução

Registrei os comandos de reconstrução, assinatura e comparação, além dos testes que dependem de um aparelho. [Reprodução](documentacao/REPRODUCAO.md) · [Testes de regressão](documentacao/REGRESSAO.md).

## Créditos

O aplicativo é do projeto Krux. Minha alteração se concentra no empacotamento Android. [Créditos e licenças](AVISOS.md).
