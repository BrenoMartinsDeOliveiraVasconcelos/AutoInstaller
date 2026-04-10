#!/bin/bash

echo "======================="
echo "Instalando dependências"
echo "======================="

if command -v apt; then
    sudo apt install python3-venv
else
    echo "Caso dê erro, instale python3-venv manualmente."
fi

python3 -m venv ./venv

./venv/bin/python3 -m pip install -r requirements.txt