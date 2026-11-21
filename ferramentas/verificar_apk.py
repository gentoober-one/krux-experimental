"""Compara o conteúdo descompactado dos APKs e calcula o SHA-256."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZipFile


def comparar(original, experimental):
    with ZipFile(original) as antes, ZipFile(experimental) as depois:
        for pacote in (antes, depois):
            if pacote.testzip() or len(pacote.namelist()) != len(set(pacote.namelist())):
                raise ValueError("ZIP com entrada inválida ou duplicada")
        iniciais = set(antes.namelist())
        finais = set(depois.namelist())
        def protegidas(nomes):
            return {nome for nome in nomes if nome.startswith(("assets/", "lib/")) or re.fullmatch(r"classes\d*\.dex", nome)}
        comuns = iniciais & finais
        alteradas = sorted(nome for nome in comuns if antes.read(nome) != depois.read(nome))
        if protegidas(iniciais) != protegidas(finais) or protegidas(alteradas):
            raise ValueError("Código, bibliotecas ou assets divergentes")
        return {"entradas_preservadas_de_codigo_bibliotecas_e_assets": len(protegidas(iniciais)),
                "alteradas": alteradas, "incluidas": sorted(finais - iniciais),
                "removidas": sorted(iniciais - finais)}


def principal():
    argumentos = argparse.ArgumentParser(description=__doc__)
    argumentos.add_argument("original", type=Path)
    argumentos.add_argument("experimental", type=Path)
    opcoes = argumentos.parse_args()
    resultado = comparar(opcoes.original, opcoes.experimental)
    for nome, caminho in vars(opcoes).items():
        with caminho.open("rb") as entrada:
            resultado["sha256_" + nome] = hashlib.file_digest(entrada, "sha256").hexdigest()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    principal()
