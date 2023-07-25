from django.db import models
from django.utils import timezone
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=225)
    create_at = models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=225)
    price =  models.FloatField()
    students_qty = models.IntegerField()
    reviews_qty = models.IntegerField()
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    create_at = models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return self.title


