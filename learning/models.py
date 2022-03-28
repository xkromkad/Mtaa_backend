from django.db import models


class Users(models.Model):
    class Meta:
        db_table = 'Users'
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=30)
    photo = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Feed(models.Model):
    class Meta:
        db_table = 'Feed'
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Files(models.Model):
    class Meta:
        db_table = 'Files'
    feed_id = models.ForeignKey(Feed, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=50)


class Chats(models.Model):
    class Meta:
        db_table = 'Chats'
    created_at = models.DateTimeField(auto_now_add=True)


class Chat_users(models.Model):
    class Meta:
        db_table = 'Chat_users'
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    chat_id = models.ForeignKey(Chats, on_delete=models.CASCADE)


class Messages(models.Model):
    class Meta:
        db_table = 'Messages'
    text = models.CharField(max_length=200)
    created_by = models.ForeignKey(Chat_users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


