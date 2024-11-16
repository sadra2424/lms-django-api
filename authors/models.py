from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField()
    nationality = models.CharField(max_length=50)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name
