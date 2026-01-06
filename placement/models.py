from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    sId = models.CharField(max_length=50, primary_key=True, editable=False)   # student ID
    phone = PhoneNumberField(region = 'IN')
    gender = models.CharField(max_length=10)
    course = models.CharField(max_length=100)
    passout_year = models.SmallIntegerField()
    university = models.CharField(max_length=200)
    specialization = models.CharField(max_length=100)
    university_state = models.CharField(max_length=50)
    university_city = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)   # keep in plain text only for testing!
    verification_status_mail = models.BooleanField(default=False)
    verification_status_phone = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sId)
        #It show the name of the student in admin panel and then admin can easily identify the student.

class StudentProfile(models.Model): 
    # choices=[(value,label),(value,label)]
    #     value will be stored in Database, abd label will be shown in Admin Forms

    jobLocationChoices = [('PAN INDIA','PAN INDIA'),
                      ('Other','Other')
                      ]
    durationChoices = [('45 days','45 days'),
                   ('90 days','90 days'),
                   ('3-6 months','3-6 months'),
                   ('Currently Working','Currently Working')
                   ]
    yesNoChoices = [("yes", "yes"),
                ("no","no")
               ]
    student = models.OneToOneField(Student, on_delete=models.CASCADE)    # student ID
    '''Here we make the primary key of Student table as foreign key in StudentProfile.
        on_delete = models.CASCADE will CASCADE(delete all the related data) when the foreign/primary key
        is deleted'''
    semester = models.PositiveIntegerField()
    language = models.CharField(max_length=100)
    tools = models.CharField(max_length=100)
    board10 = models.CharField(max_length=50)
    board12 = models.CharField(max_length=50)
    marks10 = models.DecimalField(max_digits=5, decimal_places=2)
    marks12 = models.DecimalField(max_digits=5, decimal_places=2)

    graduation_college = models.CharField(max_length=200, blank=True, null=True)
    graduation_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    post_graduation_college = models.CharField(max_length=200, blank=True, null=True)
    post_graduation_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    internship = models.CharField(max_length=3, choices= yesNoChoices, default="no")
    company = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=20,choices=durationChoices, blank=True, null=True)
    stipend = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    skills_gained = models.CharField(max_length=200, blank=True, null=True)

    project = models.CharField(max_length=3, choices= yesNoChoices, default="no")
    project_details = models.TextField(blank=True, null=True)
    skills_learned = models.TextField(max_length=200, blank=True, null=True)

    job_location = models.CharField(max_length=10, choices=jobLocationChoices, default='PAN INDIA')
    other_location = models.CharField(max_length=50, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    github = models.URLField(max_length=200, blank=True, null=True)

    resume=models.FileField(upload_to='resumes/')

    def __str__(self):
        return f"{self.student.sId} - {self.student.name}"
        #It show the name of the student in admin panel and then admin can easily identify the student.

class Job(models.Model):
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    placement_type = models.CharField(max_length=50)
    job_stipend = models.CharField(max_length=50)
    package = models.CharField(max_length=50)
    eligiblity_batch = models.CharField(max_length=50)
    eligiblity_10_marks = models.DecimalField(max_digits=5, decimal_places=2)
    eligiblity_12_marks = models.DecimalField(max_digits=5, decimal_places=2)
    eligiblity_college_marks = models.DecimalField(max_digits=5, decimal_places=2)
    eligiblity_others = models.TextField()
    application_deadline = models.DateField()

    question1 = models.CharField(max_length=200, blank=True, null=True)
    question2 = models.CharField(max_length=200, blank=True, null=True)
    question3 = models.CharField(max_length=200, blank=True, null=True)
    question4 = models.CharField(max_length=200, blank=True, null=True)
    question5 = models.CharField(max_length=200, blank=True, null=True)
    question6 = models.CharField(max_length=200, blank=True, null=True)
    question7 = models.CharField(max_length=200, blank=True, null=True)
    question8 = models.CharField(max_length=200, blank=True, null=True)
    question9 = models.CharField(max_length=200, blank=True, null=True)
    question10 = models.CharField(max_length=200, blank=True, null=True)

    type1 = models.CharField(max_length=20, blank=True, null=True)
    type2 = models.CharField(max_length=20, blank=True, null=True)
    type3 = models.CharField(max_length=20, blank=True, null=True)
    type4 = models.CharField(max_length=20, blank=True, null=True)
    type5 = models.CharField(max_length=20, blank=True, null=True)
    type6 = models.CharField(max_length=20, blank=True, null=True)
    type7 = models.CharField(max_length=20, blank=True, null=True)
    type8 = models.CharField(max_length=20, blank=True, null=True)
    type9 = models.CharField(max_length=20, blank=True, null=True)
    type10 = models.CharField(max_length=20, blank=True, null=True)

    post_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(blank=True, null=True)
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.job_id)
    
class JobApplication(models.Model):
    application_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    sId = models.ForeignKey(Student, on_delete=models.CASCADE)
    apply_date = models.DateField(auto_now_add=True)
    answer1 = models.TextField(blank=True, null=True)
    answer2 = models.TextField(blank=True, null=True)
    answer3 = models.TextField(blank=True, null=True)
    answer4 = models.TextField(blank=True, null=True)
    answer5 = models.TextField(blank=True, null=True)
    answer6 = models.TextField(blank=True, null=True)
    answer7 = models.TextField(blank=True, null=True)
    answer8 = models.TextField(blank=True, null=True)
    answer9 = models.TextField(blank=True, null=True)
    answer10 = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.application_id)

class ApplicationStatus(models.Model):
    application = models.OneToOneField(JobApplication, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    round1 = models.CharField(max_length=20, null=True, blank=True)
    round2 = models.CharField(max_length=20, null=True, blank=True)
    round3 = models.CharField(max_length=20, null=True, blank=True)
    round4 = models.CharField(max_length=20, null=True, blank=True)
    
    reason1= models.CharField(max_length=200, null=True, blank=True)
    reason2= models.CharField(max_length=200, null=True, blank=True)
    reason3= models.CharField(max_length=200, null=True, blank=True)
    reason4= models.CharField(max_length=200, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    feedback = models.TextField(null=True, blank=True)

 
    def __str__(self):
        return f"Status of {self.application.application_id}: {self.student.name}"