# AutoInstaller

Isso é um script que automaticamente baixa e executa arquivos de instalação através de um arquivo JSON. Também é posspivel executar comandos no invés de baixar.

## Modelo de arquivo

* Usando `--dwl <ARQUIVO JSON>` como argumento:

Esse argumento baixa o arquivo da internet e instala executando ele na linha de comando.

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

* Usando `--cmd <ARQUIVO JSON>` como argumento:

Esse argumento executa um comando já existente no `PATH` do sistema na linha de comando.

O arquivo JSON deve ser composto de uma listra, e dentro dessa lista deve ter dicionários com o `comando` a ser executado e seus `argumentos`.

Exemplo:
```json
[
    {
       "comando": "winget",
       "argumentos": ["install", "--accept-source-agreements", "--accept-package-agreements", "chrome"]
    }
]
```

## Nota de segurança

O script NÃO evita a instalação de malwares e nem foi feito paa isso, portando, o ussuário ainda deve tomar cuidado sobre os arquivos que baixa a instala pela internet.
