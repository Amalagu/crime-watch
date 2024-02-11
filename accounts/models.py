from django.db import models
from django.contrib.auth.models import User  # Import User model from django.contrib.auth

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


class Investigator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    logo = models.ImageField(null=True, blank=True, default='static/images/evidence.jpg')
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    specializations = models.ManyToManyField('Specialization', blank=True)
    
    def __str__(self):
        return self.name
    

class Specialization(models.Model):
    name = models.CharField(max_length=3, choices=select_category, unique=True)

    def __str__(self):
        return self.get_name_display()
