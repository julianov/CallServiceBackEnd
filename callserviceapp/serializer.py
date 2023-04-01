from callserviceapp.models import item
from rest_framework import serializers

class serializerRequestRubros(serializers.ModelSerializer):
    class Meta:
        model = item
        fields = ('items', 'certificate','provider', 'radius', 'description', 'days_of_works',
        'hour_init', 'hour_end', 'picture1','picture2','picture3')