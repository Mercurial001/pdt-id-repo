from datetime import datetime
from django.core.serializers import serialize
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.template.loader import render_to_string
from rest_framework.response import Response
from .models import Individual, Barangay, Gender, Religion, Occupation, CivilStatus, Sitio, EducationalAttainment
from . serializers import BarangaySerializer, SitioSerializer, GenderSerializer, \
    CivilStatusSerializer, ReligionSerializer, OccupationSerializer, \
    EducationalAttainmentSerializer, SchoolNameSerializer, IndividualHouseSerializer, \
    IndividualSerializer
from rest_framework.decorators import api_view
import requests
import qrcode
from cryptography.fernet import Fernet
from django.core.signing import Signer
import pdfkit
from id_repository import settings


def base(request):
    barangays = Barangay.objects.all()

    return render(request, 'base.html', {
        'barangays': barangays,
    })


def individual_all(request):
    individuals = Individual.objects.all()

    return render(request, 'individuals-page.html', {
        'individuals': individuals,
    })


def create_individual(request):
    barangays = Barangay.objects.all()
    genders = Gender.objects.all()
    religions = Religion.objects.all()
    occupations = Occupation.objects.all()
    civil_statuses = CivilStatus.objects.all()
    educational_lvl = EducationalAttainment.objects.all()

    # counters
    barangays_len = len(barangays)
    genders_len = len(genders)
    religions_len = len(religions)
    occupations_len = len(occupations)
    civil_statuses_len = len(civil_statuses)
    educational_lvl_len = len(educational_lvl)

    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        middle_name = request.POST.get('middle-name')
        last_name = request.POST.get('last-name')
        suffix = request.POST.get('suffix')
        birthday_str = request.POST.get('birthday')
        gender_str = request.POST.get('gender')
        civil_status_str = request.POST.get('civil-status')
        brgy_id = request.POST.get('brgy')
        religion_str = request.POST.get('religion')
        occupation_str = request.POST.get('occupation')
        educational_lvl_str = request.POST.get('educational-lvl')
        image = request.FILES.get('individual-img')
        sitio_str = request.POST.get('htmx-sitio')

        birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()

        brgy = Barangay.objects.get(id=brgy_id)

        if sitio_str == '':
            sitio = None
        elif sitio_str is None:
            sitio = None
        else:
            sitio, created_sitio = Sitio.objects.get_or_create(
                name=sitio_str,
                brgy=brgy
            )

        if gender_str == '':
            gender = None
        elif gender_str is None:
            gender = None
        else:
            gender, created_gender = Gender.objects.get_or_create(
                name=gender_str
            )

        if civil_status_str == '':
            civil_status = None
        elif civil_status_str is None:
            civil_status = None
        else:
            civil_status, created_cvs = CivilStatus.objects.get_or_create(
                name=civil_status_str
            )

        if religion_str == '':
            religion = None
        elif religion_str is None:
            religion = None
        else:
            religion, created_religion = Religion.objects.get_or_create(
                name=religion_str
            )

        if occupation_str == '':
            occupation = None
        elif occupation_str is None:
            occupation = None
        else:
            occupation, created_occupation = Occupation.objects.get_or_create(
                name=occupation_str
            )

        individual, created = Individual.objects.get_or_create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            suffix=suffix,
            birthday=birthday,
            brgy=brgy,
            gender=gender,
        )

        individual.sitio = sitio
        individual.civil_status = civil_status
        individual.religion = religion
        individual.occupation = occupation
        individual.image = image
        individual.save()

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )

        key = b'bSKEk2cT2V8vllCpMtQWsO2FxUVQdl3S_IHwBbEE4eQ='
        cipher_suite = Fernet(key)
        signing_key = b'Cold'
        signer = Signer(key=signing_key)

        # Commented 2/20/2024 encrypted_username = signer.sign(member.name) # 1st Encrypt the username
        encrypted_username = signer.sign(individual.id) # 1st Encrypt the username
        data = encrypted_username.encode('utf-8') # 2 Convert encrypted_username to bytes
        encrypted_data = cipher_suite.encrypt(data) # Final

        qr.add_data(encrypted_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        img.save(f'management/static/qr-codes/QR-Code-{individual.first_name}-{individual.middle_name}-{individual.last_name}-{individual.brgy}-{individual.id}.png')

        http_referrer = request.META.get('HTTP_REFERER')
        if http_referrer:
            return HttpResponseRedirect(http_referrer)
        else:
            return redirect('base')

    return render(request, 'create-individual.html', {
        'barangays': barangays,
        'genders': genders,
        'religions': religions,
        'occupations': occupations,
        'civil_statuses': civil_statuses,
        'educational_lvl': educational_lvl,
        # counters
        'barangays_len': barangays_len,
        'genders_len': genders_len,
        'religions_len': religions_len,
        'occupations_len': occupations_len,
        'civil_statuses_len': civil_statuses_len,
        'educational_lvl_len': educational_lvl_len,
    })


@api_view(['POST'])
def create_individual_api(request):
    data = request.data

    first_name = data['first_name'],
    middle_name = data['middle_name'],
    last_name = data['last_name'],
    suffix = data['suffix'],
    gender_str = data['gender'],
    brgy_name_raw = data['brgy'],
    sitio_str = data.get('sitio', ''),
    image = request.FILES.get('image'),
    birthday_str = data['birthday']
    civil_status_str = data['civil_status']
    religion_str = data['religion']
    occupation_str = data['occupation']


    birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()

    brgy_name = str(brgy_name_raw).replace("â", '-')
    brgy = Barangay.objects.get(name=brgy_name)

    if sitio_str == '':
        sitio = None
    elif sitio_str is None:
        sitio = None
    else:
        sitio, created_sitio = Sitio.objects.get_or_create(
            name=sitio_str,
            brgy=brgy
        )

    if gender_str == '':
        gender = None
    elif gender_str is None:
        gender = None
    else:
        gender, created_gender = Gender.objects.get_or_create(
            name=gender_str
        )

    if civil_status_str == '':
        civil_status = None
    elif civil_status_str is None:
        civil_status = None
    else:
        civil_status, created_cvs = CivilStatus.objects.get_or_create(
            name=civil_status_str
        )

    if religion_str == '':
        religion = None
    elif religion_str is None:
        religion = None
    else:
        religion, created_religion = Religion.objects.get_or_create(
            name=religion_str
        )

    if occupation_str == '':
        occupation = None
    elif occupation_str is None:
        occupation = None
    else:
        occupation, created_occupation = Occupation.objects.get_or_create(
            name=occupation_str
        )

    individual, created = Individual.objects.get_or_create(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        suffix=suffix,
        birthday=birthday,
        brgy=brgy,
        gender=gender,
    )

    individual.sitio = sitio
    individual.civil_status = civil_status
    individual.religion = religion
    individual.occupation = occupation
    individual.image = image
    individual.save()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )

    key = b'bSKEk2cT2V8vllCpMtQWsO2FxUVQdl3S_IHwBbEE4eQ='
    cipher_suite = Fernet(key)
    signing_key = b'Cold'
    signer = Signer(key=signing_key)

    # Commented 2/20/2024 encrypted_username = signer.sign(member.name) # 1st Encrypt the username
    encrypted_username = signer.sign(individual.id)  # 1st Encrypt the username
    data = encrypted_username.encode('utf-8')  # 2 Convert encrypted_username to bytes
    encrypted_data = cipher_suite.encrypt(data)  # Final

    qr.add_data(encrypted_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img.save(
        f'management/static/qr-codes/QR-Code-{individual.first_name}-{individual.middle_name}-{individual.last_name}-{individual.brgy}-{individual.id}.png')

    serializer = IndividualSerializer(individual, many=False)
    return Response(serializer.data)


# HTMX


def sitio_htmx(request):
    brgy_str = request.POST.get('brgy')
    brgy = Barangay.objects.get(id=brgy_str)
    if Sitio.objects.filter(brgy=brgy).exists():
        sitios = Sitio.objects.filter(brgy=brgy)
        sitios_len = len(sitios)
    else:
        sitios = None
        sitios_len = 0
    return render(request, 'htmx-templates/responsive-sitio.html', {
        'sitios': sitios,
        'sitios_len': sitios_len
    })

    # url = "https://genesisa.pythonanywhere.com/api/brgys-all/"
    #
    # # Send a GET request to the API
    # response = requests.get(url)
    # response.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)
    #
    # # Parse the JSON response
    # data = response.json()
    # for obj in data:
    #
    #     barangay, created = Barangay.objects.get_or_create(
    #         name=obj['brgy_name']
    #     )
    #     barangay.lat = obj['lat']
    #     barangay.long = obj['long']
    #     barangay.save()


def individual_ids_pdf(request):
    individuals = Individual.objects.all()
    root_directory = settings.BASE_DIR
    html = render_to_string('pdf/individual-ids.html', {
        'individuals': individuals,
        'root_directory': root_directory,
    })

    options = {
        'margin-top': '0',
        'margin-right': '0',
        'margin-bottom': '0',
        'margin-left': '0',
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'quiet': '',
        'print-media-type': '',
        'disable-smart-shrinking': '',
        'no-outline': '',
        'enable-local-file-access': ''
    }

    # config = pdfkit.configuration(wkhtmltopdf='C:/Users/kate/wkhtmltopdf/bin/wkhtmltopdf.exe')
    config = pdfkit.configuration(wkhtmltopdf='C:/Users/danda/wkhtmltopdf/bin/wkhtmltopdf.exe')

    pdf = pdfkit.from_string(html, False, options=options, configuration=config)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="individual-ids.pdf"'
    return response
