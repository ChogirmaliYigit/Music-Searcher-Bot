from django.db import models

class User(models.Model):
    full_name = models.CharField(max_length=500)
    username = models.CharField(max_length=400, null=True, blank=True)
    telegram_id = models.PositiveBigIntegerField()
    is_ban = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'User - {self.full_name}'


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.title


class FileId(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.TextField(null=True, blank=True, default=None)
    file_id = models.CharField(max_length=1000)
    show = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'File ID - {self.file_id}'


class Download(models.Model):
    file = models.ForeignKey(FileId, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Downloaded file - {self.file.file_id}'


class Keyword(models.Model):
    content = models.TextField()
    file = models.ForeignKey(FileId, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Keyword - {self.content}'


class Audio(models.Model):
    link = models.TextField()
    file_id = models.TextField()
    caption = models.TextField()

    def __str__(self) -> str:
        return f'Audio - {self.caption}'
