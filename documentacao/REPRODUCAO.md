# Reconstrução no Windows

Usei Python 3.13, Git, Java 17, Apktool 3.0.3 e Android SDK Build Tools 35.0.0. O script confere o SHA-256 do APK original e do Apktool antes de abrir os arquivos. Ele usa um diretório temporário e gera um APK alinhado, pronto para assinatura.

Na raiz do repositório, ajuste os caminhos para as ferramentas locais. [APK original](https://github.com/selfcustody/KruxMobileApp/releases/tag/26.06.beta1.A_02) · [Apktool 3.0.3](https://github.com/iBotPeaches/Apktool/releases/tag/v3.0.3).

```powershell
$original = '.\Krux_26.06.beta1_Android_0.2.apk'
$apktool = '.\apktool_3.0.3.jar'
$ferramentas = Join-Path $env:LOCALAPPDATA 'Android\Sdk\build-tools\35.0.0'
python ferramentas\reconstruir.py --original $original --apktool $apktool --zipalign "$ferramentas\zipalign.exe" --saida .\krux-alinhado.apk
```

Para assinar uma reconstrução com sua própria chave de testes, use o prompt de senha do `apksigner`. A assinatura e o SHA-256 final dependem da chave utilizada.

```powershell
& "$ferramentas\apksigner.bat" sign --ks .\chave-de-teste.jks --out .\krux-teste.apk .\krux-alinhado.apk
& "$ferramentas\apksigner.bat" verify --verbose --print-certs .\krux-teste.apk
& "$ferramentas\zipalign.exe" -c -P 16 4 .\krux-teste.apk
python ferramentas\verificar_apk.py $original .\krux-teste.apk
python -m unittest discover -s testes -v
```

A comparação valida o ZIP, detecta inclusões, remoções ou alterações no DEX, nas bibliotecas e nos assets e lista as diferenças entre as demais entradas. Para conferir as regras no próprio binário, use o AAPT.

```powershell
& "$ferramentas\aapt.exe" dump xmltree .\krux-teste.apk AndroidManifest.xml
& "$ferramentas\aapt.exe" dump xmltree .\krux-teste.apk res/xml/auditoria_exclusao_backup.xml
```
