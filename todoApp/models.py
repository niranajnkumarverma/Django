from django.db import models

# first model/table
class User(models.Model):
    ProfilePhoto = models.FileField(upload_to="uploads/users/", default="uploads/default.png")
    Name = models.CharField(max_length=20, null=True, blank=True)
    Email = models.EmailField(max_length=30)
    Password = models.CharField(max_length=12)
    Address = models.CharField(max_length=12, null=True, blank=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return 'No Name' if not self.Name else self.Name

class ToDo(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=20)
    Content = models.TextField(max_length=50)
    DateCreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'todo'

    def __str__(self):
        return self.Title
