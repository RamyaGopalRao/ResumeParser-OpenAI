import os
import chardet
from django.shortcuts import render, redirect
from .models import Resume, Education, Experience
from .parser import parse_resume
from django.db import IntegrityError
from pydantic import ValidationError

def handle_uploaded_file(f):
    try:
        # Create the uploads directory if it doesn't exist
        upload_dir = os.path.join('media', 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Construct the file path within the uploads directory
        file_path = os.path.join(upload_dir, f.name)

        # Save the uploaded file to the specified file path
        with open(file_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return file_path
    except Exception as e:
        print(f"Error handling uploaded file: {e}")
        return None

def upload_resume(request):
    try:
        if request.method == 'POST':
            resume_file = request.FILES['resume']
            file_path = handle_uploaded_file(resume_file)

            if not file_path:
                return render(request, 'parser/upload_resume.html', {'error': 'Failed to handle uploaded file.'})

            resume_dict = parse_resume(file_path)

            if not resume_dict:
                return render(request, 'parser/upload_resume.html', {'error': 'Failed to extract details from resume.'})

            # Check if a resume with the same email already exists
            existing_resume = Resume.objects.filter(email=resume_dict['email']).first()

            if existing_resume:
                existing_resume.name = resume_dict['name']
                existing_resume.phone = resume_dict['phone']
                existing_resume.skills = ", ".join(resume_dict['skills'])
                existing_resume.save()

                # Update Education entries
                for edu in resume_dict['education']:
                    Education.objects.create(
                        resume=existing_resume,
                        degree=edu['degree'],
                        field=edu['specialization'],
                        institution=edu['institution'],
                        year=edu['year']
                    )

                # Update Experience entries
                for exp in resume_dict['experience']:
                    Experience.objects.create(
                        resume=existing_resume,
                        position=exp['position'],
                        company=exp['company'],
                        duration=exp['years']
                    )
            else:
                # Save new resume details to database
                resume = Resume.objects.create(
                    name=resume_dict['name'],
                    email=resume_dict['email'],
                    phone=resume_dict['phone'],
                    skills=", ".join(resume_dict['skills'])
                )

                # Create Education entries
                for edu in resume_dict['education']:
                    Education.objects.create(
                        resume=resume,
                        degree=edu['degree'],
                        field=edu['specialization'],
                        institution=edu['institution'],
                        year=edu['year']
                    )

                # Create Experience entries
                for exp in resume_dict['experience']:
                    Experience.objects.create(
                        resume=resume,
                        position=exp['position'],
                        company=exp['company'],
                        duration=exp['years']
                    )

            return redirect('resume_list')
        return render(request, 'parser/upload_resume.html')

    except IntegrityError as e:
        print(f"Database Integrity Error: {e}")
        return render(request, 'parser/upload_resume.html', {'error': 'Database error while saving resume details.'})
    except ValidationError as e:
        print(f"Validation Error: {e}")
        return render(request, 'parser/upload_resume.html', {'error': f'Validation error: {e}'})
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return render(request, 'parser/upload_resume.html', {'error': f'An unexpected error occurred: {e}'})

def resume_list(request):
    try:
        resumes = Resume.objects.all()
        return render(request, 'parser/resume_list.html', {'resumes': resumes})
    except Exception as e:
        print(f"Error fetching resumes: {e}")
        return render(request, 'parser/resume_list.html', {'error': 'Failed to fetch resumes.'})
