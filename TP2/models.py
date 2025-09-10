from django.db import models

class Statement(models.Model):
    date = models.DateTimeField("Date du statement")
    text = models.TextField(blank=True, null=True)
    mood = models.IntegerField(
        choices=[(1, "Affreux"), (2, "Pas top "), (3, "Ok, ça passe"), (4, "Là j'suis bien"), (5, "Euphorique")],
        default=3,
    )

    def __str__(self):
        return f"{self.date} - mood {self.mood}"


class Actual(models.Model):
    statement = models.OneToOneField(Statement, on_delete=models.CASCADE)

    def __str__(self):
        return f"Current: {self.statement}"


class Indicator(models.Model):  
    title = models.CharField(max_length=200)
    question = models.TextField()

    def __str__(self):
        return self.title


class Answer(models.Model): 
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.indicator.title} -> {self.value}"
