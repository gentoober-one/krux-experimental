# Testes de regressão

| Verificação | Resultado |
|---|---|
| SHA-256 do original contra o lançamento oficial | Coincide |
| CRC do ZIP experimental e comparação de DEX, bibliotecas e assets | Passaram |
| Assinatura Android v2 e v3 e alinhamento | Passaram |
| Reconstrução a partir do APK original e do patch | Todas as entradas compartilhadas com o APK assinado tiveram conteúdo idêntico. A saída sem assinatura omite três entradas em `META-INF`. |
| Exclusões em `cloud-backup` e `device-transfer` | Nove domínios em cada modalidade |
| Instalação, abertura e leitura de QR no aparelho | Pendente |
| Backup, restauração e migração entre aparelhos | Pendente |

Para testar a migração, crie uma carteira fictícia no aparelho de origem. Faça a transferência para outro aparelho e confira se os dados privados da carteira reaparecem no destino. Registre a versão do Android, o modelo e o mecanismo de transferência. Repita separadamente para restauração de backup em nuvem, com uma conta de teste.
