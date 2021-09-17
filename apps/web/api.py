import stripe

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http.response import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from apps.web import repo, serializers, models


@api_view(['POST'])
def patients(request):
    patient_serl = serializers.PatientSerializer(data=request.data)
    if patient_serl.is_valid():
        patient = patient_serl.create(patient_serl.validated_data)
        patient.therapist = request.user
        patient.save()
        return JsonResponse(patient_serl.data, status=status.HTTP_201_CREATED)
    return JsonResponse(patient_serl.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def patient(request, patient_id):
    try:
        patient_repo = repo.PatientRepo()
        patient = patient_repo.get(patient_id)
    except models.Patients.DoesNotExist:
        return JsonResponse({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        patient_serl = serializers.PatientSerializer(patient)
        return JsonResponse(data=patient_serl.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        patient_serl = serializers.PatientSerializer(patient, data=request.data)
        if patient_serl.is_valid():
            patient = patient_serl.update(patient, patient_serl.validated_data)
            patient.save()
            messages.info(request, "Patient has been updated")
            return JsonResponse(patient_serl.data)
        return JsonResponse(patient_serl.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        patient.delete()
        return JsonResponse({'message': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def sending_email_to_patient(request):
    receiver = request.POST["email"]
    link = request.POST["link"]
    send_mail("Memory Remedy",
              f"Please join the section at: {link}",
              settings.SERVER_EMAIL,
              [receiver])
    messages.info(request, f"An email has been sent to {receiver}")
    return JsonResponse({'message': "OK"})
