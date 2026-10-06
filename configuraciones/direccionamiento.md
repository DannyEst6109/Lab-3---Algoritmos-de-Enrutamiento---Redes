# Direccionamiento propuesto del laboratorio

Bloques base: OSPF 192.168.0.0/20; EIGRP 172.16.0.0/20; enlaces 10.0.0.0/24.

| Segmento | Hosts requeridos | Red/prefijo | Mascara | Primer host | Ultimo host | Broadcast |
|---|---:|---|---|---|---|---|
| R-OSPF-2 LAN | 200 | 192.168.0.0/24 | 255.255.255.0 | 192.168.0.1 | 192.168.0.254 | 192.168.0.255 |
| R-OSPF-1 VLAN 10 | 50 | 192.168.1.0/26 | 255.255.255.192 | 192.168.1.1 | 192.168.1.62 | 192.168.1.63 |
| R-OSPF-1 VLAN 30 | 10 | 192.168.1.64/28 | 255.255.255.240 | 192.168.1.65 | 192.168.1.78 | 192.168.1.79 |
| R-EIGRP-2 LAN | 100 | 172.16.0.0/25 | 255.255.255.128 | 172.16.0.1 | 172.16.0.126 | 172.16.0.127 |
| R-EIGRP-1 VLAN 10 | 60 | 172.16.0.128/26 | 255.255.255.192 | 172.16.0.129 | 172.16.0.190 | 172.16.0.191 |
| R-EIGRP-1 VLAN 20 | 30 | 172.16.0.192/26 | 255.255.255.192 | 172.16.0.193 | 172.16.0.254 | 172.16.0.255 |
| OSPF-1 a OSPF-2 | 2 | 10.0.0.0/30 | 255.255.255.252 | 10.0.0.1 | 10.0.0.2 | 10.0.0.3 |
| CENTRAL a OSPF-1 | 2 | 10.0.0.4/30 | 255.255.255.252 | 10.0.0.5 | 10.0.0.6 | 10.0.0.7 |
| CENTRAL a OSPF-2 | 2 | 10.0.0.8/30 | 255.255.255.252 | 10.0.0.9 | 10.0.0.10 | 10.0.0.11 |
| EIGRP-1 a EIGRP-2 | 2 | 10.0.0.12/30 | 255.255.255.252 | 10.0.0.13 | 10.0.0.14 | 10.0.0.15 |
| CENTRAL a EIGRP-1 | 2 | 10.0.0.16/30 | 255.255.255.252 | 10.0.0.17 | 10.0.0.18 | 10.0.0.19 |
| CENTRAL a EIGRP-2 | 2 | 10.0.0.20/30 | 255.255.255.252 | 10.0.0.21 | 10.0.0.22 | 10.0.0.23 |

La VLAN 20 reserva capacidad para 30 equipos finales mas el gateway. Por eso usa /26.
Los gateways LAN usan el primer host utilizable. Los PCs de prueba usan el segundo.

Resumen LAN OSPF: 192.168.0.0/23. Resumen LAN EIGRP: 172.16.0.0/24.
Los resumenes se calculan a partir de las subredes usadas, no necesariamente de todo el bloque base /20.

Estado: propuesta calculada; las evidencias de funcionamiento se deben obtener de Packet Tracer.