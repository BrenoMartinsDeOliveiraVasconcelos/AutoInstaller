# AutoInstaller

Isso é um script que automaticamente baixa e executa arquivos de instalação através de um arquivo JSON. Necessário Python para executar

Execute `python3 installer.py <Arquivo JSON>`.

## Modelo de arquivo

O arquivo JSON deve ser composto de uma lista, e dentro dessa lista deve ter dicionários com `url` para download, `destino` do arquivo baixado e os `argumentos` na linha de comando.

Exemplo:
```json
[
    {
        "url": "https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7BCD43C927-1346-7965-174D-14ADB330175B%7D%26lang%3Dpt-BR%26browser%3D3%26usagestats%3D1%26appname%3DGoogle%2520Chrome%26needsadmin%3Dprefers%26ap%3D-arch_x64-statsdef_1%26installdataindex%3Dempty/update2/installers/ChromeSetup.exe",

        "destino": "office.exe",
        "argumentos": ["/silent", "/install"]
    }
]
```
