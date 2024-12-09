def calculate_reactions(length, point_load=None, point_load_position=None, udl=None, support_condition=None):
    if support_condition == "simply_supported":
        if udl:
            reaction = udl * length / 2
            return reaction, reaction
        elif point_load and point_load_position:
            R1 = point_load * (length - point_load_position) / length
            R2 = point_load * point_load_position / length
            return R1, R2
    elif support_condition == "cantilever":
        if udl:
            R1 = udl * length
            return R1, 0  # Cantilever has one support
        elif point_load and point_load_position:
            R1 = point_load
            return R1, 0
    # Add logic for fixed beams or other conditions as needed
    return 0, 0



def shear_force(length, point_load=None, point_load_position=None, udl=None, support_condition="simply_supported"):
    """Calculate shear force values along the beam."""
    shear = []
    if support_condition == "simply_supported":
        if udl:
            for x in range(0, int(length + 1)):
                shear_value = udl * (length / 2 - x)
                shear.append((x, shear_value))

        elif point_load and point_load_position:
            for x in range(0, int(length + 1)):
                if x < point_load_position:
                    shear_value = point_load * (length - point_load_position) / length
                else:
                    shear_value = -point_load * point_load_position / length
                shear.append((x, shear_value))

    elif support_condition == "cantilever":
        if udl:
            for x in range(0, int(length + 1)):
                shear_value = udl * (length - x)
                shear.append((x, shear_value))

        elif point_load and point_load_position:
            for x in range(0, int(length + 1)):
                shear_value = point_load if x < point_load_position else 0
                shear.append((x, shear_value))

    return shear


def bending_moment(length, point_load=None, point_load_position=None, udl=None, support_condition="simply_supported"):
    """Calculate bending moment values along the beam."""
    moment = []
    if support_condition == "simply_supported":
        if udl:
            for x in range(0, int(length + 1)):
                moment_value = (udl * x * (length - x)) / 2
                moment.append((x, moment_value))

        elif point_load and point_load_position:
            for x in range(0, int(length + 1)):
                if x < point_load_position:
                    moment_value = (point_load * (length - point_load_position) * x) / length
                else:
                    moment_value = (point_load * point_load_position * (length - x)) / length
                moment.append((x, moment_value))

    elif support_condition == "cantilever":
        if udl:
            for x in range(0, int(length + 1)):
                moment_value = udl * (length - x) * x / 2
                moment.append((x, moment_value))

        elif point_load and point_load_position:
            for x in range(0, int(length + 1)):
                moment_value = point_load * (length - x) if x <= point_load_position else 0
                moment.append((x, moment_value))

    return moment


import matplotlib.pyplot as plt
from io import BytesIO
import base64

def plot_diagrams(shear, bending, support_condition):
    plt.figure(figsize=(12, 6))

    # Plot Shear Force Diagram (SFD)
    plt.subplot(1, 2, 1)
    x, y = zip(*shear)
    plt.plot(x, y, label="SFD")
    plt.title(f"Shear Force Diagram ({support_condition})")
    plt.xlabel("Beam Length")
    plt.ylabel("Shear Force")
    plt.grid(True)

    # Plot Bending Moment Diagram (BMD)
    plt.subplot(1, 2, 2)
    x, y = zip(*bending)
    plt.plot(x, y, label="BMD")
    plt.title(f"Bending Moment Diagram ({support_condition})")
    plt.xlabel("Beam Length")
    plt.ylabel("Bending Moment")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("calculations/static/plots/beam_diagrams.png")
    plt.close()

from reportlab.pdfgen import canvas
from io import BytesIO
from fpdf import FPDF

def generate_report(length, point_load, point_load_position, udl, reactions, shear, bending, support_condition):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Beam Calculation Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(0, 10, f"Support Condition: {support_condition}", ln=True)
    pdf.cell(0, 10, f"Beam Length: {length} m", ln=True)
    if point_load:
        pdf.cell(0, 10, f"Point Load: {point_load} N at {point_load_position} m", ln=True)
    if udl:
        pdf.cell(0, 10, f"UDL: {udl} N/m", ln=True)
    pdf.cell(0, 10, f"Reactions: R1 = {reactions[0]} N, R2 = {reactions[1]} N", ln=True)

    # Attach plot image
    pdf.image("calculations/static/plots/beam_diagrams.png", x=10, y=80, w=180)

    pdf_path = "calculations/static/reports/beam_report.pdf"
    pdf.output(pdf_path)
    return pdf_path
