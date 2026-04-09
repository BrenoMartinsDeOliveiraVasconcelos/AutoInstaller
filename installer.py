import requests
import json

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
    chaves = ["url", "destino"]
    instancias = [str, str]

# Classe de download
class Download():
    def __init__(self, url: str, destino: str, useragent: str="autoinstaller/1.0.0"):
        self.url = url
        self.destino = destino
        self.timeout = 5
        self.useragent = useragent

    
    # Função de download
    def download(self):
        script_headers = {"User-Agent": self.useragent}

        print("Baixando...")
        req = requests.get(self.url, timeout=self.timeout, headers=script_headers)
        headers = req.headers
        # Baixar o arquivo
        if req.status_code == 200:

            print(f"Salvando como {self.destino}! Pode demorar um pouco.")
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
            print(f"URL: {url} -> {destino}")

            dwl = Download(url, destino)
            dwl.download()


if __name__=='__main__':
    lista = json.load(open("list.json"))
    v = validar_json(lista, JsonRules.chaves, JsonRules.instancias)
    t = Downloader(lista)
    t.download()
    print(lista, v)