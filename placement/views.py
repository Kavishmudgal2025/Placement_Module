from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Student, StudentProfile , Job, JobApplication, ApplicationStatus
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login
import csv,random
from decimal import Decimal
from datetime import date
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from functools import wraps
from .utils import send_email_for_verification
from django.utils import timezone
from django.utils.dateparse import parse_date


#Declare Global Varibales here.

# Create your views here.

def student_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'student_id' not in request.session:
            return redirect('/login/')   # student login page
        return view_func(request, *args, **kwargs)
    return wrapper


def switch_profile(request):
    return render(request, 'switch_profile.html')


def signin(request):
    #return HttpResponse("hello")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        student = Student.objects.filter(email=email).first()
        if student:
            if student.password == password:
                request.session['student_id'] = student.sId
                return redirect('profile/')
            else:
                return render(request,'student_login.html', {"ERROR":"Invalid Email ID or Password"})
        else:
            return render(request,'student_login.html', {"ERROR":"Invalid Email address or Password"})
    

    return render(request,'student_login.html')


def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        sId = request.POST.get("sId")
        number = request.POST.get("phone")
        gender = request.POST.get("gender")
        course = request.POST.get("course")
        passYear = request.POST.get("passYear")
        university = request.POST.get("university")
        specialization = request.POST.get("spec")
        state = request.POST.get("state")
        city = request.POST.get("city")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if len(number)!=10:
            return render(request,"student_signup.html", {"ERROR":"Please enter a valid number"})
        
        if password1 != password2:
            return render(request,"student_signup.html", {"ERROR":"Password do not match"})
        
        if Student.objects.filter(email=email).exists():
            return render(request, "student_signup.html", {"ERROR": "Email already exists"})
        
        if Student.objects.filter(phone=number).exists():
            return render(request, "student_signup.html", {"ERROR": "Phone number already exists"})
        
        if Student.objects.filter(sId=sId).exists():
            return render(request, "student_signup.html", {"ERROR": "Student ID already exists"})
        
        if password1 == password2:  # check confirm password
            student = Student(
                name=name,
                sId=sId,
                phone=number,
                gender=gender,
                course=course,
                passout_year = passYear,
                university=university,
                specialization=specialization,
                university_state=state,
                university_city=city,
                email=email,
                password=password1
            )
            student.save()
            messages.success(request, "You're successfully registered, Please login")

            return redirect("signup")  
    return render(request, "student_signup.html")

# Mail Verification logic
@student_login_required
def verify_student(request):                
    student_id = request.session.get('student_id')
    studentDetails = Student.objects.get(sId=student_id)

    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        actual_otp = request.session.get('mail_otp')
        
        if str(entered_otp) == str(actual_otp):
            del request.session['mail_otp']
            studentDetails.verification_status_mail = True
            studentDetails.save()
            messages.success(request, "Email verified ")
            return redirect('/login/profile/student_verification/')
        else:
            messages.error(request, "Invalid OTP. Please try again!")
            return render(request, "student_verification.html", {"student_data":studentDetails} )
    
    return render(request, "student_verification.html", {"student_data":studentDetails} )

# For sending OTP-mail
def send_otp(request):           
    student= request.session.get('student_id')
    student_data = Student.objects.get(sId=student)
    otp = random.randint(100000,999999)
    request.session['mail_otp'] = otp
    send_email_for_verification(otp, student_data.name, student_data.email)
    
    return redirect('/login/profile/student_verification/')


@student_login_required
def student_profile(request):
    student_id = request.session.get('student_id')   

    if student_id:
        studentDetails = Student.objects.get (sId = student_id)
        profile = StudentProfile.objects.filter(student=studentDetails)
        profile_obj = profile.first()
        all_jobs = Job.objects.all()
        eligible_jobs = []

        for job_post in all_jobs:
            if (studentDetails.passout_year == int(job_post.eligiblity_batch)):
                if profile_obj:
                    if (profile_obj.marks10 >= Decimal(job_post.eligiblity_10_marks) and profile_obj.marks12 >= Decimal(job_post.eligiblity_12_marks) and (profile_obj.graduation_marks is None or profile_obj.graduation_marks >= Decimal(job_post.eligiblity_college_marks))):
                        eligible_jobs.append(job_post)
        return render(request,'student_profile.html', {"student_data":studentDetails, 
                                                                        "updated_data":profile,
                                                                        "job_data":eligible_jobs} )
    else: 
        
        return render(request,"home_login.html")


def student_logout(request):
    try:
        del request.session['student_id']
    except KeyError:
        pass
    return redirect('/login/')


def admin (request):
    studentDetails = Student.objects.all()

    if request.method =="POST":
        username = request.POST ["username"]
        password = request.POST ["password"]

        user = authenticate(request,username=username, password=password)
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect("admin_home")  # admin home 
            else:
                return render(request, "admin_login.html")
        else:
            return render(request, "admin_login.html", {'ERROR': " Invalid Email address or Password"})
    
    return render(request,"admin_login.html")


@login_required(login_url='/admin_login/')
def admin_home(request):
    studentDetails = Student.objects.all()

    # collect filters
    filters = {
        "name": request.GET.get("name"),
        "sid": request.GET.get("ID"),
        "email": request.GET.get("email"),
        "course": request.GET.get("course"),
        "university": request.GET.get("university"),
        "university_city": request.GET.get("university_city"),
        "university_state": request.GET.get("university_state"),
        "phone": request.GET.get("phone"),
        "gender": request.GET.get("gender"),
        "passout_year": request.GET.get("passout_year"),
    }

    # check if any filters applied
    applied = False

    if filters["name"]:
        studentDetails = studentDetails.filter(name__icontains=filters["name"])
        applied = True
    if filters["sid"]:
        studentDetails = studentDetails.filter(sId__icontains=filters["sid"])
        applied = True
    if filters["email"]:
        studentDetails = studentDetails.filter(email__icontains=filters["email"])
        applied = True
    if filters["course"]:
        studentDetails = studentDetails.filter(course__icontains=filters["course"])
        applied = True
    if filters["university"]:
        studentDetails = studentDetails.filter(university__icontains=filters["university"])
        applied = True
    if filters["university_city"]:
        studentDetails = studentDetails.filter(university_city__icontains=filters["university_city"])
        applied = True
    if filters["university_state"]:
        studentDetails = studentDetails.filter(university_state__icontains=filters["university_state"])
        applied = True
    if filters["phone"]:
        studentDetails = studentDetails.filter(phone__icontains=filters["phone"])
        applied = True
    if filters["gender"]:
        studentDetails = studentDetails.filter(gender__icontains=filters["gender"])
        applied = True
    if filters["passout_year"]:
        studentDetails = studentDetails.filter(passout_year__icontains=filters["passout_year"])
        applied = True

    # if page reload has query params but no filters -> reset URL
    if request.GET and not applied:
        return redirect("admin_home")

    return render(request, "admin_home.html", {"studentData": studentDetails})


def admin_logout(request):
    logout(request)
    return redirect('/admin_login/')

@login_required(login_url='/admin_login/')
def import_students(request):
    return render(request, "import_students.html")


def student_upload(request):
    if request.method == "POST":
        
        uploaded_file = request.FILES.get("user_file")

        if not uploaded_file:
            messages.error(request, "No file selected")
            return redirect("student_upload")

        if not uploaded_file.name.endswith('.csv'):
            messages.error(request, "Only CSV files are allowed")
            return redirect("student_upload")

        file_data = uploaded_file.read().decode("utf-8").splitlines()
        reader = csv.reader(file_data)

        next(reader) #To skip the first ROW (table heading row) in the sheet

        success_count = 0
        error_count = 0

        for row in reader:
            try:
                Name = row[0]
                Student_ID = row[1]
                Phone_number = row[2]
                Gender = row[3]
                Course = row[4]
                Passout_year = row[5]
                University = row[6]
                Specialization = row[7]
                University_state = row[8]
                University_city = row[9]
                Email = row[10]
                Password = row[11]

                Student.objects.create(
                    name = Name,
                    sId = Student_ID,
                    phone = Phone_number,
                    gender = Gender,
                    course = Course,
                    passout_year = Passout_year,
                    university = University,
                    specialization = Specialization,
                    university_state = University_state,
                    university_city = University_city,
                    email = Email,
                    password = Password
                )
                success_count += 1
            except Exception:
                error_count += 1
                continue

        messages.success(request, f"Import completed: {success_count} records added, {error_count} failed.")
        return redirect("student_upload")

    return render(request, "import_students.html")


@login_required(login_url='/admin_login/')
def export_students(request):
    studentDetails = Student.objects.all()

    # apply same filters as admin_home
    filters = {
        "name": request.GET.get("name"),
        "sid": request.GET.get("ID"),
        "email": request.GET.get("email"),
        "course": request.GET.get("course"),
        "university": request.GET.get("university"),
        "university_city": request.GET.get("university_city"),
        "university_state": request.GET.get("university_state"),
        "phone": request.GET.get("phone"),
        "gender": request.GET.get("gender"),
        "passout_year": request.GET.get("passout_year"),
    }

    if filters["name"]:
        studentDetails = studentDetails.filter(name__icontains=filters["name"])
    if filters["sid"]:
        studentDetails = studentDetails.filter(sId__icontains=filters["sid"])
    if filters["email"]:
        studentDetails = studentDetails.filter(email__icontains=filters["email"])
    if filters["course"]:
        studentDetails = studentDetails.filter(course__icontains=filters["course"])
    if filters["university"]:
        studentDetails = studentDetails.filter(university__icontains=filters["university"])
    if filters["university_city"]:
        studentDetails = studentDetails.filter(university_city__icontains=filters["university_city"])
    if filters["university_state"]:
        studentDetails = studentDetails.filter(university_state__icontains=filters["university_state"])
    if filters["phone"]:
        studentDetails = studentDetails.filter(phone__icontains=filters["phone"])
    if filters["gender"]:
        studentDetails = studentDetails.filter(gender__icontains=filters["gender"])
    if filters["passout_year"]:
        studentDetails = studentDetails.filter(passout_year__icontains=filters["passout_year"])

    # create the HttpResponse object with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Student ID', 'Gender', 'Course', 'University', 'Passout Year', 'State', 'City', 'Email', 'phone'])

    for student in studentDetails:
        writer.writerow([
            student.name,
            student.sId,
            student.gender,
            student.course,
            student.university,
            student.passout_year,
            student.university_state,
            student.university_city,
            student.email,
            student.phone,
        ])

    return response

@student_login_required
def updateProfile(request):
    #return HttpResponse("update here")
    
    ID = request.session.get("student_id")  # fetch from session

    if not ID:
        return HttpResponse("No student_id found in session")  # debug message
    try:
        stu = Student.objects.get(sId=ID)   # or .get(id=ID) if using default pk
    except Student.DoesNotExist:
        return HttpResponse("Student not found")
        
    profile = StudentProfile.objects.filter(student=stu).first()

    if request.method == "POST":
        if not profile:
            profile = StudentProfile(student=stu) 

        profile.semester =request.POST.get("sem") 
        profile.language =request.POST.get("language")
        profile.tools =request.POST.get("tools")

        profile.board10 =request.POST.get("board10")
        profile.marks10 =request.POST.get("marks10")

        profile.board12 =request.POST.get("board12")
        profile.marks12 =request.POST.get("marks12")

        profile.graduation_college =request.POST.get("graduation")
        graduation_marks = request.POST.get("graduationMarks")
        profile.graduation_marks = request.POST.get("graduationMarks") if graduation_marks else None

        profile.post_graduation_college =request.POST.get("postGraduation")
        post_graduation_marks = request.POST.get("postGraduationMarks")
        profile.post_graduation_marks = request.POST.get("postGraduationMarks") if post_graduation_marks else None

        internship = request.POST.get("internship")
        profile.internship =request.POST.get("internship")
        profile.company =request.POST.get("companyName").upper() if internship == "yes" else None
        profile.duration =request.POST.get("duration") if internship == "yes" else None
        stipend = request.POST.get("stipend")
        profile.stipend = request.POST.get("stipend") if internship == "yes" and stipend else None
        profile.skills_gained =request.POST.get("skill_gained") if internship == "yes" and profile.internship else None
        
        project = request.POST.get("project") 
        profile.project = request.POST.get("project") 
        profile.project_details =request.POST.get("projectDetails") if project == "yes" else None
        profile.skills_learned =request.POST.get("learned_skills") if project == "yes" else None

        job_location = request.POST.get("jobLocation") 
        profile.job_location =request.POST.get("jobLocation")
        profile.other_location =request.POST.get("locationInput") if job_location == 'Other' else None

        profile.linkedin = request.POST.get("linkedin") or None
        profile.github = request.POST.get("github") or None

        if 'cv' in request.FILES:
            profile.resume = request.FILES['cv']

        profile.save()
        return redirect("/login/profile/")
        #We should change it to new url when deployed

    return render(request, "profile_update.html", {"info" : profile})


@login_required(login_url='/admin_login/')
def job_post(request):

    if request.method == "POST":
        title = request.POST.get("title")
        organization = request.POST.get("organization")
        location = request.POST.get("location")

        description = request.POST.get("description")

        placement_type = request.POST.get("placement_type")
        stipend = request.POST.get("stipend") or "N/A"
        package = request.POST.get("package") or "N/A"

        eligiblity_batch = request.POST.get("batch")
        eligiblity_10_mark = request.POST.get("min_marks10")
        eligiblity_12_mark = request.POST.get("min_marks12")
        eligible_college_mark = request.POST.get("min_marks_college")
        other_criteria = request.POST.get("Other_criteria") or "N/A"

        deadline = request.POST.get("deadline")

        question1 = request.POST.get("question1") or "N/A"
        question2 = request.POST.get("question2") or "N/A"
        question3 = request.POST.get("question3") or "N/A"
        question4 = request.POST.get("question4") or "N/A"
        question5 = request.POST.get("question5") or "N/A"
        question6 = request.POST.get("question6") or "N/A"
        question7 = request.POST.get("question7") or "N/A"
        question8 = request.POST.get("question8") or "N/A"
        question9 = request.POST.get("question9") or "N/A"
        question10 = request.POST.get("question10") or "N/A"

        type1 = request.POST.get("question1_type") or "N/A"
        type2 = request.POST.get("question2_type") or "N/A"
        type3 = request.POST.get("question3_type") or "N/A"
        type4 = request.POST.get("question4_type") or "N/A"
        type5 = request.POST.get("question5_type") or "N/A"
        type6 = request.POST.get("question6_type") or "N/A"
        type7 = request.POST.get("question7_type") or "N/A"
        type8 = request.POST.get("question8_type") or "N/A"
        type9 = request.POST.get("question9_type") or "N/A"
        type10 = request.POST.get("question10_type") or "N/A"
    
# Validate numeric fields
        if deadline:
            today = date.today()
            deadline_date = date.fromisoformat(deadline)
            if deadline_date < today:
                return render(request, "post_job.html", {"ERROR": "Deadline cannot be in the past"})
            else:
                deadline = deadline_date
        job_field = Job(
            title = title,
            organization = organization,
            location = location,

            description = description,

            placement_type = placement_type,
            job_stipend = stipend,
            package = package,

            eligiblity_batch = eligiblity_batch,
            eligiblity_10_marks = eligiblity_10_mark,
            eligiblity_12_marks = eligiblity_12_mark,
            eligiblity_college_marks = eligible_college_mark,
            eligiblity_others = other_criteria,

            application_deadline = deadline,

            question1 = question1,
            question2 = question2,
            question3 = question3,
            question4 = question4,
            question5 = question5,
            question6 = question6,
            question7 = question7,
            question8 = question8,
            question9 = question9,
            question10 = question10,

            type1 = type1,
            type2 = type2,
            type3 = type3,
            type4 = type4,
            type5 = type5,
            type6 = type6,
            type7 = type7,
            type8 = type8,
            type9 = type9,
            type10 = type10
        )
        job_field.save()
        messages.success(request, "Job added successfully!")
        return redirect('/thankyou/')  # Redirect to admin home after adding job
    return render(request, "post_job.html")


@login_required(login_url='/admin_login/')
def job_post_thankyou(request):
    return render(request, "job_post_thankyou.html")


@login_required(login_url='/admin_login/')
def view_jobs(request):

    today = timezone.now().date()
    Job.objects.filter(application_deadline__lt=today, active_status=True).update(active_status=False)
    job_list= Job.objects.all()
    
    return render(request, "view_jobs.html", {"job_list":job_list})


@login_required(login_url='/admin_login/')
def export_jobs(request):
    job_list = Job.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="job_posts.csv"'

    writer = csv.writer(response)
    writer.writerow(['Job ID',
                      'Title', 
                      'Organization',
                      'Job Location',
                      'Placement Type', 
                      'Stipend', 
                      'Package (in LPA)', 
                      'Eligibility Batch',
                      'Application Deadline', 
                      'Post Date'])

    for job in job_list:
        writer.writerow([
            job.job_id,
            job.title,
            job.organization,
            job.location,
            job.placement_type,
            job.job_stipend,
            job.package,
            job.eligiblity_batch,
            job.application_deadline,
            job.post_date,
        ])

    return response

@student_login_required
def job_application(request, job_id):
    job = get_object_or_404(Job, job_id=job_id)
    student_id = request.session.get("student_id")
    student = get_object_or_404(Student, sId=student_id)
    student_data = StudentProfile.objects.filter(student=student)
    application = JobApplication.objects.filter(job_id=job, sId=student).first()
    status = ApplicationStatus.objects.filter(application=application, student=student).first()

    # Check if already applied
    already_applied = JobApplication.objects.filter(job_id=job, sId=student).exists()
    if already_applied:
        return render(request, "already_applied.html", {"student": student, "status":status})

    if request.method == "POST":
        answer1 = request.POST.get("ans1") or None
        answer2 = request.POST.get("ans2") or None
        answer3 = request.POST.get("ans3") or None
        answer4 = request.POST.get("ans4") or None
        answer5 = request.POST.get("ans5") or None
        answer6 = request.POST.get("ans6") or None
        answer7 = request.POST.get("ans7") or None
        answer8 = request.POST.get("ans8") or None
        answer9 = request.POST.get("ans9") or None
        answer10 = request.POST.get("ans10") or None

        application_answer = JobApplication(
            job_id=job,
            sId=student,
            answer1=answer1,
            answer2=answer2,
            answer3=answer3,
            answer4=answer4,
            answer5=answer5,
            answer6=answer6,
            answer7=answer7,
            answer8=answer8,
            answer9=answer9,
            answer10=answer10
        )
        application_answer.save()
        return render(request, "application_thankyou.html")

    return render(request, "apply_job.html", {"the_job": job, "student": student, "data": student_data})


@login_required(login_url='/admin_login/')
def edit_job(request, job_id):
    job = get_object_or_404(Job, job_id=job_id)
    if request.method == "POST":
        job.title = request.POST.get("title")
        job.organization = request.POST.get("organization")
        job.location = request.POST.get("location")

        job.description = request.POST.get("description")

        job.placement_type = request.POST.get("placement_type")
        job.job_stipend = request.POST.get("stipend") or "N/A"
        job.package = request.POST.get("package") or "N/A"

        job.eligiblity_batch = request.POST.get("batch")
        job.eligiblity_10_marks = request.POST.get("min_marks10")
        job.eligiblity_12_marks = request.POST.get("min_marks12")
        job.eligiblity_college_marks = request.POST.get("min_marks_college")
        job.eligiblity_others = request.POST.get("Other_criteria") or "N/A"

        job.application_deadline = parse_date(request.POST.get("deadline"))

        job.question1 = request.POST.get("question1") or "N/A"
        job.question2 = request.POST.get("question2") or "N/A"
        job.question3 = request.POST.get("question3") or "N/A"
        job.question4 = request.POST.get("question4") or "N/A"
        job.question5 = request.POST.get("question5") or "N/A"
        job.question6 = request.POST.get("question6") or "N/A"
        job.question7 = request.POST.get("question7") or "N/A"
        job.question8 = request.POST.get("question8") or "N/A"
        job.question9 = request.POST.get("question9") or "N/A"
        job.question10 = request.POST.get("question10") or "N/A"

        job.type1 = request.POST.get("question1_type") or "N/A"
        job.type2 = request.POST.get("question2_type") or "N/A"
        job.type3 = request.POST.get("question3_type") or "N/A"
        job.type4 = request.POST.get("question4_type") or "N/A"
        job.type5 = request.POST.get("question5_type") or "N/A"
        job.type6 = request.POST.get("question6_type") or "N/A"
        job.type7 = request.POST.get("question7_type") or "N/A"
        job.type8 = request.POST.get("question8_type") or "N/A"
        job.type9 = request.POST.get("question9_type") or "N/A"
        job.type10 = request.POST.get("question10_type") or "N/A"

        job.update_date = date.today()

        today = timezone.now().date()
        if job.application_deadline >= today:
            job.active_status = True
        else:
            job.active_status=False

        job.save()
        messages.success(request, "Job Updates Successfully ")
        return redirect("/admin_home/view_jobs/")
    
    return render(request,"edit_job.html", {"job":job})


@login_required(login_url='/admin_login/')
def applied_student_list(request, job_id):
    # return HttpResponse("List of Students")

    job = get_object_or_404(Job, job_id=job_id)
    applications = JobApplication.objects.filter(job_id=job)

    status = ApplicationStatus.objects.filter(application__in=applications).select_related('application')
    status_dict = {s.application.application_id: s for s in status}
    
    for app in applications:
        app.status = status_dict.get(app.application_id)

    return render(request, "applied_students_list.html", {"job": job, "applications": applications})


@login_required(login_url='/admin_login/')
def export_applied_students(request ,job_id):
    job = Job.objects.get(job_id=job_id)
    application = JobApplication.objects.filter(job_id=job_id).select_related('sId', 'sId__studentprofile')

    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = f'attachment; filename= "student_list _for_{job.title} at {job.organization}.csv"'

    writer = csv.writer(response)

    writer.writerow(['Student ID',"Name","Email","Job title","organization","Placement type","CTC","Apply Date","Gender","Course","Semester","Passout Year","University","University City & State"])
    for i in application:
        profile = getattr(i.sId,'studentprofile',None)
        city_state = f"{i.sId.university_city}, {i.sId.university_state}" if i.sId.university_city and i.sId.university_state else ""
        
        if job.placement_type == "Internship":
            placement_info = f"Stipend: {job.job_stipend}"
        elif job.placement_type == "Full-time":
            placement_info = f"Package: {job.package} LPA"
        else:
            placement_info = f"Stipend: {job.job_stipend}, PPO: {job.package} LPA"

        writer.writerow([
            i.sId,
            i.sId.name,
            i.sId.email,
            job.title,
            job.organization,
            job.placement_type,
            placement_info,
            i.apply_date,
            i.sId.gender,
            i.sId.course,
            profile.semester,
            i.sId.passout_year,
            i.sId.university,
            city_state,
            
        ])
    return response


@login_required(login_url='/admin_login/')
def dashboard(request):
    return render(request,'dashboard.html')


@login_required(login_url='/admin_login/')
def status_update(request, job_id, application_id):
    job = Job.objects.get(job_id=job_id)
    application = JobApplication.objects.get(application_id=application_id)
    status, created = ApplicationStatus.objects.get_or_create(student=application.sId, application=application)

    if request.method == "POST":
        status.round1 = request.POST.get('round1')
        status.round2 = request.POST.get('round2')
        status.round3 = request.POST.get('round3')
        status.round4 = request.POST.get('round4')


        status.reason1 = request.POST.get('des1')
        status.reason2 = request.POST.get('des2')
        status.reason3 = request.POST.get('des3')  
        status.reason4 = request.POST.get('des4')

        status.feedback = request.POST.get('review') or None

        status.save()
        return redirect('applied_student_list', job_id=job_id)

    return render(request, "status_update.html",{"job":job, "application":application, "status":status})


@login_required(login_url='/admin_login/')
def table_download(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_upload_format.csv"'

    writer = csv.writer(response)

    # CSV header row
    writer.writerow(["Name", "Student_ID", "Phone_number", "Gender", "Course", "Passout_year", "University", "Specialization", "University_state", "University_city", "Email", "Password"])
    return response
