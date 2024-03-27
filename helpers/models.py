from django.db import models


class TrackingModel(models.Model):   ##This model automatically includes the created and updated timestamps for our models so we do not need to define them again.
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models. DateTimeField(auto_now = True)

    class Meta:
        abstract = True   #Prevents us from creating instances of this class since this class is just to be inherited from.
        ordering = ('-created_at',)   #orders the attributes of this class according to the created at timestamp in descending order.