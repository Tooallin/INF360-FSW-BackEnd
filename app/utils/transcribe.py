from fastapi import FastAPI, UploadFile, File, HTTPException
import speech_recognition as sr
import tempfile
from pydub import AudioSegment

async def transcribe(audio: UploadFile):
    try:
        print(f"Archivo recibido: {audio.filename}")
        if not audio.filename.endswith(".wav"):
            raise HTTPException(status_code=400, detail="Formato no compatible. Usa .wav")

        # Guardar el archivo original en un temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_original:
            contenido = await audio.read()
            tmp_original.write(contenido)
            tmp_original_path = tmp_original.name

        # Convertir a WAV PCM con pydub
        sound = AudioSegment.from_file(tmp_original_path)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_pcm:
            sound.export(tmp_pcm.name, format="wav")
            tmp_pcm_path = tmp_pcm.name

        # Transcribir con speech_recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_pcm_path) as source:
            audio_data = recognizer.record(source)
            texto = recognizer.recognize_google(audio_data, language="es-CL")
            return texto

    except sr.UnknownValueError:
        raise HTTPException(status_code=422, detail="No se pudo entender el audio")
    except sr.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Error al contactar el servicio: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")