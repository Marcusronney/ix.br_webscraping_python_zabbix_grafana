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

### Zabbix - Low-Level Discovery Rule (LLD)




Discovery rules
Name	Description	Type	Key and additional info
Interfaces	
-

SNMP agent	interfaces.discovery
Update: 3600

Memory Useage	
-

SNMP agent	memoryusage.discovery
Update: 3600

Mac Address	
-

SNMP agent	macaddress.discovery
Update: 3600

Temperature Discovery	
Discovering modules temperature (same filter as in Module Discovery) plus and temperature sensors

SNMP agent	temp.discovery
Update: 3600

CPU	
-

SNMP agent	cpu.discovery
Update: 3600

Fan Discovery	
Discovering all entities of PhysicalClass - 7: fan(7)

SNMP agent	fan.discovery
Update: 3600

Entity Discovery	
-

SNMP agent	entity.discovery
Update: 3600

PSU Discovery	
Discovering all entities of PhysicalClass - 6: powerSupply(6)

SNMP agent	psu.discovery
Update: 3600





