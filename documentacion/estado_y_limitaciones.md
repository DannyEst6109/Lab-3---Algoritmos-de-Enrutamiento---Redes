# Laboratorio 3 - Redes UVG

## Archivos
- `packet_tracer/Lab3_Enrutamiento.pkt`: topología funcional con resumen compatible mediante origen estático hacia OSPF.
- `packet_tracer/variantes/Lab3_Redistribucion_Directa.pkt`: variante con redistribución dinámica mutua; sin resumen EIGRP hacia OSPF.
- `Informe_Laboratorio_3.pdf`: tablas reales de cinco routers, interfaces OSPF, topología y protocolos EIGRP, ping y tracert.
- `documentacion/Guia_PDF1_Manuscrito.pdf`: cálculos y conceptos para reproducir a mano; NO es el PDF1 exigido.
- `configuraciones/aplicadas/R-CENTRAL.txt`: configuración exportada del router CENTRAL de la variante principal.
- `evidencias/`: salidas y capturas originales.

## Estado comprobado
Cinco routers 1941, cuatro switches y seis PCs. Seis enlaces seriales /30 activos. Router-on-a-stick para VLAN 10/30 en OSPF-1 y VLAN 10/20 en EIGRP-1. OSPF área 0, EIGRP AS 100 e interfaces LAN pasivas.

OSPF instala dos caminos de costo 21 hacia las LAN del otro router de acceso. EIGRP instala dos caminos internos con variance 4: métricas 102656/310016 y 104960/312320 según el sentido. Las rutas alternas cumplen factibilidad. La evidencia del 75/25 es de configuración y métricas; no se midió reparto real de paquetes.

Ping PC0 192.168.1.2 -> PC5 172.16.0.2: cuatro respuestas, cero pérdida. Tracert: 192.168.1.1 -> 10.0.0.5 -> 10.0.0.22 -> 172.16.0.2.

## Limitación importante antes de entregar
El IOS simulado de Packet Tracer rechazó `summary-address` de OSPF, `route-map` y `distribute-list`. La variante principal usa `ip route 172.16.0.0 255.255.255.0 Null0 250` y `redistribute static metric-type 1 subnets`. CENTRAL continúa aprendiendo las LAN más específicas por EIGRP y las usa para reenviar. El agregado permanece anunciado aun si desaparecen todas esas rutas EIGRP; es una limitación de esta aproximación.

Esto NO cumple literalmente la redistribución dinámica EIGRP hacia OSPF del enunciado. La variante directa sí conserva esa redistribución, pero no su sumarización, y tiene realimentación del agregado OSPF. Se necesita aclarar con el docente cuál adaptación acepta o usar un entorno IOS que permita la configuración propuesta con filtros y sumarización. `R-CENTRAL_propuesta.*` contiene comandos de diseño que el simulador no aceptó; no representa la configuración aplicada.

La página 2 menciona tres VLAN para EIGRP-1, mientras la tabla detallada de la página 3 especifica dos. Se implementaron las dos de la tabla. Voz usa /26 para 30 equipos finales más gateway.

## Pendientes humanos
1. Escribir A MANO el procedimiento VLSM y conceptos; escanearlo como PDF1_Manuscrito.pdf. La guía mecanografiada solo sirve de apoyo.
2. Resolver con el docente la limitación del simulador y la discrepancia de VLAN.
3. Publicar el paquete en el GitHub indicado por el curso, tras revisar los archivos. La carátula ya identifica a Carlos Daniel Estrada Vega, carné 20853, como único integrante. No se ha publicado remotamente.

No se presenta este paquete como cumplimiento total mientras estos puntos sigan pendientes.
