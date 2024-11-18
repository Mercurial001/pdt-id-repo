from .models import IndividualHouse, Individual, Gender, Religion, Occupation,EducationalAttainment, \
    Barangay, Sitio, CivilStatus, SchoolName
from rest_framework.serializers import ModelSerializer


class BarangaySerializer(ModelSerializer):
    class Meta:
        model = Barangay
        fields = '__all__'


class SitioSerializer(ModelSerializer):
    class Meta:
        model = Sitio
        fields = '__all__'


class GenderSerializer(ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'


class CivilStatusSerializer(ModelSerializer):
    class Meta:
        model = CivilStatus
        fields = '__all__'


class ReligionSerializer(ModelSerializer):
    class Meta:
        model = Religion
        fields = '__all__'


class OccupationSerializer(ModelSerializer):
    class Meta:
        model = Occupation
        fields = '__all__'


class EducationalAttainmentSerializer(ModelSerializer):
    class Meta:
        model = EducationalAttainment
        fields = '__all__'


class SchoolNameSerializer(ModelSerializer):
    class Meta:
        model = SchoolName
        fields = '__all__'


class IndividualHouseSerializer(ModelSerializer):
    class Meta:
        model = IndividualHouse
        fields = '__all__'


class IndividualSerializer(ModelSerializer):
    class Meta:
        model = Individual
        fields = '__all__'
