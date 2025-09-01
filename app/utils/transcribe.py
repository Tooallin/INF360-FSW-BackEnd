# app/utils/transcribe.py
from fastapi import UploadFile, HTTPException
import speech_recognition as sr
import tempfile
from pydub import AudioSegment
import os

# Si necesitas apuntar ffmpeg manualmente (Windows/hosting), descomenta y ajusta:
# from pydub.utils import which
# AudioSegment.converter = which("ffmpeg")  # o ruta absoluta

CT_EXT_MAP = {
    "audio/webm": "webm",
    "video/webm": "webm",       # algunos navegadores lo envían así
    "audio/ogg": "ogg",
    "audio/opus": "opus",
    "audio/m4a": "m4a",
    "audio/x-m4a": "m4a",
    "audio/mp4": "m4a",         # Safari/QuickTime
    "audio/wav": "wav",
    "audio/x-wav": "wav",
    "audio/mp3": "mp3",
    "audio/mpeg": "mp3",
    "application/octet-stream": "bin",  # deja inferir por cabeceras
}

def guess_ext(filename: str | None, content_type: str | None) -> str:
    if filename and "." in filename:
        return filename.rsplit(".", 1)[-1].lower()
    if content_type in CT_EXT_MAP:
        return CT_EXT_MAP[content_type]
    return "bin"  # ffmpeg intentará inferir por cabeceras

async def transcribe(audio: UploadFile) -> str:
    tmp_original_path = None
    tmp_pcm_path = None

    try:
        orig_name = audio.filename or "upload"
        ext = guess_ext(orig_name, audio.content_type)
        print(f"[transcribe] Archivo recibido: {orig_name} | content_type={audio.content_type} | ext={ext}")

        # (Opcional) tamaño máximo, si está disponible
        # if getattr(audio, "size", None) and audio.size > 25 * 1024 * 1024:
        #     raise HTTPException(status_code=413, detail="Archivo demasiado grande (>25MB)")

        # Guardar original
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp_original:
            content = await audio.read()
            if not content:
                raise HTTPException(status_code=400, detail="Archivo vacío")
            tmp_original.write(content)
            tmp_original_path = tmp_original.name

        # Cargar con pydub (ffmpeg) e inferir formato si ext == "bin"
        try:
            fmt = None if ext == "bin" else ext
            sound = AudioSegment.from_file(tmp_original_path, format=fmt)
        except Exception as fe:
            raise HTTPException(
                status_code=415,
                detail=f"Formato no soportado o ffmpeg ausente: {fe}"
            )

        # Normalizar: mono, 16kHz, 16-bit PCM
        sound = sound.set_channels(1).set_frame_rate(16000)

        # Exportar a WAV PCM
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_pcm:
            sound.export(tmp_pcm.name, format="wav")
            tmp_pcm_path = tmp_pcm.name

        # Transcribir
        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_pcm_path) as source:
            audio_data = recognizer.record(source)
            texto = recognizer.recognize_google(audio_data, language="es-CL")
            return texto

    except sr.UnknownValueError:
        raise HTTPException(status_code=422, detail="No se pudo entender el audio")
    except sr.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Error al contactar el servicio de STT: {e}")
    except HTTPException:
        raise
    except Exception as e:
        print("[transcribe] Error no controlado:", e)
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")
    finally:
        # Limpieza de temporales
        for path in (tmp_original_path, tmp_pcm_path):
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as _:
                    pass