def calculate_reactions(length, point_load=None, point_load_position=None, udl=None):
    """Calculate support reactions for a simply supported beam."""
    if udl:
        # Uniformly Distributed Load (UDL)
        reaction = udl * length / 2
        return reaction, reaction  # R1 and R2 are equal for symmetrical UDL

    elif point_load and point_load_position:
        # Point Load
        R1 = point_load * (length - point_load_position) / length
        R2 = point_load * point_load_position / length
        return R1, R2

    return 0, 0

def shear_force(length, point_load=None, point_load_position=None, udl=None):
    """Calculate shear force values along the beam."""
    x_vals = []
    shear_vals = []
    if udl:
        for x in range(0, int(length + 1)):
            shear_value = udl * (length / 2 - x)
            x_vals.append(x)
            shear_vals.append(shear_value)
    elif point_load and point_load_position:
        for x in range(0, int(length + 1)):
            if x < point_load_position:
                shear_value = point_load * (length - point_load_position) / length
            else:
                shear_value = -point_load * point_load_position / length
            x_vals.append(x)
            shear_vals.append(shear_value)
    return x_vals, shear_vals


def bending_moment(length, point_load=None, point_load_position=None, udl=None):
    """Calculate bending moment values along the beam."""
    x_vals = []
    moment_vals = []
    if udl:
        for x in range(0, int(length + 1)):
            moment_value = (udl * x * (length - x)) / 2
            x_vals.append(x)
            moment_vals.append(moment_value)
    elif point_load and point_load_position:
        for x in range(0, int(length + 1)):
            if x < point_load_position:
                moment_value = (point_load * (length - point_load_position) * x) / length
            else:
                moment_value = (point_load * point_load_position * (length - x)) / length
            x_vals.append(x)
            moment_vals.append(moment_value)
    return x_vals, moment_vals

import matplotlib.pyplot as plt
from io import BytesIO
import base64

def plot_diagrams(shear_data, moment_data):
    """Generate SFD and BMD plots."""
    x_shear, y_shear = shear_data
    x_moment, y_moment = moment_data

    # Create subplots
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))

    # Plot SFD
    axs[0].plot(x_shear, y_shear, label='Shear Force', color='blue')
    axs[0].set_title('Shear Force Diagram (SFD)')
    axs[0].set_xlabel('Beam Length (m)')
    axs[0].set_ylabel('Shear Force (kN)')
    axs[0].grid(True)
    axs[0].legend()

    # Plot BMD
    axs[1].plot(x_moment, y_moment, label='Bending Moment', color='red')
    axs[1].set_title('Bending Moment Diagram (BMD)')
    axs[1].set_xlabel('Beam Length (m)')
    axs[1].set_ylabel('Bending Moment (kNm)')
    axs[1].grid(True)
    axs[1].legend()

    # Save plots to a BytesIO object
    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close(fig)
    return image_base64

from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(beam_data, shear_data, moment_data):
    """
    Generate a PDF report for the beam calculations.
    :param beam_data: Dictionary containing beam inputs.
    :param shear_data: Tuple containing x and y values for shear force.
    :param moment_data: Tuple containing x and y values for bending moment.
    :return: BytesIO object with PDF content.
    """
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 800, "Beam Calculation Report")

    # Beam Input Data
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 750, "Beam Inputs:")
    y = 730
    for key, value in beam_data.items():
        pdf.drawString(70, y, f"{key.capitalize()}: {value}")
        y -= 20

    # Shear Force Data
    pdf.drawString(50, y - 20, "Shear Force Data (SFD):")
    y -= 40
    for x, sf in zip(*shear_data):
        pdf.drawString(70, y, f"Position: {x:.2f} m, Shear Force: {sf:.2f} kN")
        y -= 20
        if y < 100:  # Avoid overflow
            pdf.showPage()
            y = 800

    # Bending Moment Data
    pdf.drawString(50, y - 20, "Bending Moment Data (BMD):")
    y -= 40
    for x, bm in zip(*moment_data):
        pdf.drawString(70, y, f"Position: {x:.2f} m, Moment: {bm:.2f} kNm")
        y -= 20
        if y < 100:  # Avoid overflow
            pdf.showPage()
            y = 800

    # Save and close
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
