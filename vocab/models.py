from django.db import models


class EnWord(models.Model):
    word = models.CharField(max_length=50)
    translate = models.ManyToManyField('RuWord', blank=True)
    part_of_speech = models.ManyToManyField('PartOfSpeech', blank=True)
    collocation = models.ManyToManyField('Collocation', blank=True)
    phrase = models.ManyToManyField('Phrase', blank=True)
    cognate_word = models.ManyToManyField('CognateWord')
    audio_us = models.FileField(upload_to='audio/', blank=True)
    audio_uk = models.FileField(upload_to='audio/', blank=True)

    class Meta:
        ordering = ['word']

    def __str__(self):
        return self.word

    def get_translate(self):
        return ", ".join([str(p) for p in self.translate.all()])

    def get_collocation(self):
        return ", ".join([str(p) for p in self.collocation.all()])

    def get_phrase(self):
        return ", ".join([str(p) for p in self.phrase.all()])

    def get_cognate_word(self):
        return ", ".join([str(p) for p in self.cognate_word.all()])

    def get_part_of_speech(self):
        return ", ".join([str(p) for p in self.part_of_speech.all()])


class RuWord(models.Model):
    word = models.CharField(max_length=50, null=True)

    class Meta:
        ordering = ['word']

    def __str__(self):
        return self.word


class Collocation(models.Model):
    en_collocation = models.CharField(max_length=50)
    ru_collocation = models.CharField(max_length=50, null=True)

    class Meta:
        ordering = ['en_collocation']

    def __str__(self):
        return self.en_collocation


class Phrase(models.Model):
    en_phrase = models.CharField(max_length=50)
    ru_phrase = models.CharField(max_length=50, null=True)

    class Meta:
        ordering = ['en_phrase']

    def __str__(self):
        return self.en_phrase


class CognateWord(models.Model):
    en_cognate_word = models.CharField(max_length=50)
    ru_cognate_word = models.CharField(max_length=50, null=True)

    class Meta:
        ordering = ['en_cognate_word']

    def __str__(self):
        return self.en_cognate_word


class PartOfSpeech(models.Model):
    part_of_speech = models.CharField(max_length=50, null=True)

    class Meta:
        ordering = ['part_of_speech']

    def __str__(self):
        return self.part_of_speech



