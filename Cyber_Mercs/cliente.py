import sys
import os

# Forzar UTF-8 en Windows para evitar errores con caracteres Unicode en consola
if sys.platform == "win32":
    os.environ.setdefault("PYTHONUTF8", "1")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import requests
import time
import random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

BASE_URL = "http://localhost:8000"
API_KEY = "zaun-key-2026"
HEADERS = {"X-API-KEY": API_KEY}
console = Console()

def animacion_hackeo():
    with Progress(
        SpinnerColumn(spinner_name="dots2", style="green"),
        TextColumn("[bold bright_green]{task.description}"),
        BarColumn(bar_width=40, style="dark_green", complete_style="bright_green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Bypasseando firewalls corporativos...", total=100)
        while not progress.finished:
            progress.update(task, advance=random.randint(3, 10))
            time.sleep(0.03)
    console.print("[bold bright_green]✓ ACCESO CONCEDIDO AL MAINFRAME.[/bold bright_green]\n")

def separador(titulo: str):
    console.rule(f"[bold bright_green]■ {titulo} ■[/bold bright_green]", style="green")
    time.sleep(0.5)

if __name__ == "__main__":
    console.clear()
    console.print(Panel.fit("[bold bright_green]/// CYBER-MERCS TERMINAL - SISTEMA ZAUN ///[/bold bright_green]", border_style="green"))
    animacion_hackeo()

    # FASE 1
    separador("FASE 1 - VERIFICAR CONEXIÓN")
    try:
        r = requests.get(f"{BASE_URL}/")
        console.print(f"Status: [bold bright_green]{r.status_code}[/bold bright_green] - Servidor Activo")
        requests.delete(f"{BASE_URL}/reset", headers=HEADERS)
        console.print("[bold green]Datos de simulaciones anteriores purgados.[/bold green]")
    except Exception as e:
        console.print("[bold red]❌ Error de conexión. El mainframe de uvicorn no responde.[/bold red]")
        exit(1)

    # FASE 2: LOS JUGADORES
    separador("FASE 2 - RECLUTAMIENTO DE MERCENARIOS (JUGADORES)")
    jugadores = [
        {"alias": "Jinx", "clase_nombre": "hacker", "hp": 100, "creditos": 0},
        {"alias": "Ekko", "clase_nombre": "hacker", "hp": 120, "creditos": 500},
        {"alias": "Vi", "clase_nombre": "tanque", "hp": 200, "creditos": 100},
        {"alias": "Caitlyn", "clase_nombre": "sniper", "hp": 110, "creditos": 1000},
        {"alias": "Silco", "clase_nombre": "fixer", "hp": 90, "creditos": 5000},
    ]
    for jug in jugadores:
        r = requests.post(f"{BASE_URL}/mercs/", json=jug, headers=HEADERS)
        if r.status_code in [200, 201]:
            console.print(f"[bright_green]>[/bright_green] Perfil de [bold cyan]{jug['alias']}[/bold cyan] ([italic]{jug['clase_nombre']}[/italic]) cargado en la red.")
        else:
            # Consultar la DB para mostrar la clase del merc existente
            r_merc = requests.get(f"{BASE_URL}/mercs/")
            clase = jug['clase_nombre']
            for m in r_merc.json():
                if m['alias'] == jug['alias']:
                    clase = m['clase_nombre']
                    break
            console.print(f"[bright_green]>[/bright_green] Perfil de [bold cyan]{jug['alias']}[/bold cyan] ([italic]{clase}[/italic]) cargado en la red.")
        time.sleep(0.1)

    # FASE 3: CONTRATOS
    separador("FASE 3 - CONTRATOS DEL MERCADO NEGRO")
    contratos = [
        # FUERTE: clase ideal para el contrato
        {"titulo": "Atraco al Banco Piltover", "tipo_contrato": "asalto", "mercenario_asignado": "Vi", "dano_estimado": 50, "pago_base": 1000},
        {"titulo": "Infiltración Hextech", "tipo_contrato": "infiltracion", "mercenario_asignado": "Jinx", "dano_estimado": 40, "pago_base": 1500},
        {"titulo": "Robar planos del Z-Drive", "tipo_contrato": "hackeo", "mercenario_asignado": "Ekko", "dano_estimado": 60, "pago_base": 2000},
        {"titulo": "Sabotaje a la Planta Shimmer", "tipo_contrato": "sabotaje", "mercenario_asignado": "Silco", "dano_estimado": 35, "pago_base": 1800},
        # DÉBIL: clase en desventaja (alto riesgo, alto drama)
        {"titulo": "Asesinato Corporativo", "tipo_contrato": "asalto", "mercenario_asignado": "Caitlyn", "dano_estimado": 80, "pago_base": 2500},
        {"titulo": "Hackear el Mainframe de Piltover", "tipo_contrato": "hackeo", "mercenario_asignado": "Vi", "dano_estimado": 70, "pago_base": 3000},
        # NEUTRAL: suerte pura
        {"titulo": "Extorsión al Consejo de Zaun", "tipo_contrato": "combate", "mercenario_asignado": "Ekko", "dano_estimado": 55, "pago_base": 2200},
        {"titulo": "Cacería en los Muelles", "tipo_contrato": "combate", "mercenario_asignado": "Silco", "dano_estimado": 65, "pago_base": 2800},
    ]
    ids_contratos = []
    for c in contratos:
        r = requests.post(f"{BASE_URL}/contratos/", json=c, headers=HEADERS)
        data = r.json()
        ids_contratos.append((data.get('id', 0), c['titulo'], c['mercenario_asignado']))
        console.print(f"📄 Contrato encriptado: [bold magenta]{c['titulo']}[/bold magenta] -> Asignado a: [cyan]{c['mercenario_asignado']}[/cyan]")
        time.sleep(0.1)

    # FASE 4: EJECUCIÓN (CON ECONOMÍA CRYPTO DINÁMICA)
    separador("FASE 4 - EJECUCIÓN Y ECONOMÍA CRYPTO")
    # Colores de borde por tipo de evento
    EVENTO_ESTILO = {
        "Jackpot Corporativo":      ("bright_yellow", "🎰"),
        "Golpe de Suerte":          ("bright_green", "🍀"),
        "Infiltración Fantasma":    ("bright_green", "👻"),
        "Operación Limpia":         ("green", "✅"),
        "Resistencia Inesperada":   ("yellow", "⚠️"),
        "Emboscada Corporativa":    ("red", "🔥"),
        "Desastre Absoluto":        ("bright_red", "💀"),
    }

    # (variante_vivo, variante_muerto) — la narrativa cambia según si sobrevivió o no
    NARRATIVA = {
        "Jackpot Corporativo": (
            "El objetivo estaba vacío. Sin guardias, sin alarmas. Botín completo y salida limpia por la azotea.",
            "El objetivo estaba vacío... pero una bomba trampa oculta detonó en la salida. No hubo tiempo de reaccionar.",
        ),
        "Golpe de Suerte": (
            "Un contacto anónimo filtró los códigos minutos antes. Entrada y salida como un fantasma.",
            "Los códigos filtrados eran una trampa. La puerta se selló y el gas nervioso hizo el resto.",
        ),
        "Infiltración Fantasma": (
            "Las cámaras estaban en loop, los guardias dormidos. Nadie supo que estuvo ahí hasta la mañana siguiente.",
            "Las cámaras estaban en loop, pero el último guardia no dormía. Un disparo silencioso en la oscuridad.",
        ),
        "Operación Limpia": (
            "Sin sorpresas. El plan se ejecutó tal como fue diseñado. Profesionalismo de manual.",
            "El plan era sólido, pero el cuerpo no aguantó. Las heridas acumuladas cobraron su precio final.",
        ),
        "Resistencia Inesperada": (
            "Refuerzos corporativos aparecieron de la nada. Hubo que improvisar una salida entre balas y humo.",
            "Los refuerzos eran demasiados. Luchó hasta el último cartucho, pero las balas se acabaron primero.",
        ),
        "Emboscada Corporativa": (
            "Era una trampa. Francotiradores en los techos y drones rastreadores. Pero la experiencia ganó.",
            "Era una trampa. Francotiradores en los techos, drones cerrando el perímetro. No hubo escapatoria.",
        ),
        "Desastre Absoluto": (
            "Todo salió mal. Traición interna y explosivos prematuros. Apenas logró arrastrarse fuera del edificio.",
            "Todo salió mal. Traición interna, explosivos prematuros. El cuerpo fue hallado entre los escombros.",
        ),
    }

    INTRO_CLASE = {
        "hacker": "{alias} conecta su neural-link al sistema enemigo y empieza a descifrar firewalls...",
        "tanque": "{alias} carga su armamento pesado, ajusta la armadura subdérmica y avanza...",
        "sniper": "{alias} toma posición en las alturas, calibra la mira y espera el momento justo...",
        "fixer": "{alias} activa su red de contactos en el bajo mundo y coordina la operación...",
        "novato": "{alias} respira hondo, revisa su equipo básico y cruza hacia territorio hostil...",
    }

    # Lookup de clase por alias para los intros
    clase_por_alias = {j["alias"]: j["clase_nombre"] for j in jugadores}

    # Estado real de HP desde la DB (post-registro, antes de misiones)
    r_estado = requests.get(f"{BASE_URL}/mercs/")
    hp_tracker = {m["alias"]: m["hp"] for m in r_estado.json()}
    mercs_muertos = set()

    for cid, titulo, merc_alias in ids_contratos:
        clase_merc = clase_por_alias.get(merc_alias, "novato")
        hp_antes = hp_tracker.get(merc_alias, 0)

        # Si el mercenario ya murió, la misión se aborta
        if merc_alias in mercs_muertos:
            console.print(f"\n[bold cyan]{merc_alias}[/bold cyan] [dim]({clase_merc})[/dim] [red]— HP: 0 (FLATLINE)[/red]")
            msg = f"💀 [bold red]MISIÓN ABORTADA[/bold red]\n"
            msg += f"[italic dim]{merc_alias} fue eliminado en una misión anterior. No hay quien ejecute este contrato.[/italic dim]\n"
            msg += f"[italic gray]Estado del contrato: FALLIDA.[/italic gray]"
            console.print(Panel(msg, title=f"Resultado: {titulo}", border_style="dim red"))
            requests.post(f"{BASE_URL}/contratos/{cid}/fallar", headers=HEADERS)
            continue

        # Intro narrativo con HP actual
        intro = INTRO_CLASE.get(clase_merc, INTRO_CLASE["novato"]).format(alias=merc_alias)
        console.print(f"\n[bold cyan]{merc_alias}[/bold cyan] [dim]({clase_merc})[/dim] — HP: [bold green]{hp_antes}[/bold green]")
        console.print(f"[italic bright_green]{intro}[/italic bright_green]")

        with console.status(f"[bold bright_green]  Ejecutando...[/bold bright_green]", spinner="bouncingBar"):
            time.sleep(0.5)
            r = requests.post(f"{BASE_URL}/contratos/{cid}/ejecutar", headers=HEADERS)
            data = r.json()

        if r.status_code == 200:
            evento = data.get("evento", "Operación Limpia")
            estilo, icono = EVENTO_ESTILO.get(evento, ("green", "✅"))
            murio = data.get("estado_vital") == "muerto"
            narr_tuple = NARRATIVA.get(evento, ("", ""))
            narr = narr_tuple[1] if murio else narr_tuple[0]

            if murio:
                hp_gastado = data.get("hp_gastado", "LETAL")
                msg = f"{icono} [bold red]{evento}[/bold red]\n"
                msg += f"[italic dim]{narr}[/italic dim]\n"
                msg += f"🩸 Daño recibido: {hp_gastado} HP. Salud restante: 0 HP\n"
                msg += f"💀 [bold red]FLATLINE — Mercenario eliminado del sistema.[/bold red]"
                console.print(Panel(msg, title=f"Resultado: {titulo}", border_style="bright_red"))
            elif data.get("exito_mision") is False:
                hp_gastado = data.get("hp_gastado", 0)
                hp_actual = data.get("hp_actual", 0)
                msg = f"{icono} [bold red]{evento}[/bold red]\n"
                msg += f"[italic dim]{narr}[/italic dim]\n"
                msg += f"🩸 Daño recibido: {hp_gastado} HP. Salud restante: {hp_actual} HP\n"
                msg += f"[italic gray]Sin pago. Misión fracasada.[/italic gray]"
                console.print(Panel(msg, title=f"Resultado: {titulo}", border_style="bright_red"))
            else:
                pago = data.get("pago_recibido", 0)
                multiplicador = data.get("multiplicador_mercado", 1.0)
                mult_pago = data.get("multiplicador_pago_evento", 1.0)
                hp_gastado = data.get("hp_gastado", 0)
                hp_actual = data.get("hp_actual", "?")
                implante = data.get("implante_obtenido")

                msg = f"{icono} [bold]{evento}[/bold]\n"
                msg += f"[italic dim]{narr}[/italic dim]\n"
                if hp_gastado > 0:
                    msg += f"🩸 Daño recibido: {hp_gastado} HP. Salud restante: {hp_actual} HP\n"
                else:
                    msg += f"🛡️ Sin daño recibido. Salud: {hp_actual} HP\n"
                pago_str = f"💰 Pago: [bold yellow]{pago} ₿[/bold yellow] (BTC x{multiplicador}"
                if mult_pago != 1.0:
                    pago_str += f", evento x{mult_pago}"
                pago_str += ")\n"
                msg += pago_str
                if implante:
                    msg += f"🦾 Loot Cibernético: [bold cyan]{implante}[/bold cyan]"

                console.print(Panel(msg, title=f"Resultado: {titulo}", border_style=estilo))

            # --- Actualizar tracker de HP y muertos ---
            if data.get("estado_vital") == "muerto":
                mercs_muertos.add(merc_alias)
                hp_tracker[merc_alias] = 0
            elif "hp_actual" in data:
                hp_tracker[merc_alias] = data["hp_actual"]

        else:
            console.print(Panel(f"💀 [bold red]FALLO OPERATIVO:[/bold red] {data}", title=titulo, border_style="red"))

    # FASE 5: MENSAJERÍA CORPORATIVA
    separador("FASE 5 - INTERCEPCIÓN DE RED")
    mensajes_corporativos = [
        {"remitente": "Silco", "destinatario": "Ekko", "contenido": "Ekko, necesito los datos del banco antes de medianoche. Sin excusas."},
        {"remitente": "Ekko", "destinatario": "Silco", "contenido": "Los datos están encriptados. Dame 2 horas más o consigue a otro hacker."},
        {"remitente": "Caitlyn", "destinatario": "Vi", "contenido": "Buen trabajo en el distrito. Te debo una ronda de munición."},
        {"remitente": "Ekko", "destinatario": "Jinx", "contenido": "Vi lo que hiciste en el laboratorio Hextech. Eso fue demasiado, incluso para ti."},
        {"remitente": "Caitlyn", "destinatario": "Jinx", "contenido": "Tengo tu expediente encima de mi escritorio. La próxima vez no fallaré."},
    ]
    for msg_obj in mensajes_corporativos:
        requests.post(f"{BASE_URL}/comunicaciones/", json=msg_obj, headers=HEADERS)
        time.sleep(0.1)
    
    r = requests.get(f"{BASE_URL}/comunicaciones/Jinx")
    if r.status_code == 200 and r.json():
        console.print(f"📩 [bold cyan]Mensajes interceptados para Jinx:[/bold cyan]")
        for msg in r.json():
            console.print(f"> [bold red]{msg['remitente']}[/bold red]: [italic grey84]{msg['contenido']}[/italic grey84]")

    # FASE 6: ESTADO FINAL
    separador("FASE 6 - REGISTRO DE MERCENARIOS")
    r = requests.get(f"{BASE_URL}/mercs/")
    mercs_db = r.json()
    
    table = Table(title="/// BASE DE DATOS CORPORATIVA ///", header_style="bold bright_green")
    table.add_column("Alias", style="cyan", no_wrap=True)
    table.add_column("Clase", style="magenta")
    table.add_column("Estado", style="white")
    table.add_column("Salud (HP)", justify="left", style="green")
    table.add_column("Créditos (₿)", justify="right", style="yellow")
    table.add_column("Implantes", style="blue")

    for m in mercs_db:
        r_inv = requests.get(f"{BASE_URL}/implantes/{m['alias']}")
        items = r_inv.json()
        items_str = ", ".join([i['nombre_implante'] for i in items]) if items else "[italic gray]Ninguno[/italic gray]"
        
        hp = m['hp']
        estado = m.get('estado_vital', 'vivo').upper()
        creditos = m.get('creditos', 0)
        
        if estado == "MUERTO":
            estado_str = "[bold red]💀 FLATLINE[/bold red]"
            hp_str = "[red]  0 HP ░░░░░░░░░░ OFFLINE[/red]"
        else:
            estado_str = "[bold bright_green]✅ ACTIVO[/bold bright_green]"
            bloques = min(10, max(0, hp // 20))
            barra = "█" * bloques + "░" * (10 - bloques)
            hp_str = f"[green]{hp:>3} HP {barra}[/green]"

        table.add_row(m['alias'], m['clase_nombre'], estado_str, hp_str, f"{creditos:,} ₿", items_str)

    console.print(table, justify="center")
    separador("DESCONEXIÓN DEL MAINFRAME EXITOSA")
