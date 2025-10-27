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

![ix](imagens\ix.py.png)


Saída Json
````
python ix.py --json
````

![ixjson](imagens\ix.py_json.png)


Saída Seletiva
````
python ix.py --name "Rio de Janeiro,"
````

![ixname](imagens\ix_name.png)


### Zabbix - Low-Level Discovery Rule (LLD)

