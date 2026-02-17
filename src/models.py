from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tarea")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_secured = models.BooleanField(default=True, verbose_name="Blindaje Shadow")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"🏮 {self.title}"
