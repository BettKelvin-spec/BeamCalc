
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import generate_report,calculate_reactions, shear_force, bending_moment, plot_diagrams

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('calculate')  # Redirect after login
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to login page

@login_required
def calculate(request):
    if request.method == "POST":
        try:
            # Retrieve inputs
            length = float(request.POST.get("length", 0))
            point_load = float(request.POST.get("point_load", 0))
            point_load_position = float(request.POST.get("point_load_position", 0))
            udl = float(request.POST.get("udl", 0))
            support_condition = request.POST.get("support_condition", "simply_supported")

            # Validate inputs
            if length <= 0:
                return HttpResponse("Beam length must be greater than 0.", status=400)
            if point_load_position > length:
                return HttpResponse("Point load position cannot exceed beam length.", status=400)

            # Perform calculations
            reactions = calculate_reactions(length, point_load, point_load_position, udl, support_condition)
            shear = shear_force(length, point_load, point_load_position, udl, support_condition)
            bending = bending_moment(length, point_load, point_load_position, udl, support_condition)

            # Save data to session
            request.session['length'] = length
            request.session['point_load'] = point_load
            request.session['point_load_position'] = point_load_position
            request.session['udl'] = udl
            request.session['reactions'] = reactions
            request.session['shear'] = shear
            request.session['bending'] = bending
            request.session['support_condition'] = support_condition

            # Generate and save plots
            plot_diagrams(shear, bending, support_condition)

            # Generate downloadable report
            pdf_report = generate_report(
                length, point_load, point_load_position, udl, reactions, shear, bending, support_condition
            )

            # Render results page
            return render(request, "results.html", {
                "reactions": reactions,
                "shear": shear,
                "bending": bending,
                "report_url": pdf_report,
            })

        except ValueError:
            return HttpResponse("Invalid input values. Please check your entries.", status=400)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)

    # For GET requests, render the input form
    return render(request, "beam_input.html")


def landing_page(request):
    return render(request, 'landing_page.html')

from django.http import FileResponse
from .utils import generate_report

from django.http import FileResponse

def download_pdf(request):
    # Retrieve data from session
    length = request.session.get('length', 0)
    point_load = request.session.get('point_load', 0)
    point_load_position = request.session.get('point_load_position', 0)
    udl = request.session.get('udl', 0)
    reactions = request.session.get('reactions', {})
    shear = request.session.get('shear', ([0], [0]))
    bending = request.session.get('bending', ([0], [0]))
    support_condition = request.session.get('support_condition', "simply_supported")

    # Generate PDF
    pdf_buffer = generate_report(
        length, point_load, point_load_position, udl, reactions, shear, bending, support_condition
    )

    # Serve PDF as response
    return FileResponse(pdf_buffer, as_attachment=True, filename='Beam_Calculation_Report.pdf')

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')  # Redirect to login page after successful registration
        else:
            messages.error(request, 'There was an error in your registration.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
