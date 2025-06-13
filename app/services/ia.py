import requests
import json
import re
from app.core.config import settings

def generate(message: str):
	url = settings.deepseek_url
	headers = {"Content-Type": "application/json"}
	data = {
		"model": "deepseek-r1:1.5b",
		"prompt": message,
		"stream": False,
		"optiones": {
			"temperature": 0
		},
	}

	response = requests.post(url=url, headers=headers, data=json.dumps(data))
	response_text = json.loads(response.text)['response']
	ia_response = re.sub(r'<think>.*?</think>', '', response_text, flags=re.DOTALL)
	return ia_response.strip()