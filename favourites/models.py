from django.db import models

class AbstractResourceModel(models.Model):
    id = models.IntegerField(primary_key=True)
    custom_name = models.CharField(max_length=60, blank=True)
    is_favourite = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

class Planet(AbstractResourceModel):
    pass

class Movie(AbstractResourceModel):
    pass
