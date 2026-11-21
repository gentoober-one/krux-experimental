# Instalação de teste

Baixe `Krux-EXPERIMENTAL.apk` e confira o SHA-256 com `Get-FileHash .\Krux-EXPERIMENTAL.apk -Algorithm SHA256`. Compare o resultado com `VERIFICACAO-SHA256.txt` do lançamento.

Em um aparelho de teste sem o pacote `selfcustody.github.io.krux`, a instalação por USB pode ser feita com `adb -d install .\Krux-EXPERIMENTAL.apk`.

A instalação sobre o Krux oficial pode retornar `INSTALL_FAILED_UPDATE_INCOMPATIBLE`. Os dois APKs têm o mesmo identificador e certificados diferentes. Use outro aparelho ou um emulador para preservar a instalação e os dados da carteira existente.
