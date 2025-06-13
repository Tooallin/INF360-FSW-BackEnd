from deep_translator import GoogleTranslator

def to_spanish(text: str):
	translated = GoogleTranslator(source='en', target='es').translate(text=text)
	return translated

def to_english(text: str):
	translated = GoogleTranslator(source='es', target='en').translate(text=text)
	return translated