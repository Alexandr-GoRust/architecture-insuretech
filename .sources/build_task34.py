#!/usr/bin/env python3
"""Генератор draw.io: Task3 (C4 Event-Driven) и Task4 (C4 + ОСАГО)."""
import html

def esc(s): return html.escape(s, quote=True)

class D:
    def __init__(self):
        self.cells = []; self.id = 1
    def nid(self):
        self.id += 1; return f"n{self.id}"
    def node(self, x, y, w, h, label, style, parent="1"):
        i = self.nid()
        self.cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{style}" vertex="1" parent="{parent}"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return i
    def edge(self, src, dst, label="", color="#5B7DB1", dashed=0, points=None):
        i = self.nid()
        st = f"edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor={color};strokeWidth=1.6;dashed={dashed};fontSize=10;"
        pts = ""
        if points:
            pts = '<Array as="points">' + "".join(f'<mxPoint x="{p[0]}" y="{p[1]}"/>' for p in points) + '</Array>'
        self.cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{st}" edge="1" parent="1" source="{src}" target="{dst}"><mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>')
        return i

SYS  = "rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#666666;arcSize=10;"     # внешняя система
CONT = "rounded=1;whiteSpace=wrap;html=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;arcSize=8;"       # контейнер
DB   = "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#FFE6CC;strokeColor=#D79B00;"
PERSON = "shape=ellipse;whiteSpace=wrap;html=1;fillColor=#E1D5E7;strokeColor=#9673A6;"
KAFKA = "shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;size=25;fillColor=#F8CECC;strokeColor=#B85450;"
BOUND = "rounded=1;whiteSpace=wrap;html=1;fillColor=none;dashed=1;arcSize=4;"
NOTE  = "text;html=1;whiteSpace=wrap;align=left;verticalAlign=top;fillColor=#FFF9E6;strokeColor=#E6D878;rounded=1;spacing=6;spacingLeft=8;"
EV = "#B85450"   # события (красный)
REST = "#5B7DB1" # REST (синий)
TCP = "#D79B00"  # БД (оранжевый)

def base(d, osago=False):
    """Общие элементы C4 InsureTech; возвращает dict id."""
    ids = {}
    ids['bound'] = d.node(360, 30, 1180, 960, "", BOUND)
    d.node(380, 935, 300, 30, "InsureTech [System]", "text;html=1;fontSize=15;fontColor=#666666;")
    ids['client'] = d.node(80, 360, 160, 90, "Клиент<br>[Person]", PERSON)
    ids['web'] = d.node(420, 330, 210, 110, "<b>InsureTech Web</b><br>[Container: JavaScript,<br>React]<br>веб-приложение", CONT)
    ids['core'] = d.node(760, 330, 240, 130, "<b>core-app</b> [Container:<br>Kotlin, SpringBoot]<br>продукты, заявки, ОСАГО", CONT)
    ids['ci'] = d.node(430, 560, 210, 100, "<b>client-info</b><br>[Container: Kotlin,<br>SpringBoot]<br>клиентские данные", CONT)
    ids['agg'] = d.node(760, 660, 250, 110, "<b>ins-product-aggregator</b><br>[Container: Kotlin, SpringBoot]<br>интеграция со СК", CONT)
    ids['set'] = d.node(1180, 660, 240, 110, "<b>ins-comp-settlement</b><br>[Container: Kotlin,<br>SpringBoot]<br>взаиморасчёты", CONT)
    ids['coredb'] = d.node(800, 480, 110, 80, "<b>core-db</b><br>[PostgreSQL]", DB)
    ids['cidb'] = d.node(700, 560, 100, 80, "<b>client-db</b><br>[PostgreSQL]", DB)
    ids['setdb'] = d.node(1310, 795, 110, 80, "<b>settlement-db</b><br>[PostgreSQL]", DB)
    ids['pay'] = d.node(80, 60, 220, 100, "<b>Платёжный сервис</b><br>[Software System]<br>оплата страховок", SYS)
    ids['part'] = d.node(420, 60, 230, 100, "<b>Системы партнёров</b><br>[Software System]<br>страховые услуги в своих<br>продуктах", SYS)
    ids['ins'] = d.node(1100, 60, 260, 100, "<b>Системы страховых</b><br><b>компаний (10)</b><br>[Software System]<br>API тарифов / ОСАГО", SYS)
    ids['kafka'] = d.node(1080, 420, 300, 110, "<b>Kafka</b> [Event Streaming]<br>топики: insurance-products,<br>policy-issued" + (",<br>osago-offers" if osago else ""), KAFKA)
    # постоянные связи
    d.edge(ids['client'], ids['web'], "HTTPS")
    d.edge(ids['web'], ids['pay'], "оплата (redirect) [HTTP]", REST, points=[(525, 210), (190, 210)])
    d.edge(ids['web'], ids['ci'], "данные клиента [REST]", REST)
    d.edge(ids['web'], ids['core'], "тарифы, заявки [REST]", REST)
    d.edge(ids['core'], ids['ci'], "данные клиента [REST]", REST)
    d.edge(ids['core'], ids['coredb'], "TCP", TCP)
    d.edge(ids['ci'], ids['cidb'], "TCP", TCP)
    d.edge(ids['set'], ids['setdb'], "TCP", TCP)
    d.edge(ids['core'], ids['pay'], "оплата [HTTP]", REST, points=[(880, 260), (190, 260)])
    d.edge(ids['part'], ids['core'], "оформление страховок [REST]", REST, points=[(535, 305), (760, 305)])
    d.edge(ids['agg'], ids['ins'], "тарифы [REST/SOAP/GraphQL]", REST, points=[(885, 620), (1230, 240), (1230, 160)])
    d.edge(ids['set'], ids['ins'], "взаиморасчёты [REST/SOAP/GraphQL]", REST, points=[(1420, 620), (1420, 160)])
    # event-streaming (Task3 суть)
    d.edge(ids['agg'], ids['kafka'], "publish: insurance-products<br>(Transactional Outbox + Debezium CDC)", EV)
    d.edge(ids['kafka'], ids['core'], "subscribe: insurance-products<br>(актуализация реплики тарифов)", EV)
    d.edge(ids['core'], ids['kafka'], "publish: policy-issued<br>(Transactional Outbox + Debezium CDC)", EV)
    d.edge(ids['kafka'], ids['set'], "subscribe: policy-issued<br>(накопление реестра)", EV)
    return ids

# ---------------- Task3 ----------------
d3 = D()
ids = base(d3, osago=False)
d3.node(40, 620, 300, 290,
 "Изменения as-is → to-be:<br>1. REST-polling тарифов (core-app 15 мин, settlement раз в сутки) → подписка на поток insurance-products: реплики актуальны секунды, RPS на СК не растёт с числом потребителей.<br>2. Суточная REST-выгрузка оформленных страховок (settlement→core-app) → поток policy-issued: без ночных пиков и таймаутов на больших выгрузках.<br>3. Transactional Outbox + CDC (Debezium): событие и бизнес-изменение — одна транзакция, публикация без потерь (нет двойной записи).<br>4. Декомпозиция сервисов не менялась — изменён способ доставки данных.", NOTE)
xml3 = f'''<mxfile host="app.diagrams.net"><diagram id="task3" name="InsureTech C4 Event-Driven">
<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" pageScale="1" pageWidth="1700" pageHeight="1000" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>{"".join(d3.cells)}</root></mxGraphModel></diagram></mxfile>'''
open("/Users/xo/dev/Yandex.Praktikum/System Design/architecture-insuretech/Task3/InsureTech_C4_Event-Driven.drawio", "w").write(xml3)

# ---------------- Task4 (osago поверх Task3) ----------------
d4 = D()
ids = base(d4, osago=True)
osago = d4.node(760, 800, 250, 120, "<b>osago-aggregator</b><br>[Container: Kotlin, SpringBoot]<br>заявки ОСАГО в СК,<br>опрос решений (≤60 c)", CONT)
osagodb = d.node if False else d4.node(1060, 820, 110, 80, "<b>osago-db</b><br>[PostgreSQL]<br>заявки/статусы", DB)
d4.edge(ids['core'], osago, "создание заявки ОСАГО [REST]<br>[Timeout][Retry][Circuit Breaker]", REST, points=[(880, 460) if False else (880, 800)])
d4.edge(osago, ids['kafka'], "publish: osago-offers<br>(предложения по мере ответа СК)", EV)
d4.edge(ids['kafka'], ids['core'], "subscribe: osago-offers", EV)
d4.edge(osago, ids['ins'], "заявка / опрос решения [REST]<br>[Timeout 60s][Retry][Circuit Breaker][Rate Limiting]", REST, points=[(1010, 780), (1330, 780), (1330, 200)])
d4.edge(osago, osagodb, "TCP", TCP)
d4.edge(ids['web'], ids['core'], "WS: поток предложений ОСАГО<br>(по мере поступления) [WebSocket]", "#82B366", points=[(640, 300), (640, 300)])
d4.node(40, 620, 300, 400,
 "Решения Task4:<br>1. osago-aggregator — свой API + СВОЯ БД (osago-db): заявки и статусы живут у него, опрос решений (до 60 c) не зависит от сессии core-app, переживает рестарты.<br>2. API core-app→osago: REST (команда «создать заявку», точка-точка); результаты — события osago-offers в Kafka (по мере ответа каждой СК).<br>3. API веб→core-app: REST (создание заявки) + WebSocket-канал потока предложений — Server push, отображение сразу по приходу оффера (кейс урока front-to-back).<br>4. Паттерны (бейджи на стрелках): к СК — Timeout 60s, Retry, Circuit Breaker, Rate Limiting; core-app→osago — Timeout/Retry/CB; веб→core-app — Rate Limiting (2500 польз.).<br>5. Множественные экземпляры: офферы публикуются в Kafka → их видят ВСЕ экземпляры core-app; WebSocket конкретного пользователя закреплён за его экземпляром — решение от количества экземпляров не зависит.", NOTE)
xml4 = f'''<mxfile host="app.diagrams.net"><diagram id="task4" name="InsureTech C4 + ОСАГО">
<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" pageScale="1" pageWidth="1700" pageHeight="1000" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>{"".join(d4.cells)}</root></mxGraphModel></diagram></mxfile>'''
open("/Users/xo/dev/Yandex.Praktikum/System Design/architecture-insuretech/Task4/InsureTech_C4_OSAGO.drawio", "w").write(xml4)
print("task3/task4 written")
