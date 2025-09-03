from apps.base.serializers import CustomModelSerializer
from apps.sections.models import Measure


class MeasureSerializer(CustomModelSerializer):
    class Meta:
        model = Measure
        exclude = ["slug", "created_by", "updated_at", "updated_by"]
