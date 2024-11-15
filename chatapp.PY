# chatproject/settings.py
INSTALLED_APPS = [
    # ... các ứng dụng khác
    'chatapp',
]
# chatapp/models.py
from django.db import models
from django.utils import timezone

class Message(models.Model):
    user = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}: {self.content[:20]}"

# chatapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
from models import Message
from django.views.decorators.csrf import csrf_exempt
import json

def chat_view(request):
    return render(request, 'chatapp/chat.html')

def get_messages(request):
    messages = Message.objects.order_by('-timestamp')[:50]  # Lấy 50 tin nhắn mới nhất
    messages = reversed(messages)  # Đảo ngược thứ tự
    data = [{"user": m.user, "content": m.content, "timestamp": m.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for m in messages]
    return JsonResponse(data, safe=False)

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data.get('user', 'Anonymous')
        content = data.get('content', '')
        if content:
            message = Message.objects.create(user=user, content=content)
            return JsonResponse({"user": message.user, "content": message.content, "timestamp": message.timestamp.strftime('%Y-%m-%d %H:%M:%S')})
    return JsonResponse({"error": "Invalid request"}, status=400)
