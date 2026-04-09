import requests
import json


# Classe com protocolos para facilitar
class Protocolos:
    HTTP = "http"
    HTTPS = "https"

# Classe de download
class Download():
    def __init__(self, url: str, destino: str, protocolo: str = "https", useragent: str="autoinstaller/1.0.0"):
        self.url = protocolo + "://" + url
        self.destino = destino
        self.timeout = 5
        self.useragent = useragent

    
    # Função de download
    def download(self):
        script_headers = {"User-Agent": self.useragent}

        req = requests.get(self.url, timeout=self.timeout, headers=script_headers)
        headers = req.headers

        tp_arquivo = headers["Content-Type"].split("/")[1].split(";")[0] if "Content-Type" in headers.keys() else "none"
        print(tp_arquivo)

        print("Baixando...")

        # Baixar o arquivo
        if req.status_code == 200:
            # Verificar o nome do arquivo em destino para por ou não a extensão
            if not self.destino.endswith(tp_arquivo):
                self.destino += f".{tp_arquivo}"

            with open(self.destino, "wb") as arqv:
                arqv.write(req.content)
        else:
            raise requests.HTTPError(str(req.content))


class Downloader():
    def __init__(self, caminho_lista: str):
        self.caminho_lista = caminho_lista
        
        if not self._json_valido():
            raise TypeError("Formato invalido de JSON")

    
    def _json_valido(self) -> bool: # Validação .json
        self.json = json.load(open(self.caminho_lista))
        chaves = ["url", "destino"]
        instancias_chaves = [str, str]
        dicionarios_val = 0
        chaves_num = len(chaves)

        # Checar se é lista
        if not isinstance(self.json, list):
            return False

        # Verificação de validade
        for item in self.json:
            # Ja excclui se um item já não é dicionário
            if not isinstance(item, dict):
                return False
            
            chaves_vaalidas = 0
            indice = 0
            for chave in chaves:
                if chave in item.keys():
                    if isinstance(item[chave], instancias_chaves[indice]):
                        chaves_vaalidas += 1
            
                indice += 1

            if chaves_vaalidas != chaves_num:
                return False
            else:
                dicionarios_val += 1


        if dicionarios_val < len(self.json) and dicionarios_val > 0:
            return False

        return True


if __name__=='__main__':
    t = Downloader("list.json")