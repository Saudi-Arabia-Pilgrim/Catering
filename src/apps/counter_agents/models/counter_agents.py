from django.db import models

from apps.base.models import AbstractBaseModel


class CounterAgents(AbstractBaseModel):
    """
    CounterAgents model represents the counter agents in the system.
    """

    # === The name of the counter agent. ===
    name = models.CharField(max_length=255,)
    # === A unique slug for the counter agent. ===
    slug = models.SlugField(max_length=255, unique=True)
    # === The address of the counter agent. ===
    address = models.CharField(max_length=1200)
    # === The status of the counter agent, indicating if they are active. ===
    status = models.BooleanField(default=True)

    class Meta:
        # === The name of the database table. ===
        db_table = 'counter_agents'
        # === The human-readable name of the model. ===
        verbose_name = 'Counter agent'
        # === The human-readable plural name of the model. ===
        verbose_name_plural = 'Counter agents'

    def __str__(self):
        """
        Returns the string representation of the counter agent, which is the name.
        """
        return self.name