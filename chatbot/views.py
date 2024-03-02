from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

from django.utils import timezone
import logging




openai_api_key = ''
openai.api_key = openai_api_key

logger = logging.getLogger(__name__)

def ask_openai(user_message):
    try:
        # 챗봇 완성 API 엔드포인트를 사용하여 요청
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": user_message}],
        )
        answer = response.choices[0].message['content'].strip()  # 응답 구조에 맞게 접근
        return answer
    except Exception as e:
        logger.error(f"OpenAI API 호출 중 오류 발생: {e}")
        return "처리 중 오류가 발생했습니다."

# Create your views here.
def chatbot(request):

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')


