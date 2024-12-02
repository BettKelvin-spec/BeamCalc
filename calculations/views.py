from django.shortcuts import render
from .utils import shear_force, bending_moment, plot_diagrams

def calculate(request):
    if request.method == 'POST':
        length = float(request.POST['length'])
        point_load = request.POST.get('point_load')
        point_load_position = request.POST.get('point_load_position')
        udl = request.POST.get('udl')

        point_load = float(point_load) if point_load else None
        point_load_position = float(point_load_position) if point_load_position else None
        udl = float(udl) if udl else None

        shear_data = shear_force(length, point_load, point_load_position, udl)
        moment_data = bending_moment(length, point_load, point_load_position, udl)

        diagram_image = plot_diagrams(shear_data, moment_data)

        context = {
            'shear_data': shear_data,
            'moment_data': moment_data,
            'diagram_image': diagram_image,
        }
        return render(request, 'results.html', context)
    return render(request, 'beam_input.html')

def landing_page(request):
    return render(request, 'landing_page.html')

from django.http import FileResponse
from .utils import generate_pdf

def download_pdf(request):
    # Mock input and calculation data (replace with real data from session or DB)
    beam_data = {
        "length": request.session.get('length', 10),
        "point_load": request.session.get('point_load', 20),
        "udl": request.session.get('udl', 5),
    }
    shear_data = request.session.get('shear_data', ([0, 5, 10], [10, 0, -10]))
    moment_data = request.session.get('moment_data', ([0, 5, 10], [0, 25, 0]))

    # Generate PDF
    pdf_buffer = generate_pdf(beam_data, shear_data, moment_data)

    # Serve PDF as response
    return FileResponse(pdf_buffer, as_attachment=True, filename='Beam_Calculation_Report.pdf')
