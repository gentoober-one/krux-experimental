"""Confere os arquivos incluídos no Git antes da publicação."""
import re as expressoes
import subprocess as processos
from pathlib import Path as Caminho

RAIZ = Caminho(__file__).resolve().parents[1]


def principal():
    resposta = processos.run(["git", "ls-files", "-z"], cwd=RAIZ, check=True, capture_output=True)
    nomes = [nome.decode("utf-8") for nome in resposta.stdout.split(b"\0") if nome]
    if not nomes:
        raise SystemExit("Nenhum arquivo no índice Git; prepare o conjunto antes de verificar")
    proibidos = {".apk", ".idsig", ".jar", ".zip", ".p12", ".pfx", ".jks", ".keystore", ".key", ".pem", ".log"}
    padroes = [r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
               r"\bgh[pousr]_[A-Za-z0-9]{30,}\b", r"\bgithub_pat_[A-Za-z0-9_]{30,}\b",
               r"(?i)[A-Z]:[\\/]Users[\\/](?!Public\b|Default\b)[^\s\\/]+"]
    falhas = []
    for nome in nomes:
        arquivo = RAIZ / nome
        if arquivo.suffix.lower() in proibidos or arquivo.name.startswith(".env"):
            falhas.append(nome + ": extensão ou nome privado")
            continue
        if arquivo.stat().st_size > 1024 * 1024:
            falhas.append(nome + ": arquivo grande inesperado")
            continue
        texto = arquivo.read_text(encoding="utf-8-sig")
        for padrao in padroes:
            if expressoes.search(padrao, texto):
                falhas.append(nome + ": padrão sensível; revisar sem publicar o conteúdo")
                break
    if falhas:
        raise SystemExit("\n".join(falhas))
    print("Conferência aprovada: " + str(len(nomes)) + " arquivos no índice; nenhum binário ou padrão sensível identificado")


if __name__ == "__main__":
    principal()
