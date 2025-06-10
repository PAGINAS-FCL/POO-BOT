import os
from utilidades.json_utils import cargar_json, guardar_json

RUTA_MODULOS = "modulos/modulos.json"
RUTA_PROGRESO = "progreso"
RUTA_DATA = "data/data.json"

modulos = cargar_json(RUTA_MODULOS)

usuarios_codigo = {}  # Memoria temporal para mapear usuario_id a código

def ruta_progreso(usuario_id):
    return f"{RUTA_PROGRESO}/usuario_{usuario_id}.json"

def registrar_en_data_json(codigo, modulo):
    data = cargar_json(RUTA_DATA)
    if not isinstance(data, dict):
        data = {}
    data[codigo] = {"modulo_actual": modulo}
    guardar_json(RUTA_DATA, data)

def procesar_entrada_usuario(usuario_id, entrada):
    entrada = entrada.strip()
    ruta = ruta_progreso(usuario_id)

    if not os.path.exists(ruta):
        if entrada.lower().startswith("codigo:"):
            codigo = entrada.split(":", 1)[1].strip()
            usuarios_codigo[usuario_id] = codigo
            guardar_json(ruta, {"modulo": 0, "etapa": "inicio", "indice_pregunta": 0, "codigo": codigo})
            registrar_en_data_json(codigo, 0)
            return (
                "✅ Código registrado correctamente.\n"
                "👋 ¡Bienvenido al curso de POO aplicada a HTML, CSS y JavaScript!\n"
                "Escribe **empezar** para comenzar."
            )
        else:
            return "🔑 Por favor ingresa tu código con el formato: `codigo: TU_CODIGO`"

    progreso = cargar_json(ruta)
    codigo = progreso.get("codigo", usuarios_codigo.get(usuario_id, f"usuario_{usuario_id}"))
    indice_modulo = progreso["modulo"]

    if indice_modulo >= len(modulos):
        return "🎉 ¡Felicitaciones! Has completado todos los módulos."

    modulo_actual = modulos[indice_modulo]
    etapa = progreso["etapa"]
    entrada = entrada.lower()

    if etapa == "inicio":
        if entrada == "empezar":
            progreso["etapa"] = "textos"
            guardar_json(ruta, progreso)
            return (
                f"🎬 Video: {modulo_actual['video_url']}\n\n"
                f"📚 {modulo_actual['textos'][0]}\n\n"
                f"📚 {modulo_actual['textos'][1]}\n\n"
                f"NOTA: {modulo_actual['textos'][2]}"
            )
        else:
            return "❌ Escribe **empezar** para iniciar el módulo."
    elif etapa == "textos":
        if entrada == "seguir":
            progreso["etapa"] = "pregunta"
            guardar_json(ruta, progreso)
            return modulo_actual["preguntas"][0]["pregunta"]
        else:
            return "❌ Escribe **seguir** para continuar."
    elif etapa == "pregunta":
        i = progreso["indice_pregunta"]
        respuesta_correcta = modulo_actual["preguntas"][i]["respuesta"].strip().lower()
        if entrada == respuesta_correcta:
            i += 1
            if i >= len(modulo_actual["preguntas"]):
                progreso["modulo"] += 1
                progreso["etapa"] = "inicio"
                progreso["indice_pregunta"] = 0
                guardar_json(ruta, progreso)
                registrar_en_data_json(codigo, progreso["modulo"])
                if progreso["modulo"] >= len(modulos):
                    return "🎉 ¡Felicitaciones! Has completado todos los módulos."
                return f"✅ ¡Muy bien! Has terminado este módulo.\n\nPerfecto, llevas completados {progreso['modulo']}/18.\nEscribe **empezar** para continuar."
            else:
                progreso["indice_pregunta"] = i
                guardar_json(ruta, progreso)
                return modulo_actual["preguntas"][i]["pregunta"]
        else:
            return "❌ Respuesta incorrecta. Intenta de nuevo."

    return "❌ Entrada no válida."
