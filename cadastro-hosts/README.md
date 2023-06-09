# Cadastro Automatizado de Hosts no Zabbix

Este é um programa desenvolvido em Python para automatizar o cadastro de hosts no Zabbix por meio da API. Com esta ferramenta, é possível realizar o cadastro em massa de equipamentos a partir de um arquivo CSV.

# Requisitos

Antes de executar o programa, certifique-se de ter instalado os seguintes pacotes Python:

    csv: Biblioteca para manipulação de arquivos CSV.
    tkinter: Biblioteca para criação de interfaces gráficas.
    zabbix_api: Biblioteca de API para interação com o Zabbix.
    customtkinter: Biblioteca personalizada para estilização de elementos do tkinter.
    PIL: Biblioteca para processamento de imagens.

# Como Utilizar

Preencha os campos de conexão com as credenciais do Zabbix (servidor, usuário e senha).

Clique no botão "Conectar" para estabelecer uma conexão com a API do Zabbix.

Se a conexão for bem-sucedida, a mensagem "Conectado na API" será exibida em verde.

Clique no botão "Selecionar arquivo CSV" para escolher o arquivo contendo os dados dos hosts a serem cadastrados. 

Certifique-se de que o arquivo CSV esteja no seguinte formato:

    Host;Endereço IP;Tipo;Grupos;Templates;Conexao;Descricao
    Maquina2;192.168.0.1;Agent;Servidores;Template Linux;server;Maquina do datacenter
    Maquina2;192.168.0.2;SNMP;Roteadores,Switches;Template SNMP;proxy;Maquina pessoal

    Host: Nome do host.
    Endereço IP: Endereço IP do host.
    Tipo: Tipo de agente de monitoramento (Agent, SNMP).
    Grupos: Nomes dos grupos aos quais o host será associado, separados por vírgula.
    Templates: Nomes dos templates a serem aplicados ao host, separados por vírgula.
    Server: Indica se o host utilizará um proxy ou server.
    Descrição: Descrição do host.

Após selecionar o arquivo CSV, o caminho do arquivo será exibido no campo correspondente.

Clique no botão "Cadastrar Hosts" para iniciar o processo de cadastro dos hosts no Zabbix.

Durante o cadastro, o programa exibirá mensagens indicando o progresso e o status de cada host cadastrado.

Ao final do processo, a mensagem "Todos os hosts foram cadastrados" será exibida em verde.

# Observações

É importante garantir que os grupos e templates mencionados no arquivo CSV já estejam cadastrados no Zabbix.
Caso um host com o mesmo NOME já exista no Zabbix, o programa irá pular o cadastro desse host e exibirá a mensagem correspondente.
Caso seja necessário utilizar um proxy, certifique-se de que o proxy desejado esteja configurado corretamente no Zabbix e informe "proxy" na coluna "Conexao" do arquivo CSV.

# Autor

Este programa foi desenvolvido por Caio Davantel

© 2023 by Caio Davantel. Todos os direitos reservados.
