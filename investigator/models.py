
from django.db import models
from accounts.models import Investigator

# Create your models here.

select_category = (
     ('TAR', 'Theft and Robbery'),
     ('B', 'Burglary'),
     ('PR', 'Offence against Property'),
     ('SO', 'Sexual offence'),
     ('MVO', 'Motor vehicle offence'),
     ('FD', 'Forced disappearance'),
     ('P', 'Piracy'),
     ('SS', 'Sexual slavery'),
     ('CL', 'Child labour'),
     ('DRC', 'Drug related case'),
     ('K', 'Kidnapping'),
     ('FI', 'False Imprisonment'),
     ('MC', 'Murder Case'),
     ('O', 'other'),
    ('ASA', 'Assault and Battery'),
    ('VND', 'Vandalism'),
    ('FRD', 'Fraud'),
    ('DNM', 'Drug Manufacturing'),
    ('DV', 'Domestic Violence'),
    ('ARS', 'Arson'),
    ('HRS', 'Homicide'),
    ('ECP', 'Embezzlement'),
    ('HSM', 'Harassment'),
    ('DUI', 'Driving Under the Influence'),
    ('SCX', 'Sexual Coercion'),
    ('CYP', 'Cyberbullying'),
    ('WFS', 'Weapons Offense'),
    ('HBT', 'Human Trafficking'),
)

report_status = (
    ('VALID', 'VALID'),
    ('ACTIVE', 'ACTIVE'),
    ('DISMISSED', 'DISMISSED')
)

class Report(models.Model):
    title = models.CharField(max_length=500)
    photo = models.ImageField(null=True, blank=True)
    category = models.CharField(max_length=3, choices=select_category) 
    description = models.TextField()
    reporter = models.CharField(max_length=200)
    incident_date = models.DateField()
    incident_time = models.TimeField()
    approved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=report_status, default='VALID') 


    def __str__(self):
        return f"{self.incident_date} - {self.title}"

class Case(models.Model):
    number = models.CharField(max_length=50, null=True, blank=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    investigator = models.ForeignKey(Investigator, on_delete=models.CASCADE )
    authorization_letter = models.ImageField(null=True, blank=True)
    time_opened = models.DateTimeField(auto_now_add=True)
    time_closed = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    isdismissed = models.BooleanField(default=False, blank=True, null=True)
    isresolved = models.BooleanField(default=False, blank=True, null=True)

    def get_case_number(self):
        return f"CS/{self.id}I{self.investigator.id}/RP/{self.report.id}"
    
    def save(self, *args, **kwargs):
        self.number = self.get_case_number()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.time_closed: 
            closed_date = f"to {self.time_closed}"
        else:
            closed_date = ''
        return f"{self.investigator.name} | {self.number} | {self.time_opened} {closed_date}"


class Timeline(models.Model):
    date=models.DateField(auto_now_add=True)
    description = models.TextField()
    case = models.ForeignKey(Case, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.case.number} - {self.description}"


class Evidence(models.Model):
    serial_no = models.CharField(max_length=20, null=True, blank=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='evidences', null=True, blank=True)
    title = models.CharField(max_length=100)
    scene_description = models.TextField()
    photo = models.ImageField( null=True, blank=True)
    acquisition_date = models.DateField()
    acquisition_time = models.TimeField()
    acquisition_by = models.CharField(max_length=200)
    acquisition_tools = models.CharField(max_length=255)
    packaging = models.CharField(max_length=255, null=True, blank=True)
    packaged_by = models.CharField(max_length=255, null=True, blank=True)
    transported_by = models.CharField(max_length=255, null=True, blank=True)
    examiner = models.CharField(max_length=255, null=True, blank=True)
    examination_tools = models.CharField(max_length=255, null=True, blank=True)
    examination_time = models.TimeField(null=True, blank=True)
    examination_date = models.DateField(null=True, blank=True)
    evidence_analysis = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.serial_no} - Evidence of: {self.title}"


    def get_serial_no(self):
        return f"EV/{self.id}/{self.case.number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.serial_no = self.get_serial_no()
        super().save(*args, **kwargs)
