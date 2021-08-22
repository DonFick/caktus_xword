from django.db import models
from random import randint

# Create your models here.

# we are using SQLLite, so we can set relatively long lengths on a CharField.
class Entry(models.Model):
    entry_text = models.CharField(max_length=50, unique=True,)

    def __str__(self):
        return '{}'.format(self.entry_text)


class Puzzle(models.Model):
    title = models.TextField(max_length=255, blank=True, default='',)
    date = models.DateField()
    byline = models.TextField(max_length=255,)
    publisher = models.TextField(max_length=12,)

    def __str__(self):
        return '{} - {}'.format(self.date, self.publisher)


class Clue(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE,)
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE,)
    clue_text = models.CharField(max_length=512,)
    theme = models.BooleanField(default=False,)

    # def __str__(self):
    #     return '{} - {}'.format(self.entry.entry_text, self.clue_text)
    #
