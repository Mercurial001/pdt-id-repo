from django.contrib import admin
from .models import Barangay
from .models import Sitio
from .models import Gender
from .models import CivilStatus
from .models import Religion
from .models import Occupation
from .models import EducationalAttainment
from .models import SchoolName
from .models import IndividualHouse
from .models import Individual


class BarangayAdmin(admin.ModelAdmin):
    list_display = ('name', )


class SitioAdmin(admin.ModelAdmin):
    list_display = ('name', )


class GenderAdmin(admin.ModelAdmin):
    list_display = ('name', )


class CivilStatusAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ReligionAdmin(admin.ModelAdmin):
    list_display = ('name', )


class OccupationAdmin(admin.ModelAdmin):
    list_display = ('name', )


class EducationalAttainmentAdmin(admin.ModelAdmin):
    list_display = ('name', )


class SchoolNameAdmin(admin.ModelAdmin):
    list_display = ('name', )


class IndividualHouseAdmin(admin.ModelAdmin):
    list_display = ('residence', )


class IndividualAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'brgy')


admin.site.register(Barangay, BarangayAdmin)
admin.site.register(Sitio, SitioAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(CivilStatus, CivilStatusAdmin)
admin.site.register(Religion, ReligionAdmin)
admin.site.register(Occupation, OccupationAdmin)
admin.site.register(EducationalAttainment, EducationalAttainmentAdmin)
admin.site.register(SchoolName, SchoolNameAdmin)
admin.site.register(IndividualHouse, IndividualHouseAdmin)
admin.site.register(Individual, IndividualAdmin)
