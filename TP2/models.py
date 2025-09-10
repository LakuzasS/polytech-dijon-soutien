from django.db import models


class Statement(models.Model):
    date = models.DateTimeField("Date and time")
    text = models.TextField(blank=True, null=True)
    mood = models.IntegerField(
        choices=[
            (1, "Affreux"),
            (2, "Mauvais"),
            (3, "Moyen"),
            (4, "Bien"),
            (5, "Euphorique"),
        ],
        default=3,
    )

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d %H:%M')} - Humeur : {self.mood}"
