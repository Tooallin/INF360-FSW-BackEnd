import requests
import json
import re
from app.utils import translate
from app.core.config import settings

def generate_base():
	url = settings.deepseek_url
	headers = {"Content-Type": "application/json"}
	data = {
		"model": "deepseek-r1:1.5b",
		"prompt": "You are about to start a new conversation, return a greetings message, be gentle and respectful.",
		"stream": False,
		"options": {
			"temperature": 0
		},
	}

	response = requests.post(url=url, headers=headers, data=json.dumps(data), timeout=(5, 30))
	response_text = json.loads(response.text)['response']
	ia_response = re.sub(r'<think>.*?</think>', '', response_text, flags=re.DOTALL)
	return ia_response.strip()

def generate(message: str):
	url = settings.deepseek_url
	headers = {"Content-Type": "application/json"}
	data = {
		"model": "deepseek-r1:1.5b",
		"prompt": "Answer the following prompt carefully, trying not to hurt the person's feelings. The prompt is as follows:" + translate.to_english(message),
		"stream": False,
		"options": {
			"temperature": 0
		},
	}

	response = requests.post(url=url, headers=headers, data=json.dumps(data), timeout=(5, 30))
	response_text = json.loads(response.text)['response']
	ia_response = re.sub(r'<think>.*?</think>', '', response_text, flags=re.DOTALL)
	return ia_response.strip()