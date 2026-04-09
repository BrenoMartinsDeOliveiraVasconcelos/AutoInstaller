import requests

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


if __name__=='__main__':
    t = Download("www.globo.com", "a")
    t.download()