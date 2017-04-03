from django.db import models


class Voice(models.Model):
    voice_id = models.IntegerField()
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=100)

    def get_max_id(self):
        return self.objects.all().order_by('-voice_id').first()
