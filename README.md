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
        "url": "https://c2rsetup.officeapps.live.com/c2r/download.aspx?productReleaseID=O365ProPlusRetail&platform=Def&language=pt-br",
        "destino": "office.exe",
        "argumentos": []
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
