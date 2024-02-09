from django.db import models

# Create your models here.


class Test(models.Model):
    joke = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}: {self.joke}"
