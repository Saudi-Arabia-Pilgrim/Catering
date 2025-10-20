from django.db import models
from django.utils.text import slugify

from apps.base.models import AbstractBaseModel


class CounterAgent(AbstractBaseModel):
    """
    CounterAgent model represents the counter agents in the system.
    """

    class Type(models.TextChoices):
        B2B = "B2B"
        B2C = "B2C"

    # === The type of the counter agent(B2B or B2C). ===
    counter_agent_type = models.CharField(choices=Type.choices)
    # === The name of the counter agent. ===
    name = models.CharField(max_length=255)
    # === The slug of the counter agent. ===
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    # === The address of the counter agent. ===
    address = models.CharField(max_length=1200)
    # === The status of the counter agent, indicating if they are active. ===
    status = models.BooleanField(default=True)

    def __str__(self):
        """
        Returns the string representation of the counter agent, which is the name.
        """
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        # === The name of the database table. ===
        db_table = "counter_agents"
        # === The human-readable name of the model. ===
        verbose_name = "Counter agent"
        # === The human-readable plural name of the model. ===
        verbose_name_plural = "Counter agents"
        # === Ordering field for sorting a set of queries ===
        ordering = ["-created_at"]
