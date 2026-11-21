import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as xml
from zipfile import ZipFile

from ferramentas.verificar_apk import comparar


class TestePublicacao(unittest.TestCase):
    def test_exclusoes_em_cada_modalidade(self):
        raiz = Path(__file__).resolve().parents[1]
        regras = xml.parse(raiz / "alteracoes/auditoria_exclusao_backup.xml").getroot()
        self.assertEqual([modo.tag for modo in regras], ["cloud-backup", "device-transfer"])
        dominios = {"root", "file", "database", "sharedpref", "external", "device_root",
                    "device_file", "device_database", "device_sharedpref"}
        for modo in regras:
            self.assertEqual({(item.tag, item.get("domain"), item.get("path")) for item in modo},
                             {("exclude", dominio, ".") for dominio in dominios})

    def test_detecta_mudanca_no_dex(self):
        with tempfile.TemporaryDirectory() as pasta:
            original, alterado = (Path(pasta) / nome for nome in ("um.zip", "dois.zip"))
            for pacote, conteudo in [(original, b"original"), (alterado, b"alterado")]:
                with ZipFile(pacote, "w") as arquivo:
                    arquivo.writestr("classes.dex", conteudo)
            self.assertEqual(comparar(original, original)["alteradas"], [])
            with self.assertRaises(ValueError):
                comparar(original, alterado)
