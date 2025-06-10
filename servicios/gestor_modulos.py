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
        guardar_json(ruta, {"codigo": None, "modulo": 0, "etapa": "inicio", "indice_pregunta": 0})
    return cargar_json(ruta)

def actualizar_data_json(usuario_id, codigo, modulo):
    data = cargar_json(RUTA_DATA)
    encontrado = False
    for usuario in data:
        if usuario["id"] == usuario_id:
            usuario["modulo"] = modulo
            encontrado = True
            break
    if not encontrado:
        data.append({"id": usuario_id, "codigo": codigo, "modulo": modulo})
    guardar_json(RUTA_DATA, data)

def procesar_entrada_usuario(usuario_id, entrada):
    ruta = ruta_progreso(usuario_id)
    progreso = inicializar_usuario(usuario_id)

    if progreso["codigo"] is None:
        progreso["codigo"] = entrada.strip()
        guardar_json(ruta, progreso)
        actualizar_data_json(usuario_id, progreso["codigo"], progreso["modulo"])
        return "✅ Código registrado correctamente. Escribe **empezar** para comenzar el curso."

    indice_modulo = progreso["modulo"]
    if indice_modulo >= len(modulos):
        return "🎉 ¡Felicitaciones! Has completado todos los módulos."

    modulo_actual = modulos[indice_modulo]
    etapa = progreso["etapa"]
    entrada = entrada.strip().lower()

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
            return "❌ Para comenzar, debes escribir la palabra: **empezar**"
    elif etapa == "textos":
        if entrada == "seguir":
            progreso["etapa"] = "pregunta"
            guardar_json(ruta, progreso)
            return modulo_actual["preguntas"][0]["pregunta"]
        else:
            return "❌ Escribe la palabra **'seguir'** para continuar."
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
                actualizar_data_json(usuario_id, progreso["codigo"], progreso["modulo"])

                if progreso["modulo"] >= len(modulos):
                    return "🎉 ¡Felicitaciones! Has completado todos los módulos."

                return f"✅ ¡Muy bien! Has terminado este módulo.\n\nPerfecto, llevas completados {progreso['modulo']}/18 módulos.\nEscribe **'empezar'** para continuar."
            else:
                progreso["indice_pregunta"] = i
                guardar_json(ruta, progreso)
                return modulo_actual["preguntas"][i]["pregunta"]
        else:
            return "❌ Respuesta incorrecta. Intenta de nuevo."

    return "❌ Entrada no válida. Por favor, escribe una palabra correcta según la etapa."
