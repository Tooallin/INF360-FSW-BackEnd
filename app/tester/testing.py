# app/tester/ia_tester_endpoint.py
import re
import ast
from typing import List, Dict
from fastapi import APIRouter
from app.schemas.user import UserCreate
from app.main import generate

UMBRAL_PALABRAS_BUENAS = 1

PALABRAS_CLAVE_APOYO = [
    'a veces puede parecer', 'acompañarte', 'apoyo', 'buscar apoyo', 'buen trabajo',
    'celebro', 'comprendo', 'cuidarte', 'cuesta manejarlo', 'descansar', 'demasiado',
    'entiendo', 'es complejo', 'es comprensible', 'es difícil', 'es normal', 'es válido',
    'está claro', 'estas haciendo lo mejor', 'estoy aquí', 'estoy contigo',
    'estoy contento por ti', 'felicidades', 'felicitaciones', 'genial',
    'gracias por compartir', 'gracias por contarlo', 'increíble', 'lamento',
    'lo que sientes importa', 'lo tendré en cuenta', 'lo registro', 'me alegra',
    'me emociona', 'me parece', 'mereces', 'mucho esfuerzo', 'no está mal sentirse así',
    'no estás solo', 'no te exijas', 'paso a paso', 'puedes sentirte así',
    'puedo seguirte', 'puede ser confuso', 'puede ser duro', 'puede ser pesado',
    'que alegría', 'que bueno', 'quizás sientas', 'recargar energías', 'respira',
    'sé que cuesta', 'sé que duele', 'sé que es', 'sé que es difícil',
    'sé que parece oscuro', 'siento mucho', 'te comprendo', 'te entiendo profundamente',
    'te escucho', 'toma un respiro', 'tómate un momento', 'validar lo que sientes', 'ánimo', 'maravilloso'
]

PALABRAS_CLAVE_INADECUADAS = [
    "que tonto", "qué tonto", "da igual lo que sientas", "exageras", "eso no importa",
    "eres débil", "no sirve de nada", "es tu culpa", "qué problema el tuyo",
    "siempre te quejas", "estás loco", "no seas ridículo", "no tiene sentido lo que dices",
    "deberías superarlo ya", "nadie quiere escucharte", "eso no es nada",
    "no hagas un drama", "tú te lo buscaste", "que inútil", "qué inútil",
    "ignóralo", "mejor cállate", "cállate", "deja de llorar", "no llores",
    "no te quejes", "es una tontería", "no es para tanto", "no te hagas la víctima"
]

POOL_EMOCIONES = ['cansancio', 'frustración', 'gratitud', 'tristeza', 'miedo',
                  'alivio', 'esperanza', 'orgullo', 'alegría', 'neutro']



router = APIRouter()


def _buscar_coincidencias(texto: str, frases):
    texto_low = texto.lower()
    halladas = [kw for kw in frases if re.search(re.escape(kw.lower()), texto_low)]
    return list(dict.fromkeys(halladas))




def analizar_respuesta(respuesta_texto, palabras_buenas):
    buenas_encontradas = _buscar_coincidencias(respuesta_texto, palabras_buenas)
    contiene_apoyo = len(buenas_encontradas) >= UMBRAL_PALABRAS_BUENAS

    malas_encontradas = _buscar_coincidencias(respuesta_texto, PALABRAS_CLAVE_INADECUADAS)
    contiene_inadecuadas = len(malas_encontradas) > 0

    emociones_encontradas = []
    m = re.search(r'(?im)^\s*emociones:\s*([^\n\r]+)', respuesta_texto)
    if m:
        emociones_str = m.group(1)
        emociones_encontradas = [e.strip().lower() for e in emociones_str.split(',') if e.strip()]

    return contiene_apoyo, contiene_inadecuadas, emociones_encontradas, buenas_encontradas, malas_encontradas




def ejecutar_prueba(caso_de_prueba, user_record: UserCreate, context: List[Dict]):
    prompt_analisis = f"""
Analiza el siguiente mensaje del usuario y responde:
- Sé empático, comprensivo y de apoyo.
- Incluye explícitamente una línea con: 'Emociones: <lista de emociones detectadas>'.
- Solo considera emociones dentro del siguiente pool: {', '.join(POOL_EMOCIONES)}.
- No uses palabras inadecuadas ni negativas.
Mensaje del usuario: {caso_de_prueba['frase']}
"""
    context = context[:]
    context.insert(0, {"role": "user", "parts": [{"text": prompt_analisis}]})

    try:
        respuesta_ia = generate(caso_de_prueba['frase'], context, user_record)

        contiene_apoyo, contiene_inadecuadas, emociones_detectadas, buenas, malas = analizar_respuesta(
            respuesta_ia, PALABRAS_CLAVE_APOYO
        )
        emociones_detectadas = [e for e in emociones_detectadas if e in [p.lower() for p in POOL_EMOCIONES]]

        emociones_esperadas_limpias = [e.lower() for e in caso_de_prueba['emociones_esperadas']]
        emocion_correcta = set(emociones_detectadas) == set(emociones_esperadas_limpias)

    except Exception:
        respuesta_ia = ""
        contiene_apoyo = contiene_inadecuadas = emocion_correcta = False
        buenas = malas = []
        emociones_detectadas = []

    respuesta_adecuada = (contiene_apoyo and not contiene_inadecuadas)
    
    return {
        'id': caso_de_prueba['id'],
        'frase': caso_de_prueba['frase'],
        'emocion_correcta': emocion_correcta,
        'respuesta_adecuada': respuesta_adecuada,
        'buenas': buenas,
        'malas': malas,
        'emociones_detectadas': emociones_detectadas,
        'respuesta': respuesta_ia
    }




def leer_casos_de_prueba_desde_archivo(nombre_archivo):
    casos = []
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        for i, linea in enumerate(f, 1):
            partes = linea.strip().rsplit(',', 1)
            if len(partes) == 2:
                frase = partes[0].strip().strip('"')
                try:
                    emociones_esperadas = ast.literal_eval(partes[1].strip())
                    casos.append({'id': i, 'frase': frase, 'emociones_esperadas': emociones_esperadas})
                except Exception:
                    continue
    return casos


def escribir_resultados_en_archivo(nombre_archivo, resultados, resumen): 
    with open(nombre_archivo, 'w', encoding='utf-8') as f: 
        for r in resultados: 
            f.write( 
                f"Caso {r['id']}: Frase: \"{r['frase']}\", " 
                f"Emoción correcta: {'Si ✅' if r['emocion_correcta'] else 'No ❌'}, " 
                f"Respuesta Adecuada: {'Si ✅' if r['respuesta_adecuada'] else 'No ❌'}\n" ) 
            if r.get('buenas'): f.write(f" - Palabras de apoyo detectadas: {', '.join(r['buenas'])}\n") 
            if r.get('malas'): f.write(f" - ⚠️ Frases inadecuadas detectadas: {', '.join(r['malas'])}\n") 
            if r.get('respuesta'): f.write(f" - Respuesta IA: {r['respuesta'].strip()}\n") 
            f.write("\n" + "="*30 + "\n") 
            f.write(resumen)




def ejecutar_todos_los_tests(user_record: UserCreate, context: List[Dict], archivo_casos="test_cases.txt"):
    casos_de_prueba = leer_casos_de_prueba_desde_archivo(archivo_casos)
    if not casos_de_prueba:
        return {"mensaje": "No se encontraron casos de prueba.", "resultados": []}

    resultados_pruebas = []
    emociones_correctas = 0
    respuestas_adecuadas = 0

    for caso in casos_de_prueba:
        resultado = ejecutar_prueba(caso, user_record, context)
        resultados_pruebas.append(resultado)
        if resultado['emocion_correcta']: emociones_correctas += 1
        if resultado['respuesta_adecuada']: respuestas_adecuadas += 1

    total = len(casos_de_prueba)
    resumen_texto = (
        f"Emociones Detectadas Correctamente: {emociones_correctas/total*100:.2f}%\n"
        f"Respuestas Adecuadas: {respuestas_adecuadas/total*100:.2f}%\n"
    )
    return {"mensaje": "Tests ejecutados correctamente", "resumen": resumen_texto, "resultados": resultados_pruebas}




@router.post("/run-tests")
def run_tests_endpoint(user: UserCreate):
    context: List[Dict] = []
    return ejecutar_todos_los_tests(user, context)
