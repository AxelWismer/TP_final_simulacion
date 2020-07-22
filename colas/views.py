from django.shortcuts import render
from django.views import generic

from .forms import ParametersForm
from .final.simulador import Simulador

class Colas(generic.FormView):
    form_class = ParametersForm
    template_name = 'colas/colas.html'

    def form_valid(self, form):
        desde = form.cleaned_data['desde']
        hasta = form.cleaned_data['hasta']

        sim = Simulador(j_hora=desde,
                        i_iteraciones=hasta,
                        cant_iteraciones=int(form.cleaned_data['iteraciones']),
                        media_int=form.cleaned_data['media_int'],
                        min_int=form.cleaned_data['min_int'],
                        max_int=form.cleaned_data['max_int'],
                        media_ext=form.cleaned_data['media_ext'],
                        min_ext=form.cleaned_data['min_ext'],
                        max_ext=form.cleaned_data['max_ext'],
                        )

        # Valores de prueba
        # sim.set_rnd(tiempo_llegada_int=[0.0463538119218031, 0.857985064561771, 0.908451102090196, 0.75555589975662,
        #                                 0.735796909342202, 0.350421703262134, 0.35809117433747],
        #             tiempo_llegada_ext=[0.527674118744456, 0.847304643698668, 0.275539224087359, 0.466184990913348],
        #             duracion_int=[0.949147020851263, 0.482405844102685, 0.996124218173933, 0.949899866287571,
        #                           0.363016984267217, 0.743025721511532],
        #             duracion_ext=[0.554989281341822, 0.583440963508874, 0.32849847758656],
        #             interno_origen=[0.881222963703666, 0.777759066106611, 0.362784188126309, 0.139547118630271,
        #                             0.589568168586502, 0.236712018601788],
        #             interno_destino=[0.536524711262778, 0.515272640056872, 0.199421975971938, 0.289331057002869,
        #                              0.605284036903027, 0.978562821912276, 0.0263739028065936, 0.283496541543839,
        #                              0.726281148429707],
        #             linea_externa=[0.711000714835721, 0.445582430452375, 0.337732484333726]
        #             )
        sim.simular()

        # Se realizan las simulaciones requeridas
        if sim.num_llamada_int_total > 0:
            porc_int = round((sim.llamadas_int_perdidas / sim.num_llamada_int_total) * 100, 4)
        else:
            porc_int = 0
        if sim.num_llamada_ext_total > 0:
            porc_ext = round((sim.llamadas_ext_perdidas / sim.num_llamada_ext_total) * 100, 4)
        else:
            porc_ext = 0
        if (sim.num_llamada_int_total + sim.num_llamada_ext_total) > 0:
            porc_total = round(((sim.llamadas_int_perdidas + sim.llamadas_ext_perdidas) /
                   (sim.num_llamada_int_total + sim.num_llamada_ext_total)) * 100, 4)
        else:
            porc_total = 0
        context = {
            'tabla': sim.iteraciones,
            'form': form,
            'llamadas_internas': sim.get_llamadas_guardadas_int(),
            'llamadas_externas': sim.get_llamadas_guardadas_ext(),
            'perdidas_int': sim.llamadas_int_perdidas,
            'perdidas_ext': sim.llamadas_ext_perdidas,
            'totales_int': sim.num_llamada_int_total,
            'totales_ext': sim.num_llamada_ext_total,
            'porc_int': porc_int,
            'porc_ext': porc_ext,
            'llamadas_total': sim.num_llamada_int_total + sim.num_llamada_ext_total,
            'perdidas_total': sim.llamadas_int_perdidas + sim.llamadas_ext_perdidas,
            'porc_total': porc_total,
        }

        # tabla.insert(len(it.tabla), {})
        # tabla.insert(len(it.tabla), {})

        return render(self.request, template_name=self.template_name, context=context)