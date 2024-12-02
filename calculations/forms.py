from django import forms

class BeamInputForm(forms.Form):
    length = forms.FloatField(label="Beam Length (m)")
    point_load = forms.FloatField(label="Point Load (kN)", required=False)
    udl = forms.FloatField(label="UDL (kN/m)", required=False)
    support_type = forms.ChoiceField(choices=[('Fixed', 'Fixed'), ('Simply Supported', 'Simply Supported')], label="Support Type")
