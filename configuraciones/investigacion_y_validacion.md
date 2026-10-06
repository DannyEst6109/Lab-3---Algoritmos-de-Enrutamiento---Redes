# Notas para resolver el laboratorio

Estado: diseno y comandos propuestos, pendientes de validar contra IOS de Packet Tracer. No son salidas reales de los routers.

## VLSM
Para LAN convencionales se busca h tal que 2^h - 2 >= hosts, incluyendo la IP del gateway si los hosts pedidos son equipos finales. Prefijo = 32-h. Asignar primero las redes mas grandes dentro de cada bloque. Las direcciones de red y broadcast no se asignan a equipos.

## OSPF
Area unica 0. Interfaces LAN pasivas: anuncian su red pero no forman vecindades con PCs. Enlace directo entre accesos costo 20; cada tramo pasando por CENTRAL costo 10. El costo de la interfaz LAN de destino se agrega a ambos caminos, por lo que la igualdad se mantiene. Deben observarse dos next hops en show ip route hacia la LAN remota.

## EIGRP
AS 100. Interfaces LAN pasivas y no auto-summary. Con los K predeterminados, metrica clasica = 256 * (10^7 / BW_min_en_kbps + suma_de_delays_en_decenas_de_microsegundos).
Propuesta: bandwidth 100000 en los seriales; delay 300 en el enlace directo; delay 1100 desde cada acceso hacia CENTRAL; delay 10 desde CENTRAL hacia cada acceso. Las metricas son direccionales.
Si la LAN Gigabit de destino tiene delay de 10 microsegundos (1 unidad), la ruta directa tiene metrica 102656 y la via CENTRAL 310016. Relacion 3.01995:1. La distancia reportada por CENTRAL prevista es 28416, menor que la distancia factible de 102656; por tanto cumple la condicion de factibilidad. Con variance 4, 310016 < 4*102656.
Esta es una prediccion para validar, no una medicion. Comprobar metrica de interfaz LAN y traffic share count en el simulador. Variance no equivale por si solo a un porcentaje.

## Redistribucion
Hacia EIGRP se indica ancho de banda, retardo, confiabilidad, carga y MTU: 100000 100 255 1 1500. Las unidades de retardo son decenas de microsegundos. La MTU se transporta como atributo, no interviene en la formula predeterminada de metrica.
OSPF E1 suma el costo interno hasta el ASBR a la metrica externa. E2 prioriza la metrica externa, usando el costo interno para resolver empates. Se propone E1, para reflejar el costo total hasta la frontera unica.
Los route-map propuestos permiten solo redes LAN del dominio de origen, evitando reinyectar rutas del otro lado y evitando redistribuir los enlaces de transporte. Su compatibilidad con Packet Tracer debe comprobarse antes de afirmar que se aplicaron.

## Sumarizacion
OSPF LAN utiliza 192.168.0.0/24, 192.168.1.0/26 y 192.168.1.64/28. El menor prefijo unico que las cubre es 192.168.0.0/23.
EIGRP LAN utiliza 172.16.0.0/25, 172.16.0.128/26 y 172.16.0.192/26. El resumen es 172.16.0.0/24.
Se debe mostrar el prefijo binario comun. En OSPF, summary-address resume rutas externas en el ASBR; en EIGRP, ip summary-address se aplica en las interfaces de salida hacia el otro dominio. Una ruta de descarte Null0 del resumen previene bucles hacia espacios no asignados; las rutas mas especificas hacia LAN reales tienen prioridad.

## Evidencias que faltan
- show ip route de los cinco routers.
- show ip ospf interface y show ip route hacia LAN OSPF remota.
- show ip eigrp topology, show ip protocols y show ip route hacia LAN EIGRP remota.
- ping y tracert desde 192.168.1.2 hacia 172.16.0.2.
- Guardar configuraciones y .pkt final.

## Fuentes oficiales
- https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/13677-19.html
- https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/8606-redist.html
- https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_eigrp/command/ire-cr-book/ire-i1.html

PDF1 requiere calculos y conceptos escritos a mano por los estudiantes. Estas notas sirven como guia; no sustituyen esa evidencia.
