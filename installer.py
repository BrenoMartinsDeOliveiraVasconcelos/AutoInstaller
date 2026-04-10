import requests
import json
import subprocess
import os
import sys 
import argparse
import traceback


def welcome():
    texto = "AutoInstaller v1.0.0 - By Breno Martins"
    tamanho = len(texto)
    print("="*tamanho)
    print(texto)
    print("="*tamanho)


def output(texto: str, severidade: int, sufixo: str = ""):
    prefixos = ["INFO", "AVISO", "ERRO", "FATAL", "INPUT"]

    print(f"[{prefixos[severidade]}] {texto}{sufixo}")


def ask(texto: str, inp_str: str) -> str:
    output(texto, 4)
    return input(inp_str)


def pause():
    return ask("Pressione enter para continuar.", "")


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


class JsonRulesDWLs:
    chaves = ["url", "destino", "argumentos"]
    instancias = [str, str, list]


class JsonRulesCMDs:
    chaves = ["comando", "argumentos"]
    instancias = [str, list]

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

        req = requests.get(self.url, timeout=self.timeout, headers=script_headers)
        headers = req.headers
        # Baixar o arquivo
        if req.status_code == 200:
            with open(self.destino, "wb") as arqv:
                arqv.write(req.content)
        else:
            raise requests.HTTPError(str(req.content))


# Classe do instalador
class Installer():
    def __init__(self, executavel: str, argumentos: list) -> int:
        self.executavel = executavel
        self.argumentos = argumentos

    def install(self) -> int:
        comando = [self.executavel]
        comando.extend(self.argumentos)
        try:
            resultado = subprocess.run(comando)
        except FileNotFoundError:
            if os.name != "nt":
                comando[0] = "./" + comando[0]
                resultado = subprocess.run(comando)

        return resultado.returncode

def main():
    welcome()
    
    # Criar argumentos para json
    parser = argparse.ArgumentParser()
    parser.add_argument('--dwl', type=str, default="")
    parser.add_argument('--cmd', type=str, default="")

    argumentos = parser.parse_args() # Argumentos passados

    cmd = argumentos.cmd
    dwl = argumentos.dwl

    cmd = cmd.removesuffix("/")
    dwl = dwl.removesuffix("/")
    lista_args = [cmd, dwl]
    vazio = [not x for x in lista_args]
    existentes = [os.path.exists(x) for x in lista_args]

    if False not in vazio:
        output("Pelo menos 1 argumento deve ser passado.", 3)
        sys.exit(1)

    
    if True not in existentes:
        output("Por favor, passe arquivos que existem como argumentos.", 3)
        sys.exit(1)


    output("Checando conexão com a internet.", 0)
    # Checar conexão com a internet antes de começar
    while checar_conexao("8.8.8.8") != 0:
        output("Verifique a conexão com a internet antes de continuar.", 3)
        pause()
    output("Conexão estabelecida", 0)


    # Por fim, começar o processo
    if dwl != "":
        objeto = json.load(open(dwl))
        json_valido = validar_json(objeto, JsonRulesDWLs.chaves, JsonRulesDWLs.instancias)
        
        if json_valido:
            for item in objeto:
                url = item["url"]
                destino = item["destino"]
                argumento_exec = item["argumentos"]

                # Baixar
                try:
                    output(f"Baixando {destino}.", 0)
                    download = Download(url, destino, timeout=10.0)
                    download.download()
                except requests.exceptions.ConnectionError:
                    output(f"Erro ao baixar arquivo. Ignorando.", 2)
                    pause()
                    continue
                except Exception as e:
                    erro = traceback.format_exc()
                    output(erro, 2)
                    continue

                # Instalar
                output(f"Instalando {destino}...", 0)
                try:
                    installer = Installer(destino, argumento_exec)
                    resultado = installer.install()

                    if resultado != 0:
                        output(f"Erro ao instalar {destino}: {resultado}", 2)
                    else:
                        output(f"{destino} foi instalado com sucesso!", 0)
                except PermissionError:
                    output(f"O usuário atual não tem permissão para executar {destino}.", 2)
                except FileNotFoundError:
                    output(f"{destino} não pôde ser encontrado.", 2)
                except Exception as e:
                    output(traceback.format_exc(), 2)
        else:
            output("O arquivo JSON em --dwl é inválido.", 3)

    # Caso o argumento de instalar por comando esteja presente
    if cmd != "":
        objeto = json.load(open(cmd))
        json_valido = validar_json(objeto, JsonRulesCMDs.chaves, JsonRulesCMDs.instancias)

        if json_valido:
            for item in objeto:
                comando = item["comando"]
                argumento_exec = item["argumentos"]

                try:
                    output(f"Executando {comando} {' '.join(argumento_exec)}...", 0)
                    instalador = Installer(comando, argumento_exec)
                    resultado = instalador.install()

                    if resultado != 0:
                        output(f"Erro ao executar o comando: {resultado}", 2)
                    else:
                        output('Comando executaado com sucesso.', 0)

                except PermissionError:
                    output("O usuário não tem permissão paa executar esse comando.", 2)
                    continue
                except FileNotFoundError:
                    output("O comando não pode ser encontrado.", 2)
                except Exception as e:
                    output(traceback.format_exc(), 2)
        else:
            output("O arquivo JSON em --cmd é inválido.", 3)


if __name__ == "__main__":
    try:
        main()
        output("Processo finalizado!", 0)
        pause()
    except json.JSONDecodeError:
        output("Erro ao ler arquivo JSON.", 3)
    except Exception as e:
        output(traceback.format_exc(), 3)
