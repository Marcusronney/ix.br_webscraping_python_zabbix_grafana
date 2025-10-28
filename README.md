# ix.br_webscraping_python_zabbix_grafana
Monitorando Status do IX.BR com python e integrando ao Zabbix e Grafana.



Seguindo as boas práticas do Zabbix, o script será armazenado dentro de **externalscripts**

Permissão de Execução
````
chmod +x /lib/zabbix/externalscripts/python_ix/ix.py
````

Saída manual
````
python3 ix.py
````

![ix](imagens/ix.py.png)


Saída Json
````
python ix.py --json
````

![ixjson](imagens/ix_json.png)


Saída Seletiva
````
python ix.py --name "Rio de Janeiro,"
````

![ixname](imagens/ix_name.png)

---------------------------------

# TEMPLATE

### Item

![lld](imagens/item.png)

| Nome | Descrição | Key | Tipo | Intervalo de Atualização |
| - | - | - |
| IX.br status (JSON) | Coleta o Json do ix.py | ixbr.status.json | Zabbix Agent | 10m |


### Status IX.BR - Low-Level Discovery Rule (LLD)

![lld](imagens/lld.png)

| Nome | Descrição | Key | Tipo | Item Mestre |
| - | - | - |
| IX.br sites | LLD para receber todos os sites do python em formato Json e sair via variável #IXNAME | ixbr.discovery | Item Dependente | IX.br status (JSON) |

Pré-Processamento JavaScript: Transforma o JSON bruto do item mestre em um array de descobertas.
````
var obj = JSON.parse(value);
var data = [];
for (var k in obj) {
  if (Object.prototype.hasOwnProperty.call(obj, k)) {
    data.push({ "{#IXNAME}": k });
  }
}
return JSON.stringify({ data: data });
````

![lldjavascript](imagens/javascript.png)


### Protótipo de item

![prototipo](imagens/prototipoitem.png)

| Nome | Descrição | Key | Tipo | Item Mestre |
| - | - | - |
| {#IXNAME} | Recebe o nome através da macro {#IXNAME} | ixbr.status[{#IXNAME}] | Item Dependente | IX.br status (JSON) |


![prototipo2](imagens/prototipoitem2.png)



Teste a saída via **zabbix_get** com a váriavel definida no Userparaments.
````
zabbix_get -s 127.0.0.1 -k ixbr.statuss
````

![teste](imagens/teste.png)

Também podemos rodar diretamente o script no servidor Zabbix.
````
/usr/bin/python3 /lib/zabbix/externalscripts/python_ix/ix.py | jq .
````

![test2](imagens/test2.png)
