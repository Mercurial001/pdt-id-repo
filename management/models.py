from datetime import timezone
from logging import fatal

from django.db import models


class Barangay(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Sitio(models.Model):
    brgy = models.ForeignKey(Barangay, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CivilStatus(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Religion(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Occupation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class EducationalAttainment(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SchoolName(models.Model):
    lvl = models.ForeignKey(EducationalAttainment, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class IndividualHouse(models.Model):
    residence = models.CharField(max_length=255)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    house = models.ImageField(null=True, blank=True, upload_to='houses/')

    def __str__(self):
        return self.residence


class Individual(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255)
    suffix = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    birthday = models.DateField()
    precinct_no = models.CharField(max_length=20, null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    brgy = models.ForeignKey(Barangay, on_delete=models.PROTECT, related_name='individual_brgy')
    sitio = models.ForeignKey(Sitio, on_delete=models.PROTECT, null=True, blank=True)
    civil_status = models.ForeignKey(CivilStatus, on_delete=models.PROTECT, null=True, blank=True)
    religion = models.ForeignKey(Religion, on_delete=models.PROTECT, null=True, blank=True)
    occupation = models.ForeignKey(Occupation, on_delete=models.PROTECT, null=True, blank=True)
    educational_attainment = models.ForeignKey(EducationalAttainment, on_delete=models.PROTECT, null=True, blank=True)
    schools = models.ManyToManyField(SchoolName, blank=True)
    house = models.ForeignKey(IndividualHouse, on_delete=models.PROTECT, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='individualImages/')

    # date_registered = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'
