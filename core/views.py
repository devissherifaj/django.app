from django.shortcuts import render
from django.http import JsonResponse
from .models import Subject
from .models import StudySession
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# Create your views here.

def test_view(request):
    return JsonResponse ({"message":"view is working."})

def subject_list (request):
    if request.method == "GET":
        subject_qs= Subject.objects.all().values("id","name","description")
        subjects = list(subject_qs)
        return JsonResponse(subjects, safe=False)

@csrf_exempt
def subject(request, numri):
    if request.method == "GET":
        subject = Subject.objects.get(id=numri)

        subject_dict = {
            "id": subject.id,
            "name": subject.name,
            "description": subject.description
        }

        return JsonResponse(subject_dict, safe=False)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        name = data.get("name")
        description = data.get("description", "")

        subject = Subject.objects.create(
            name=name,
            description=description
        )

        return JsonResponse({
            "message": "created successfully",
            "name": subject.name,
            "description": subject.description
        })

    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        subject = Subject.objects.get(id=numri)

        name = data.get("name")
        description = data.get("description")

        if name is not None:
            subject.name = name

        if description is not None:
            subject.description = description

        subject.save()

        return JsonResponse({
            "message": "updated successfully",
            "id": subject.id,
            "name": subject.name,
            "description": subject.description
        })
    if request.method == "DELETE":
        try:
            subject = Subject.objects.get(id=numri)
        except Subject.DoesNotExist:
            return JsonResponse({"error": "Subject not found"}, status=404)

        subject.delete()

        return JsonResponse(
            {"message": "Subject deleted successfully"},
        )
    
    return JsonResponse({"error": "Method not allowed"}, status=405)




def study_session_list(request):
    if request.method == "GET":
        sessions = StudySession.objects.all().values(
            "id", "subject_id", "datetime", "duration_minutes", "notes"
        )
        return JsonResponse(list(sessions), safe=False)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)



def study_session(request, numri):
    if request.method == "GET":
        try:
            session = StudySession.objects.get(id=numri)
        except StudySession.DoesNotExist:
            return JsonResponse({"error": "StudySession not found"}, status=404)

        studysession_qs = {
            "id": session.id,
            "name":session.subject.name,
            "subject_id": session.subject.id,
            "datetime": session.datetime,
            "duration_minutes": session.duration_minutes,
            "notes": session.notes
        }

        studysession_list=[]

        for studysession in studysession_qs :
            subject = Subject.objects.get(id=studysession.get("subject"))
            studysession ["subject"] = studysession.subject.name
            studysession.append(studysession)
            
        return JsonResponse(studysession_list,studysession_qs)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        subject_id = data.get("subject_id")
        datetime_str = data.get("datetime",datetime.now())
        duration_minutes = data.get("duration_minutes",60)
        notes = data.get("notes", "")

        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return JsonResponse({"error": "Subject not found"}, status=404)

        try:
            session_datetime = datetime.fromisoformat(datetime_str)
        except Exception:
            return JsonResponse({"error": "Invalid datetime format. Use ISO format."}, status=400)

        session = StudySession.objects.create(
            subject=subject,
            datetime=session_datetime,
            duration_minutes=duration_minutes,
            notes=notes
        )

        return JsonResponse({
            "message": "created successfully",
            "id": session.id,
            "subject_id": session.subject.id,
            "datetime": session.datetime,
            "duration_minutes": session.duration_minutes,
            "notes": session.notes
        })
    
    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        try:
            session = StudySession.objects.get(id=numri)
        except StudySession.DoesNotExist:
         return JsonResponse({"error": "StudySession not found"}, status=404)

        subject_id = data.get("subject_id")
        datetime_str = data.get("datetime")
        duration_minutes = data.get("duration_minutes")
        notes = data.get("notes")

    if subject_id is not None:
        try:
            subject = Subject.objects.get(id=subject_id)
            session.subject = subject
        except Subject.DoesNotExist:
            return JsonResponse({"error": "Subject not found"}, status=404)

    if datetime_str is not None:
        try:
            session.datetime = datetime.fromisoformat(datetime_str)
        except Exception:
            return JsonResponse({"error": "Invalid datetime format. Use ISO format."}, status=400)

    if duration_minutes is not None:
        session.duration_minutes = duration_minutes

    if notes is not None:
        session.notes = notes

    session.save()

    return JsonResponse({
        "message": "updated successfully",
        "id": session.id,
        "subject_id": session.subject.id,
        "datetime": session.datetime,
        "duration_minutes": session.duration_minutes,
        "notes": session.notes
    })

    
    if request.method == "DELETE":
        try:
            session = StudySession.objects.get(id=numri)
        except StudySession.DoesNotExist:
            return JsonResponse({"error": "StudySession not found"}, status=404)

    session.delete()

    return JsonResponse({"message": "StudySession deleted successfully"})

    return JsonResponse({"error": "Method not allowed"}, status=405)
