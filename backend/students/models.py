from django.db import models


class Student(models.Model):

    YEAR_CHOICES = [
        (1, 'Year 1'),
        (2, 'Year 2'),
        (3, 'Year 3'),
        (4, 'Year 4'),
    ]

    student_id = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    department = models.CharField(
        max_length=100
    )

    year = models.IntegerField(
        choices=YEAR_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['student_id']

    def __str__(self):
        return f"{self.student_id} - {self.name}"
