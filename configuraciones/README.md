# Configuraciones

`aplicadas/` contiene los bloques utilizados para configurar los dispositivos de acceso y la configuración completa exportada de CENTRAL (`R-CENTRAL.txt`). Los `.cfg` se importan desde la pestaña Config de Packet Tracer; no incluyen `enable` ni `configure terminal`.

El simulador muestra un máximo de cuatro caminos aunque los bloques de acceso solicitan `maximum-paths 2`; las tablas capturadas muestran los dos caminos relevantes. Las salidas reales del informe son la referencia de validación.

`propuestas/R-CENTRAL_propuesta.cfg` es el diseño con filtros y sumarización para un IOS que acepte esos comandos. No se aplicó íntegramente en Packet Tracer. Ver `documentacion/estado_y_limitaciones.md`.
