from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.sections.models import Section


class SectionSerializer(CustomModelSerializer): 

    class Meta:
        model = Section
        exclude = ["slug", "created_at", "created_by", "updated_at", "updated_by"]
        # required_fields = ["name_uz", "name_ru", "name_ar", "name_en"]
        # read_only_fields = ["name"]
