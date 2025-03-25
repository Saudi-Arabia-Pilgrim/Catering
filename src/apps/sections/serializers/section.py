from apps.base.serializers import CustomModelSerializer
from apps.sections.models import Section


class SectionSerializer(CustomModelSerializer):
    class Meta:
        model = Section
        exclude = ["slug", "created_at", "created_by", "updated_at", "updated_by"]