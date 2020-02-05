# LabCidados
Empacotador de dados abertos do [LabCidade - FAUUSP](http://www.labcidade.fau.usp.br/), desenvolvido para documentação e divulgação de dados produzidos ou retrabalhados pelo laboratório.

*Último congelamento: LabCidados 2020.1 (05/01/2020)*
*Próxima versão: Sem previsão*

## Conteúdo
Este repositório possui a seguinte estrutura principal:

    LabCidados
    ├ LabCidados py
    │	├ LabCidados.pyw
    │	├ licencas
    │	│	└[…]
    │	├ recursos
    │	│	└[…]
    │	└ LabCidados.ui
    ├ LabCidados 2020-1
	│	├ LabCidados.exe
	│	└[…]
    ├ LICENSE
    └ README.md

A pasta */LabCidados py* contém o código-fonte original (*LabCidados.pyw*), a interface do usuário desenvolvida no Qt Designer (*LabCidados.ui*) e os diretórios com recursos usados pelo programa. A pasta */LabCidados 2020-1* contém uma versão congelada do código-fonte, que não requer uma instalação de Python, bastando apenas executar o arquivo *LabCidados.exe*.

## Executando o LabCidados
Para usar o LabCidados, deve-se primeiro descompactar todos os arquivos em alguma pasta do seu computador. Em seguida, existem duas alternativas possíveis:
#### 1. Via executável
Basta clicar no arquivo *LabCidados.exe*, na subpasta */LabCidados 2020-1*. Este arquivo permite criar atalhos para o LabCidados na sua área de trabalho ou menus, como qualquer outro programa. Contudo, é possível que este arquivo seja classificado como malware pelo seu antivírus, ou que seja incompatível com seu sistema operacional. Nesses casos, recomendamos a segunda alternativa.
#### 2. Via script Python
Para esta alternativa, é necessária uma instalação local de [Python 3.7](https://www.python.org/downloads/release/python-375/). Atendido este requisito, basta clicar no arquivo *LabCidados.pyw*, na subpasta */LabCidados py*. A primeira inicialização pode levar algum tempo, pois será instalado o pacote PyQt5 - que conecta o código e a interface do usuário. Certifique-se de possuir uma conexão com a internet nesta ocasião.
___
