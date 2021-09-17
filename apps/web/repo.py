from typing import List
from apps.web import models


class PatientRepo:
    def __init__(self):
        pass

    def list(self, therapist) -> List[models.Patients]:
        return models.Patients.objects.filter(therapist=therapist).all().order_by("email")

    def add(self, record: models.Patients):
        record.save()

    def get(self, id: int) -> models.Patients:
        return models.Patients.objects.get(id=id)
