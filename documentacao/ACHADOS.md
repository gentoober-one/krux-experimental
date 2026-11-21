# Backup dos dados da carteira

No manifesto original, `android:allowBackup` estava habilitado. No bytecode de `src/krux/encryption.pyc`, dentro de `assets/private.tar`, encontrei a referência a um arquivo de armazenamento de carteiras.

```text
114 LOAD_CONST ("../seeds.json")
116 STORE_NAME (STORE_FILE_PATH)
```

Essa referência identifica o caminho usado pelo código. Ela não demonstra que uma carteira tenha sido copiada ou que o arquivo contenha dados em texto aberto. A medida adotada foi excluir o armazenamento do aplicativo dos mecanismos de backup e migração declarados ao Android.

| Item | Original | Experimental |
|---|---|---|
| `allowBackup` | `true` | `false` |
| `fullBackupContent` | ausente | `false` |
| `dataExtractionRules` | ausente | `@xml/auditoria_exclusao_backup` |

Também examinei o início de `RAND_bytes` na biblioteca ARM64 `libcrypto1.1.so`. Estas duas instruções fazem parte da preparação da pilha.

```asm
0x23bb64  sub sp, sp, #0x30
0x23bb68  str x30, [sp, #0x20]
```

Mantive o bytecode e as instruções ARM64 do original. A comparação do APK assinado cobre os 36 itens em DEX, bibliotecas e assets. O efeito prático das regras ainda depende de uma restauração com dados fictícios. [Comparação dos APKs](../metadados/validacao.json) · [Roteiro de teste](REGRESSAO.md).
