#!/usr/bin/env python3
"""Генератор draw.io (mxGraph XML) для Task1: InsureTech технологическая архитектура to-be."""
import html

def esc(s): return html.escape(s, quote=True)

class D:
    def __init__(self):
        self.cells = []
        self.id = 1
    def nid(self):
        self.id += 1
        return f"n{self.id}"
    def node(self, x, y, w, h, label, style, parent="1"):
        i = self.nid()
        self.cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{style}" vertex="1" parent="{parent}"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return i
    def edge(self, src, dst, label="", style=None, points=None):
        i = self.nid()
        st = style or "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#5B7DB1;strokeWidth=1.5;"
        pts = ""
        if points:
            pts = '<Array as="points">' + "".join(f'<mxPoint x="{p[0]}" y="{p[1]}"/>' for p in points) + '</Array>'
        self.cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{st}" edge="1" parent="1" source="{src}" target="{dst}"><mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>')
        return i

FRAME = "rounded=1;whiteSpace=wrap;html=1;fillColor=none;arcSize=6;dashed=1;"          # зона
K8S   = "rounded=1;whiteSpace=wrap;html=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;arcSize=8;"  # кластер
NSBOX = "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF2CC;strokeColor=#D6B656;arcSize=10;" # namespace
POD   = "rounded=1;whiteSpace=wrap;html=1;fillColor=#D5E8D4;strokeColor=#82B366;arcSize=12;" # под/сервис
DB    = "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#FFE6CC;strokeColor=#D79B00;"  # бд
EXT   = "rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#666666;arcSize=10;"  # внешний
USER  = "shape=ellipse;whiteSpace=wrap;html=1;fillColor=#E1D5E7;strokeColor=#9673A6;"       # актор
NOTE  = "text;html=1;whiteSpace=wrap;align=left;verticalAlign=top;fillColor=#FFF9E6;strokeColor=#E6D878;rounded=1;spacing=6;spacingLeft=8;"
GSLB  = "shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;size=20;fillColor=#D4E1F5;strokeColor=#3A6EA5;"

d = D()
W = 1720

# ---------- верх: клиент ----------
users = d.node(60, 40, 200, 70, "Браузер пользователя<br>(все регионы РФ, 24/7)", USER)

cdn = d.node(340, 40, 260, 70, "CDN + Object Storage<br>статика веб-приложения<br>(ближе к пользователю)", EXT)

gslb = d.node(720, 30, 280, 90, "GSLB / Cloud DNS<br>маршрутизация к ближайшей зоне,<br>health check обеих площадок", GSLB)

# ---------- зона A ----------
za = d.node(40, 200, 760, 560, "", FRAME)
d.node(60, 690, 300, 40, "Зона доступности A", "text;html=1;fontSize=16;fontColor=#3A6EA5;")

albA = d.node(80, 240, 280, 70, "Application Load Balancer<br>L7, health check /health", EXT, )
k8sA = d.node(60, 350, 560, 280, "", K8S)
d.node(80, 600, 380, 30, "Kubernetes cluster A — независимый", "text;html=1;fontSize=12;fontColor=#1A4E8A;")
nsA = d.node(80, 390, 520, 190, "", NSBOX)
d.node(96, 548, 460, 26, "namespace InsureTech", "text;html=1;fontSize=11;fontColor=#8A6D1A;")
coreA = d.node(96, 420, 160, 60, "core-app ×N<br>HPA", POD)
cia   = d.node(272, 420, 140, 60, "client-info ×N", POD)
aggA  = d.node(96, 486, 160, 60, "ins-product-<br>aggregator ×N", POD)
setA  = d.node(272, 486, 140, 60, "ins-comp-<br>settlement ×N", POD)
dbA   = d.node(680, 380, 100, 120, "PostgreSQL<br>Patroni<br>leader", DB)
vmA   = d.node(660, 350, 140, 180, "", FRAME)

# ---------- зона B (зеркально) ----------
zb = d.node(920, 200, 760, 560, "", FRAME)
d.node(940, 690, 300, 40, "Зона доступности B", "text;html=1;fontSize=16;fontColor=#3A6EA5;")
albB = d.node(960, 240, 280, 70, "Application Load Balancer<br>L7, health check /health", EXT)
k8sB = d.node(940, 350, 560, 280, "", K8S)
d.node(960, 600, 380, 30, "Kubernetes cluster B — независимый", "text;html=1;fontSize=12;fontColor=#1A4E8A;")
nsB = d.node(960, 390, 520, 190, "", NSBOX)
d.node(976, 548, 460, 26, "namespace InsureTech", "text;html=1;fontSize=11;fontColor=#8A6D1A;")
coreB = d.node(976, 420, 160, 60, "core-app ×N<br>HPA", POD)
cib   = d.node(1152, 420, 140, 60, "client-info ×N", POD)
aggB  = d.node(976, 486, 160, 60, "ins-product-<br>aggregator ×N", POD)
setB  = d.node(1152, 486, 140, 60, "ins-comp-<br>settlement ×N", POD)
dbB   = d.node(1560, 380, 100, 120, "PostgreSQL<br>Patroni<br>replica", DB)
vmB   = d.node(1540, 350, 140, 180, "", FRAME)

# ---------- бэкапы ----------
s3 = d.node(1140, 820, 420, 90, "Object Storage (S3): pgBackRest — инкрементальные бэкапы + архив WAL<br> каждые 15 минут → RPO ≤ 15 мин", EXT)

# ---------- рёбра ----------
d.edge(users, cdn, "статика")
d.edge(users, gslb, "API / динамика")
d.edge(gslb, albA, "health check ✓", points=[(560, 75)])
d.edge(gslb, albB, "health check ✓", points=[(1160, 75)])
d.edge(albA, nsA, "HTTP")
d.edge(albB, nsB, "HTTP")
d.edge(dbA, dbB, "потоковая репликация (Patroni, авто-failover) → RTO ≤ мин", points=[(760, 340), (1600, 340)])
d.edge(dbA, s3, "бэкапы")
d.edge(dbB, s3, "бэкапы")

# ---------- комментарии ----------
d.node(40, 820, 420, 200,
 "Решения (комментарии)<br>1. Масштабирование: горизонтальное (HPA по CPU/RPS в каждом кластере); вертикальное — только точечно. Активный рост в регионах → несколько зон доступности.<br>2. K8s: НЕЗАВИСИМЫЕ кластеры в каждой зоне. Растянутый кластер требует низкой латентности межзон и рискует split-brain etcd; независимые изолируют отказ зоны, переключение трафика берёт на себя GSLB.<br>3. Фейловер: Active-Active на клиенте — GSLB держит обе зоны в ротации, при отказе зоны выводит её по health check (RTO — минуты ≤ 45 мин).<br>4. БД: Patroni (leader/replica) — авто-failover; бэкапы pgBackRest + WAL в S3 каждые 15 мин (RPO ≤ 15 мин).<br>5. Шардирование БД НЕ требуется: 50 ГБ, нагрузка покрывается репликацией и HPU приложений; шардирование усложнит транзакции без выгоды.", NOTE)

d.node(480, 820, 300, 120,
 "Одинаковое время загрузки в регионах:<br>CDN раздаёт статику из узлов,<br>ближайших к пользователю;<br>GSLB направляет API-трафик<br>в ближайшую зону.", NOTE)

d.node(1690, 30, 200, 200,
 "Обозначения:<br>— пунктир: зона доступности / VM<br>— синий: кластер K8s<br>— жёлтый: namespace<br>— зелёный: поды сервисов<br>— оранжевый цилиндр: PostgreSQL<br>— фиолетовый: пользователь<br>— синий_hex: GSLB", NOTE)

xml = f'''<mxfile host="app.diagrams.net">
  <diagram id="task1-tobe" name="InureTech_технологическая архитектура_to-be">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" pageScale="1" pageWidth="1800" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        {"".join(d.cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

out = "/Users/xo/dev/Yandex.Praktikum/System Design/architecture-insuretech/Task1/InureTech_технологическая архитектура_to-be.drawio"
open(out, "w").write(xml)
print("written", out, len(xml))
