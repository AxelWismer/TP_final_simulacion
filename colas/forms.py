from django import forms
from crispy_forms.helper import FormHelper

class ParametersForm_viejo(forms.Form):
    desde = forms.IntegerField(label='desde', initial=0, min_value=0)
    hasta = forms.IntegerField(label='hasta', initial=20, min_value=0)
    ultimas_filas = forms.IntegerField(label='ultimas filas', initial=10, min_value=0)
    tiempo = forms.IntegerField(label='tiempo', initial=60, min_value=0)

    # Salas
    capacidad_A = forms.IntegerField(label='capacidad sala A', initial=10, min_value=0)
    capacidad_B = forms.IntegerField(label='capacidad sala B', initial=10, min_value=0)
    capacidad_C = forms.IntegerField(label='capacidad sala C', initial=15, min_value=0)
    capacidad_D = forms.IntegerField(label='capacidad sala D', initial=15, min_value=0)

    def __init__(self, *args, **kwargs):
        super(ParametersForm_viejo, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.form_tag = False

class ParametersForm(forms.Form):
    desde = forms.FloatField(label='minuto de inicio (j)', initial=0, min_value=0)
    hasta = forms.IntegerField(label='iteraciones a mostrar (i)', initial=20, min_value=0)
    # ultimas_filas = forms.IntegerField(label='ultimas filas', initial=10, min_value=0)
    iteraciones = forms.FloatField(label='tiempo en minutos (X)', initial=100, min_value=0)

    # Interno
    media_int = forms.FloatField(label='media', initial=2, min_value=0)
    min_int = forms.FloatField(label='minimo', initial=1, min_value=0)
    max_int = forms.FloatField(label='maximo', initial=4, min_value=0)

    # Externo
    media_ext = forms.FloatField(label='media', initial=5, min_value=0)
    min_ext = forms.FloatField(label='minimo', initial=2, min_value=0)
    max_ext = forms.FloatField(label='maximo', initial=10, min_value=0)

    def __init__(self, *args, **kwargs):
        super(ParametersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.form_tag = False