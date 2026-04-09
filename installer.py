import requests
import json
import subprocess
import os
import sys 
import time


def checar_conexao(ping: str):
    cmd = ["ping", ping, "-c", "1"]
    if os.name == "nt":
        cmd = ["ping", ping]

    st = subprocess.run(cmd)
    return st.returncode


def validar_json(objeto: list, chaves: list, instancias: list):
    dicionarios_val = 0
    chaves_num = len(chaves)

    # Checar se é lista
    if not isinstance(objeto, list):
        return False

    # Já elimina caso esteja vazio
    if len(objeto) < 1:
        return False

    # Verificação de validade
    for item in objeto:
        # Ja excclui se um item já não é dicionário
        if not isinstance(item, dict):
            return False
        
        chaves_vaalidas = 0
        indice = 0
        for chave in chaves:
            if chave in item.keys():
                if isinstance(item[chave], instancias[indice]):
                    chaves_vaalidas += 1
        
            indice += 1

        if chaves_vaalidas != chaves_num:
            return False
        else:
            dicionarios_val += 1

    return True


class JsonRules:
    chaves = ["url", "destino", "argumentos"]
    instancias = [str, str, list]

# Classe de download
class Download():
    def __init__(self, url: str, destino: str, useragent: str="autoinstaller/1.0.0", timeout: float=5.0):
        self.url = url
        self.destino = destino
        self.timeout = timeout
        self.useragent = useragent

    
    # Função de download
    def download(self):
        script_headers = {"User-Agent": self.useragent}

        print("Baixando...")
        req = requests.get(self.url, timeout=self.timeout, headers=script_headers)
        headers = req.headers
        # Baixar o arquivo
        if req.status_code == 200:
            with open(self.destino, "wb") as arqv:
                arqv.write(req.content)
        else:
            raise requests.HTTPError(str(req.content))


class Downloader():
    def __init__(self, lista: list):
        self.json = lista

    def download(self):
        for arquivo in self.json:
            url = arquivo["url"]
            destino = arquivo["destino"]

            dwl = Download(url, destino)
            dwl.download()


# Classe do instalador
class Installer():
    def __init__(self, executavel: str, argumentos: list) -> int:
        self.executavel = executavel
        self.argumentos = argumentos

    def install(self):
        comando = [self.executavel]
        comando.extend(self.argumentos)
        resultado = subprocess.run(comando)

        return resultado.returncode

def main():
    print("="*10)
    print("AutoInstaller v1.0.0 by Breno Martins")
    print("="*10)

    # Verificar argumento da linha de comando
    if len(sys.argv) != 2:
        print("Uso: python script.py <arquivo.json>")
        sys.exit(1)

    arquivo_json = sys.argv[1]

    # Verificar conexão com a internet
    print("Verificando conexão com a internet...")
    while checar_conexao("8.8.8.8") != 0:
        print("Sem conexão com a internet. Verifique e pressione Enter para tentar novamente.")
        input()
    print("Conexão estabelecida.\n")

    # Carregar e validar o arquivo JSON
    try:
        with open(arquivo_json, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo_json}' não encontrado.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Erro: Arquivo JSON inválido. {e}")
        sys.exit(1)

    if not validar_json(dados, JsonRules.chaves, JsonRules.instancias):
        print("Erro: Estrutura do JSON inválida. Esperado lista de dicionários com chaves:", JsonRules.chaves)
        sys.exit(1)

    # Iterar e processar cada entrada
    for idx, item in enumerate(dados, start=1):
        url = item["url"]
        destino = item["destino"]
        argumentos = item["argumentos"]

        print(f"\n[{idx}/{len(dados)}] Processando: {destino}")

        # Download
        try:
            downloader = Download(url, destino)
            downloader.download()
            print(f"Download concluído: {destino}")
        except Exception as e:
            print(f"Falha no download de {url}: {e}")
            continue

        # Instalação
        try:
            print(f"Iniciado instalação de {destino}.")
            instalador = Installer(destino, argumentos)
            status = instalador.install()

            if status == 0:
                print(f"Instalação concluída: {destino}")
            else:
                print(f"Instalação falhou com código {status}.")
        except Exception as e:
            print(f"Falha na instalação de {destino}: {e}")
            continue

    print("\nProcesso finalizado.")


if __name__ == "__main__":
    main()
