
from rest_framework import serializers
from apps.web import models


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Patients
        fields = ('email',
                  'first_name',
                  'last_name')

    def create(self, validated_data):
        return models.Patients(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        return instance
