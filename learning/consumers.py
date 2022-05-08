import json

#  from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Messages


class ChatConsumer(WebsocketConsumer):
    '''
    def fetch_messages(self, data):
        messages = get_last_10_messages(data['chatId'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        user_contact = get_user_contact(data['from'])
        message = Messages.objects.create(
            contact=user_contact,
            content=data['message'])
        current_chat = get_current_chat(data['chatId'])
        current_chat.messages.add(message)
        current_chat.save()
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'text': message.text,
            'created_by': message.created_by,
            'created_at': message.created_at

        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }
    '''

    def connect(self):
        self.username = "Anonymous"
        self.accept()
        self.send(text_data="[Welcome %s!]" % self.username)

    def disconnect(self,message):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        


    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))