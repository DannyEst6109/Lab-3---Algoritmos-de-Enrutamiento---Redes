# Laboratorio 3: Algoritmos de Enrutamiento

Redes, sección 10 - Universidad del Valle de Guatemala.

**[Abrir el informe](Informe_Laboratorio_3.pdf)** · **[Abrir la simulación](packet_tracer/Lab3_Enrutamiento.pkt)**

Este laboratorio integra direccionamiento VLSM, VLANs, OSPF área 0 y EIGRP AS 100 en una red de cinco routers. El informe contiene tablas de enrutamiento, evidencias de balanceo y pruebas de conectividad.

## Organización

| Ubicación | Contenido |
| --- | --- |
| `Informe_Laboratorio_3.pdf` | Informe principal con carátula y evidencias reales (PDF2). |
| `packet_tracer/` | Simulación principal y variante con redistribución directa. |
| `configuraciones/aplicadas/` | Configuraciones de acceso y export real de CENTRAL. |
| `configuraciones/propuestas/` | Diseño de CENTRAL con comandos no admitidos por el simulador. |
| `evidencias/capturas/` | Capturas originales de las pruebas y los routers. |
| `evidencias/salidas/` | Salidas de comandos en texto. |
| `documentacion/` | Direccionamiento, conceptos, guía manuscrita y limitaciones. |
| `scripts/` | Script para regenerar el informe y la guía. |

## Resultados y pendientes

El ping de PC0 (192.168.1.2) a PC5 (172.16.0.2) obtuvo cuatro respuestas sin pérdida. El tracert alcanzó el destino a través de CENTRAL. OSPF instala dos caminos de igual costo; EIGRP tiene variance 4 y métricas próximas a una proporción de 3:1.

La variante principal anuncia el resumen EIGRP hacia OSPF mediante una ruta estática: **no satisface literalmente la redistribución dinámica exigida**. La variante directa conserva redistribución mutua, pero no el resumen en ese sentido. Ver [estado y limitaciones](documentacion/estado_y_limitaciones.md) antes de entregar.

El PDF1 debe escribirse a mano. La [guía](documentacion/Guia_PDF1_Manuscrito.pdf) sirve de apoyo y no sustituye ese entregable. El único integrante es Carlos Daniel Estrada Vega, carné 20853. Los datos de la carátula se guardan en [caratula.json](documentacion/caratula.json).

## Regenerar los documentos

Con Python, ReportLab y pypdf instalados:

```powershell
python scripts/generar_informe.py
```

El informe se guarda en la raíz y la guía en `documentacion/`. El logo se extrajo de la carátula de referencia proporcionada por el usuario.
