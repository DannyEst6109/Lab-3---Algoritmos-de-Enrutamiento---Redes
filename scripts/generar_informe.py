from pathlib import Path
import re, html, json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from io import BytesIO
from pypdf import PdfReader

root=Path(__file__).resolve().parents[1]
out=root
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='CodeSmall',fontName='Courier',fontSize=7,leading=9))
styles['Normal'].fontSize=10; styles['Normal'].leading=14
def p(s): return Paragraph(s,styles['Normal'])
def title(s): return Paragraph(s,styles['Heading1'])
def footer(c,d):
 c.setFont('Helvetica',8); c.setFillColor(colors.HexColor('#536273')); c.drawString(36,24,'UVG | Redes | Laboratorio 3'); c.drawRightString(559,24,str(d.page))
def build(name,story):
 SimpleDocTemplate(str(out/name),pagesize=A4,rightMargin=36,leftMargin=36,topMargin=36,bottomMargin=40).build(story,onFirstPage=footer,onLaterPages=footer)
def agregar_caratula(file):
 from pypdf import PdfWriter
 datos=json.loads((root/'documentacion/caratula.json').read_text(encoding='utf-8'))
 buf=BytesIO(); c=canvas.Canvas(buf,pagesize=letter)
 def centro(txt,y,size=13,bold=False):
  c.setFont('Times-Bold' if bold else 'Times-Roman',size); c.drawCentredString(306,y,txt)
 centro('Universidad del Valle de Guatemala',706,15,True)
 centro('Facultad de Ingeniería',688)
 centro('Redes - Sección 10 - Semestre 2, 2026',670)
 c.drawImage(str(root/'documentacion/recursos/logo_uvg.png'),170.7,351.25,width=270.6,height=270.6,mask='auto')
 centro('Laboratorio 3 - Algoritmos de Enrutamiento',291,16,True)
 centro('Planificación IP, VLSM, VLANs y enrutamiento',269,13.6)
 centro('OSPF / EIGRP con redistribución',249,12.6)
 centro('Integrante:' if len(datos['integrantes']) == 1 else 'Integrantes:',190,12,True)
 for i,persona in enumerate(datos['integrantes']): centro(persona,172-i*18,12)
 centro(datos['fecha'],83,12)
 c.showPage(); c.save(); buf.seek(0)
 writer=PdfWriter(); writer.append(PdfReader(buf)); writer.append(PdfReader(file)); writer.write(file)

def extract(name,command):
 text=(root/'evidencias/salidas'/f'{name}.txt').read_text(encoding='utf-8')
 pos=text.rfind('#'+command)
 if pos>=0: text=text[text.rfind('\n',0,pos)+1:]
 text=text.replace(' --More--','').replace('--More--','')
 return text.strip()

story=[title('Laboratorio 3 - Evidencias de enrutamiento'),p('Packet Tracer 9.0 | Evidencias reales de configuración y conectividad | 5 de octubre de 2026'),Spacer(1,16),p('<b>Archivo principal:</b> Lab3_Enrutamiento.pkt. Cinco routers, cuatro switches y seis PCs de prueba. OSPF área 0 y EIGRP AS 100.'),Spacer(1,12),p('<b>Limitación pendiente:</b> el IOS simulado rechazó summary-address de OSPF, route-map y distribute-list. En el archivo principal, CENTRAL publica 172.16.0.0/24 mediante una ruta estática Null0 con distancia 250, redistribuida como OSPF E1. El tráfico utiliza las rutas EIGRP más específicas. Esto logra conectividad y un resumen, pero NO cumple literalmente la redistribución dinámica EIGRP hacia OSPF solicitada.'),Spacer(1,12),p('Lab3_Redistribucion_Directa.pkt conserva redistribución dinámica mutua, pero anuncia las LAN EIGRP específicas hacia OSPF y presenta realimentación del agregado OSPF. Las dos variantes tienen esta diferencia documentada; ninguna se presenta como cumplimiento total del requisito avanzado.'),Spacer(1,12),p('<b>OSPF:</b> enlace directo costo 20 y vía CENTRAL costo 10 + 10. Las rutas a LAN remota cuestan 21 en ambos caminos, sumando costo LAN 1.'),Spacer(1,12),p('<b>EIGRP:</b> variance 4. De EIGRP-1 a EIGRP-2: métricas 102656 y 310016 (3.020:1); de EIGRP-2 a EIGRP-1: 104960 y 312320 (2.976:1). Ambas rutas alternativas cumplen distancia reportada menor que distancia factible. Es evidencia de métricas/configuración, no una medición de tráfico 75/25.'),Spacer(1,12),p('Las evidencias EIGRP se obtuvieron antes del cambio de origen del resumen OSPF; las métricas, vecinos y rutas internas EIGRP no cambiaron. Las tablas OSPF, CENTRAL, ping y tracert corresponden a la variante principal final. El PDF1 debe ser escrito a mano por los estudiantes.'),PageBreak()]
for router in ['R-OSPF-1','R-OSPF-2','R-CENTRAL','R-EIGRP-1','R-EIGRP-2']:
 story += [title(router+' - tabla de enrutamiento'),p('Salida real: show ip route'),Spacer(1,12),Preformatted(extract(router+'_rutas','show ip route'),styles['CodeSmall']),PageBreak()]
for router in ['R-OSPF-1','R-OSPF-2']:
 story += [title(router+' - interfaces OSPF'),p('Las interfaces seriales muestran costos 20 y 10. El segundo tramo vía CENTRAL añade 10; las dos rutas se verifican en la tabla anterior.'),Spacer(1,12),Preformatted(extract(router+'_interfaces','show ip ospf interface'),styles['CodeSmall']),PageBreak()]
for router in ['R-EIGRP-1','R-EIGRP-2']:
 for suffix,cmd in [('topologia','show ip eigrp topology'),('protocolos','show ip protocols')]:
  story += [title(router+' - '+suffix),Preformatted(extract(router+'_'+suffix,cmd),styles['CodeSmall']),PageBreak()]
for name,caption in [('PC0_ping_final','Ping desde PC0 (192.168.1.2) a PC5 (172.16.0.2): cuatro respuestas y 0% de pérdida.'),('PC0_tracert_final','Tracert desde PC0 a PC5: recorrido por la frontera CENTRAL hasta el extremo EIGRP.')]:
 story += [title('Conectividad extremo a extremo'),p(caption),Spacer(1,12),Preformatted(extract(name,''),styles['CodeSmall']),Spacer(1,12),Image(str(root/'evidencias/capturas'/f'{name}.jpg'),width=365,height=370),PageBreak()]
story += [title('Topología construida'),Image(str(root/'evidencias/capturas/topologia_final.jpg'),width=520,height=276),Spacer(1,16),p('Los seis enlaces seriales y las conexiones LAN están activos. PC0 y PC1 prueban las VLAN 10 y 30 de OSPF-1; PC3 y PC4 prueban las VLAN 10 y 20 de EIGRP-1.'),p('La página 2 del enunciado menciona tres VLAN en EIGRP-1, pero la tabla detallada de página 3 define únicamente dos. Se implementaron las dos especificadas en esa tabla; conviene aclarar la discrepancia con el docente.')]
build('Informe_Laboratorio_3.pdf',story)
agregar_caratula(root/'Informe_Laboratorio_3.pdf')

story=[title('Guía para el PDF1 manuscrito'),p('<b>Material de apoyo. Este documento mecanografiado NO sustituye los cálculos y conceptos escritos A MANO exigidos por el laboratorio.</b>'),Spacer(1,14),p('Escribe nombres y carnés de ambos integrantes. Incluye el procedimiento de cada LAN y enlace: demanda de hosts, bits de host, prefijo, máscara, red, rango útil y broadcast.'),title('Procedimiento VLSM'),p('Ordena las demandas de mayor a menor dentro de cada bloque. Busca h con 2^h - 2 >= equipos finales + gateway. Prefijo = 32 - h. El tamaño del bloque es 2^h. No asignas red ni broadcast.'),p('OSPF: 200 + 1 requiere h=8, /24 (254 útiles); 50 + 1 requiere h=6, /26 (62); 10 + 1 requiere h=4, /28 (14). EIGRP: 100 + 1 requiere /25 (126); 60 + 1 requiere /26 (62); 30 + 1 requiere /26 (62). Si el docente cuenta el gateway dentro de los 30 hosts, /27 permite 30 IP útiles; aquí se reservan 30 equipos finales más gateway.'),p('Cada enlace serial: dos interfaces, h=2, /30, dos IP útiles. Bloques base: 192.168.0.0/20, 172.16.0.0/20 y 10.0.0.0/24.'),PageBreak(),title('Tabla para reproducir a mano')]
lines=(root/'documentacion/direccionamiento.md').read_text(encoding='utf-8').splitlines()
rows=[]
for line in lines:
 if line.startswith('|') and not line.startswith('|---'):
  vals=[x.strip() for x in line.strip('|').split('|')]
  rows.append([p(vals[0]),p(vals[2]+'<br/>'+vals[3]),p(vals[4]+'<br/>'+vals[5]),p(vals[6])])
rows[0]=[p('<b>Segmento</b>'),p('<b>Red/prefijo y máscara</b>'),p('<b>Rango útil</b>'),p('<b>Broadcast</b>')]
t=Table(rows,colWidths=[125,155,130,110],repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e9f0f7')),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#bdc9d6')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7)])); story += [t,PageBreak(),title('Conceptos para explicar con tus palabras')]
for head,body in [
 ('VLAN y router-on-a-stick','Una VLAN separa dominios de broadcast. El enlace trunk 802.1Q transporta varias VLAN. Las subinterfaces del router tienen etiquetas VLAN y gateways distintos; permiten enrutamiento entre VLANs.'),
 ('OSPF, área e interfaces pasivas','OSPF usa estado de enlace y cálculo de camino de menor costo. Todos los routers OSPF usan área 0. Una interfaz pasiva anuncia su subred sin enviar Hellos ni formar vecinos en la LAN de usuarios. ECMP instala caminos de costo igual.'),
 ('EIGRP, successor y feasible successor','El successor es el mejor siguiente salto. Un feasible successor cumple RD < FD: distancia reportada por el vecino menor que la distancia factible local, condición que protege contra bucles. Variance permite instalar rutas factibles cuyo costo está dentro del múltiplo del mejor costo.'),
 ('Métrica y reparto cercano a 75/25','Con K predeterminados: M = 256 × (10^7/BW mínimo en kbps + suma de retardos en unidades de 10 microsegundos). Seriales: bandwidth 100000; delay directo 300; acceso hacia CENTRAL 1100; CENTRAL hacia acceso 10. En EIGRP-1: 310016/102656 = 3.020. Un reparto inverso ideal da 75.1% al mejor camino. Variance 4 habilita el alterno; no fija por sí solo un porcentaje.'),
 ('Redistribución y métrica semilla','Redistribuir importa rutas de un protocolo en otro. EIGRP recibe cinco atributos: bandwidth, delay, reliability, load y MTU. Se configuró 100000 100 255 1 1500. La MTU no participa en la fórmula de métrica predeterminada.'),
 ('OSPF E1 frente a E2','E1 suma métrica externa y costo interno hasta el ASBR. E2 compara principalmente la métrica externa; el costo interno sirve para desempatar. Se eligió E1 para reflejar el costo total hasta CENTRAL.'),
 ('Sumarización','Agrupa prefijos contiguos mediante bits iniciales comunes, reduciendo anuncios y tamaño de tablas. LAN OSPF: 192.168.0.0/23 cubre el /24 y las dos VLAN en 192.168.1.x. Los terceros octetos 00000000 y 00000001 comparten siete bits: 16+7=23. LAN EIGRP: /25 + /26 + /26 llenan 172.16.0.0/24. Las rutas específicas ganan al resumen; Null0 descarta destinos no asignados y ayuda a evitar bucles.'),
 ('Limitación del simulador','Explica las dos variantes sin afirmar que el agregado estático es redistribución dinámica EIGRP hacia OSPF. La configuración IOS propuesta con summary-address y filtros requiere un entorno que admita esos comandos. Aclara además la discrepancia de dos/tres VLAN del enunciado.')]:
 story += [Paragraph(head,styles['Heading2']),p(body)]
story += [Spacer(1,12),p('Fuentes de consulta: Cisco, How Does Unequal Cost Path Load Balancing (Variance) Work in EIGRP? (documento 13677-19); Cisco, Redistributing Routing Protocols (8606-redist); Cisco IOS EIGRP Command Reference. También se usaron los materiales de clase proporcionados.'),p('Después de escribir tus hojas, escanéalas o fotografíalas con buena iluminación y combínalas en PDF1_Manuscrito.pdf. El PDF2 ya contiene salidas reales y capturas.')]
build('documentacion/Guia_PDF1_Manuscrito.pdf',story)
for file in [root/'Informe_Laboratorio_3.pdf',root/'documentacion/Guia_PDF1_Manuscrito.pdf']: print(file.name,len(PdfReader(file).pages),'páginas')
