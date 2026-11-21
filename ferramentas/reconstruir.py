"""Reconstrói o APK alinhado a partir do lançamento Android 0.2."""
import argparse
import hashlib
import shutil
import subprocess
import tempfile
from pathlib import Path
from xml.etree import ElementTree as xml

RAIZ = Path(__file__).resolve().parents[1]
ORIGINAL = "f662b9d3f76e30d7785d0acc0e7d7358a595504ac9f62bcab28e5cb80b98ea28"
APKTOOL = "dbf930b076c6b9be08d57c449cacefc3bdd6b71ebd59b3066fc0e1f5b14f9423"
ANDROID = "{http://schemas.android.com/apk/res/android}"


def conferir_resumo(arquivo, esperado):
    with arquivo.open("rb") as entrada:
        if hashlib.file_digest(entrada, "sha256").hexdigest() != esperado:
            raise ValueError(f"SHA-256 divergente em {arquivo.name}")


def aplicar_alteracoes(pasta):
    manifesto = pasta / "AndroidManifest.xml"
    antes = xml.parse(manifesto).getroot()
    if antes.get("package") != "selfcustody.github.io.krux":
        raise ValueError("Pacote diferente do Krux")
    subprocess.run(["git", "apply", "--ignore-space-change", str(RAIZ / "alteracoes/manifesto.patch")],
                   cwd=pasta, check=True)
    aplicativo = xml.parse(manifesto).getroot().find("application")
    atributos = {"allowBackup": "false", "fullBackupContent": "false",
                 "dataExtractionRules": "@xml/auditoria_exclusao_backup"}
    if any(aplicativo.get(ANDROID + nome) != valor for nome, valor in atributos.items()):
        raise ValueError("Manifesto fora do esperado")
    destino = pasta / "res/xml/auditoria_exclusao_backup.xml"
    destino.parent.mkdir(exist_ok=True, parents=True)
    shutil.copyfile(RAIZ / "alteracoes" / destino.name, destino)


def principal():
    argumentos = argparse.ArgumentParser(description=__doc__)
    for nome in ("original", "apktool", "zipalign", "saida"):
        argumentos.add_argument("--" + nome, type=Path, required=True)
    opcoes = argumentos.parse_args()
    conferir_resumo(opcoes.original, ORIGINAL)
    conferir_resumo(opcoes.apktool, APKTOOL)
    if opcoes.saida.exists():
        argumentos.error("Escolha um nome de saída disponível")
    with tempfile.TemporaryDirectory() as temporaria:
        pasta = Path(temporaria)
        decodificado = pasta / "decodificado"
        comando = ["java", "-jar", str(opcoes.apktool.resolve())]
        estrutura = ["-p", str(pasta / "framework")]
        subprocess.run(comando + ["d", "-s", *estrutura, "-o", str(decodificado), str(opcoes.original.resolve())], check=True)
        aplicar_alteracoes(decodificado)
        pacote = pasta / "reconstruido.apk"
        subprocess.run(comando + ["b", *estrutura, "-o", str(pacote), str(decodificado)], check=True)
        alinhado = pasta / "alinhado.apk"
        subprocess.run([str(opcoes.zipalign.resolve()), "-P", "16", "4", str(pacote), str(alinhado)], check=True)
        with alinhado.open("rb") as entrada, opcoes.saida.open("xb") as saida:
            shutil.copyfileobj(entrada, saida)


if __name__ == "__main__":
    principal()
