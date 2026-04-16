# Reto de Consolidacion - Agencia del Olimpo
# Doris Mosquera Lozano - doris.mosquera@sofka.com.co
# DMosqueraLSofka

# cliente.py -- Script que consume la API por HTTP
# Ejecuta un flujo completo sin intervencion manual.
# El servidor debe estar corriendo: uvicorn main:app --reload

import requests

BASE_URL = "http://localhost:8000"
API_KEY = "olympus-key-2026"
HEADERS = {"X-API-KEY": API_KEY}


def separador(titulo: str):
    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}")


if __name__ == "__main__":

    # ==========================================
    # PASO 1: Verificar que el servidor esta vivo
    # ==========================================
    separador("Paso 1: Verificar servidor")
    r = requests.get(f"{BASE_URL}/")
    print(f"  Status: {r.status_code}")
    print(f"  Respuesta: {r.json()}")

    # ==========================================
    # PASO 2: Crear 5 agentes del Olimpo
    # ==========================================
    separador("Paso 2: Crear agentes del Olimpo")
    agentes = [
        {"nombre": "Zeus", "rol": "admin", "energia": 200},
        {"nombre": "Atenea", "rol": "estratega", "energia": 150},
        {"nombre": "Hermes", "rol": "mensajero", "energia": 120},
        {"nombre": "Apolo", "rol": "diplomatico", "energia": 130},
        {"nombre": "Artemisa", "rol": "cazadora", "energia": 140},
    ]
    for agente in agentes:
        r = requests.post(f"{BASE_URL}/agentes/", json=agente, headers=HEADERS)
        print(f"  {agente['nombre']} ({agente['rol']}): {r.json().get('mensaje', r.json())}")

    # ==========================================
    # PASO 2b: Intentar crear sin API key (debe dar 401)
    # ==========================================
    separador("Paso 2b: Intentar sin API key (espero 401)")
    r = requests.post(f"{BASE_URL}/agentes/", json={"nombre": "Intruso", "rol": "hacker", "energia": 999})
    print(f"  Status: {r.status_code}")
    print(f"  Respuesta: {r.json()}")

    # ==========================================
    # PASO 3: Crear 7 misiones epicas
    # ==========================================
    separador("Paso 3: Crear misiones del Olimpo")
    misiones = [
        {
            "titulo": "Defender el Monte Olimpo",
            "descripcion": "Proteger la entrada del Olimpo contra los Titanes",
            "agente_asignado": "Zeus",
            "energia_requerida": 40,
            "prioridad": "alta",
            "recompensa": 20
        },
        {
            "titulo": "Llevar mensaje a Hades",
            "descripcion": "Entregar un pergamino sellado al inframundo",
            "agente_asignado": "Hermes",
            "energia_requerida": 30,
            "prioridad": "media",
            "recompensa": 15
        },
        {
            "titulo": "Planificar estrategia de guerra",
            "descripcion": "Disenar el plan de batalla contra los Titanes",
            "agente_asignado": "Atenea",
            "energia_requerida": 50,
            "prioridad": "alta",
            "recompensa": 25
        },
        {
            "titulo": "Robar el fuego de Prometeo",
            "descripcion": "Recuperar el fuego sagrado de la forja de Hefesto",
            "agente_asignado": "Hermes",
            "energia_requerida": 35,
            "prioridad": "alta",
            "recompensa": 30
        },
        {
            "titulo": "Negociar con Poseidon",
            "descripcion": "Convencer al dios del mar de unirse a la causa del Olimpo",
            "agente_asignado": "Zeus",
            "energia_requerida": 60,
            "prioridad": "media",
            "recompensa": 10
        },
        {
            "titulo": "Cazar al Leon de Nemea",
            "descripcion": "Rastrear y neutralizar a la bestia que aterroriza las aldeas",
            "agente_asignado": "Artemisa",
            "energia_requerida": 45,
            "prioridad": "alta",
            "recompensa": 35
        },
        {
            "titulo": "Negociar tregua con Cronos",
            "descripcion": "Enviar un diplomatico al campamento de los Titanes para negociar la paz",
            "agente_asignado": "Apolo",
            "energia_requerida": 25,
            "prioridad": "baja",
            "recompensa": 50
        },
    ]
    ids_misiones = []
    for mision in misiones:
        r = requests.post(f"{BASE_URL}/misiones/", json=mision, headers=HEADERS)
        data = r.json()
        print(f"  #{data.get('id', '?')} {mision['titulo']} -> {mision['agente_asignado']} [{mision['prioridad']}]")
        if "id" in data:
            ids_misiones.append(data["id"])

    # ==========================================
    # PASO 4: Completar misiones exitosas
    # ==========================================
    separador("Paso 4: Completar misiones exitosas")
    # Completar misiones 1 (Zeus-Olimpo), 2 (Hermes-Hades), 4 (Hermes-Prometeo), 6 (Artemisa-Leon)
    misiones_a_completar = [ids_misiones[0], ids_misiones[1], ids_misiones[3], ids_misiones[5]]
    for mid in misiones_a_completar:
        r = requests.post(f"{BASE_URL}/misiones/{mid}/completar", headers=HEADERS)
        data = r.json()
        if r.status_code == 200:
            print(f"  Mision #{mid}: COMPLETADA por {data.get('mensaje', '')} | Energia: {data.get('energia_actual', '?')} | Tipo: {data.get('tipo_agente', '?')}")
        else:
            print(f"  Mision #{mid}: {data}")

    # ==========================================
    # PASO 4b: Fallar mision de Apolo (se paso al bando de Cronos!)
    # ==========================================
    separador("Paso 4b: MISION FALLIDA - Apolo traiciona al Olimpo!")
    print("  Apolo fue enviado a negociar la tregua con Cronos...")
    print("  Pero el bando de los Titanes lo convencio de unirse a sus filas!")
    mision_apolo = ids_misiones[6]  # Negociar tregua con Cronos
    r = requests.post(f"{BASE_URL}/misiones/{mision_apolo}/fallar", headers=HEADERS)
    print(f"  Mision #{mision_apolo}: {r.json()}")
    print("  Zeus se entera de la traicion... La agencia registra la mision como FALLIDA.")

    # ==========================================
    # PASO 5: Briefings de los agentes
    # ==========================================
    separador("Paso 5: Briefings de la agencia")
    for nombre in ["Zeus", "Atenea", "Artemisa"]:
        r = requests.get(f"{BASE_URL}/briefing/{nombre}")
        briefing = r.json()
        agente_info = briefing['agente']
        resumen = briefing['resumen_misiones']
        codigo = briefing['codigo_de_confusion']
        print(f"\n  --- Briefing de {nombre} ({agente_info['tipo']}) ---")
        print(f"  Energia: {agente_info['energia']} | Rol: {agente_info['rol']}")
        print(f"  Misiones: {resumen['total']} total | {resumen['completadas']} completadas | {resumen['pendientes']} pendientes | {resumen.get('fallidas', 0)} fallidas")
        print(f"  Codigo de confusion: {codigo['mensaje'][:80]}...")
        print(f"  Proposito: {codigo['proposito'][:60]}...")

    # ==========================================
    # PASO 6: Mensajes entre agentes
    # ==========================================
    separador("Paso 6: Mensajes entre agentes")
    mensajes = [
        {"remitente": "Zeus", "destinatario": "Atenea", "contenido": "Necesito el plan de batalla para manana."},
        {"remitente": "Atenea", "destinatario": "Zeus", "contenido": "Lo tendre listo al amanecer, padre."},
        {"remitente": "Hermes", "destinatario": "Zeus", "contenido": "Hades recibio el pergamino."},
        {"remitente": "Zeus", "destinatario": "Hermes", "contenido": "Excelente trabajo, mensajero."},
        {"remitente": "Atenea", "destinatario": "Hermes", "contenido": "Lleva estos planos a la forja de Hefesto."},
        {"remitente": "Zeus", "destinatario": "Artemisa", "contenido": "Bien hecho con el leon. Eres la mejor cazadora."},
        {"remitente": "Artemisa", "destinatario": "Zeus", "contenido": "Gracias padre. El leon ya no es amenaza."},
        {"remitente": "Zeus", "destinatario": "Atenea", "contenido": "Apolo nos traiciono. Ajusta la estrategia."},
    ]
    for msg in mensajes:
        r = requests.post(f"{BASE_URL}/mensajes/", json=msg, headers=HEADERS)
        print(f"  {msg['remitente']} -> {msg['destinatario']}: enviado")

    # Leer bandeja de Zeus
    print()
    r = requests.get(f"{BASE_URL}/mensajes/Zeus")
    bandeja = r.json()
    print(f"  Bandeja de Zeus ({len(bandeja)} mensajes):")
    for msg in bandeja:
        print(f"    [{msg['timestamp'][:19]}] {msg['remitente']}: {msg['contenido']}")

    # ==========================================
    # PASO 7: Estado final de la agencia
    # ==========================================
    separador("Paso 7: Estado final de la Agencia del Olimpo")
    r = requests.get(f"{BASE_URL}/agentes/")
    print("  AGENTES:")
    for a in r.json():
        print(f"    {a['nombre']:12} | Rol: {a['rol']:12} | Energia: {a['energia']}")

    print("\n  MISIONES POR AGENTE:")
    for nombre in ["Zeus", "Atenea", "Hermes", "Apolo", "Artemisa"]:
        r = requests.get(f"{BASE_URL}/agente/{nombre}/misiones")
        misiones_a = r.json()
        if misiones_a:
            print(f"\n    {nombre}:")
            for m in misiones_a:
                estado_emoji = {"completada": "[OK]", "pendiente": "[..]", "fallida": "[XX]"}.get(m['estado'], "[??]")
                print(f"      {estado_emoji} #{m['id']} {m['titulo']} (prioridad: {m['prioridad']}, recompensa: {m['recompensa']})")

    separador("Flujo completo finalizado exitosamente")
