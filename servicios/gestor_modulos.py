import os
from utilidades.json_utils import cargar_json, guardar_json

RUTA_MODULOS = "modulos/modulos.json"
RUTA_PROGRESO = "progreso"
RUTA_DATA = "data/data.json"

modulos = cargar_json(RUTA_MODULOS)

def ruta_progreso(usuario_id):
    return f"{RUTA_PROGRESO}/usuario_{usuario_id}.json"

def inicializar_usuario(usuario_id):
    ruta = ruta_progreso(usuario_id)
    if not os.path.exists(ruta):
        guardar_json(ruta, {
            "codigo": None,
            "modulo": 0,
            "etapa": "esperando_codigo",
            "indice_pregunta": 0
        })
    return cargar_json(ruta)

def actualizar_data_json(codigo, modulo):
    data = cargar_json(RUTA_DATA)
    if isinstance(data, list):
        data = {}
    data[codigo] = {"modulo": modulo}
    guardar_json(RUTA_DATA, data)

def procesar_entrada_usuario(usuario_id, entrada):
    ruta = ruta_progreso(usuario_id)
    progreso = inicializar_usuario(usuario_id)

    etapa = progreso.get("etapa", "esperando_codigo")
    entrada = entrada.strip()

    if etapa == "esperando_codigo":
        if entrada.isdigit():
            progreso["codigo"] = entrada
            progreso["etapa"] = "inicio"
            guardar_json(ruta, progreso)
            actualizar_data_json(entrada, progreso["modulo"])
            return (
                "✅ Código registrado correctamente.\n"
                "👋 ¡Bienvenido al curso de POO aplicada a HTML, CSS y JavaScript!\n"
                "Escribe **empezar** para comenzar."
            )
        else:
            return "🔑 Por favor ingresa tu código: "

    indice_modulo = progreso["modulo"]

    if indice_modulo >= len(modulos):
        return "🎉 ¡Felicitaciones! Has completado todos los módulos."

    modulo_actual = modulos[indice_modulo]
    etapa = progreso["etapa"]

    if etapa == "inicio":
        if entrada.lower() == "empezar":
            progreso["etapa"] = "textos"
            guardar_json(ruta, progreso)
            return (
                f"🎬 Video: {modulo_actual['video_url']}\n\n"
                f"📚 {modulo_actual['textos'][0]}\n\n"
                f"📚 {modulo_actual['textos'][1]}\n\n"
                f"NOTA: {modulo_actual['textos'][2]}"
            )
        else:
            return "❌ Para comenzar, escribe **empezar**"

    elif etapa == "textos":
        if entrada.lower() == "seguir":
            progreso["etapa"] = "pregunta"
            guardar_json(ruta, progreso)
            return modulo_actual["preguntas"][0]["pregunta"]
        else:
            return "❌ Escribe **seguir** para continuar."

    elif etapa == "pregunta":
        i = progreso["indice_pregunta"]
        respuesta_correcta = modulo_actual["preguntas"][i]["respuesta"].strip().lower()

        if entrada.lower() == respuesta_correcta:
            i += 1
            if i >= len(modulo_actual["preguntas"]):
                progreso["modulo"] += 1
                progreso["etapa"] = "inicio"
                progreso["indice_pregunta"] = 0
                guardar_json(ruta, progreso)
                actualizar_data_json(progreso["codigo"], progreso["modulo"])

                if progreso["modulo"] >= len(modulos):
                    return "🎉 ¡Felicitaciones! Has completado todos los módulos."

                return (
                    f"✅ ¡Muy bien! Has terminado este módulo.\n"
                    f"Perfecto, llevas completados {progreso['modulo']}/18 módulos.\n"
                    "Escribe **empezar** para continuar con el siguiente módulo."
                )
            else:
                progreso["indice_pregunta"] = i
                guardar_json(ruta, progreso)
                return modulo_actual["preguntas"][i]["pregunta"]
        else:
            return "❌ Respuesta incorrecta. Intenta de nuevo."

    return "❌ Entrada no válida."
