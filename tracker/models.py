from django.db import models

class JobApplication(models.Model):
    STATUS_CHOICES=[
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Rejected', 'Rejected'),
    ]

    company_name=models.CharField(max_length=100) # Creates a column for the company name.
    position=models.CharField(max_length=100) # this will store the job title or position you applied for.
    application_date=models.DateField() # It accepts a date in YYYY-MM-DD format.
    status=models.CharField(max_length=20, choices=STATUS_CHOICES) # choices=STATUS_CHOICES ensures only valid values can be saved.

#FileField: Used for uploading files
    resume=models.FileField(upload_to='resumes/', blank=True, null=True)

#AFter adding the filefield in model we have to make migrate the database
#so in the terminal i did: python manage.py makemigrations(This will detect the new resume field and prepare a migration file)
#python manage.py migrate(This applies the changes to the database so your model can now accept uploaded resume files)


    def __str__(self):
        return f"{self.company_name} - {self.position}" # This defines how the object appears in the admin panel.
