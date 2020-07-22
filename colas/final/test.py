import unittest
from simulador import Simulador
import pprint

class TestSimulador(unittest.TestCase):
    # Estado servidores
    def test_estado_interno(self):
        sim = Simulador()
        sim.num_llamada_a_int = [1] * 10
        sim.tipo_llamada_interno = [True] * 10
        sim.set_estado_interno()
        self.assertEqual(["Atendiendo int. 1"] * 10, sim.estado_int)

        sim.num_llamada_a_int = [3] * 10
        sim.tipo_llamada_interno = [False] * 10
        sim.set_estado_interno()
        self.assertEqual(["Atendiendo ext. 3"] * 10, sim.estado_int)

        sim.tipo_llamada_interno = [None] * 10
        sim.set_estado_interno()
        self.assertEqual(["Libre"] * 10, sim.estado_int)

    def test_estado_linea_externa(self):
        sim = Simulador()

        sim.llamada_linea_externa = [False] * 3
        sim.set_estado_linea_externa()
        self.assertEqual(["Libre"] * 3, sim.estado_ext)

        sim.num_llamada_a_ext = [5] * 3
        sim.llamada_linea_externa = [True] * 3

        sim.set_estado_linea_externa()
        self.assertEqual(["Atendiendo 5"] * 3, sim.estado_ext)

    # Funciones random
    def test_set_rnd(self):
        sim = Simulador()
        sim.set_rnd(
            tiempo_llegada_int=[1, 2],
            tiempo_llegada_ext=[3, 4],
            duracion_int=[5, 6],
            duracion_ext=[7, 8],
            interno_origen=[9, 10],
            interno_destino=[11, 12],
            activo=True
        )
        self.assertEqual([1, 2], sim.listas_rnd['tiempo_llegada_int'])
        self.assertEqual([3, 4], sim.listas_rnd['tiempo_llegada_ext'])
        self.assertEqual([5, 6], sim.listas_rnd['duracion_int'])
        self.assertEqual([7, 8], sim.listas_rnd['duracion_ext'])
        self.assertEqual([9, 10], sim.listas_rnd['interno_origen'])
        self.assertEqual([11, 12], sim.listas_rnd['interno_destino'])

    def test_get_rnd(self):
        sim = Simulador()
        # Probar que genere numeros aleatoreos
        self.assertGreaterEqual(1, sim.get_rnd('tiempo_llegada_int'))
        self.assertLessEqual(0, sim.get_rnd('tiempo_llegada_int'))

        # Marcandolo como activo
        sim.set_rnd(activo=True)
        self.assertGreaterEqual(1, sim.get_rnd('tiempo_llegada_int'))
        self.assertLessEqual(0, sim.get_rnd('tiempo_llegada_int'))

        sim.set_rnd(
            tiempo_llegada_int=[1, 2],
            tiempo_llegada_ext=[3, 4],
            duracion_int=[5, 6],
            duracion_ext=[7, 8],
            interno_origen=[9, 10],
            interno_destino=[11, 12],
            activo=True
        )
        self.assertEqual(1, sim.get_rnd('tiempo_llegada_int'))
        self.assertEqual(2, sim.get_rnd('tiempo_llegada_int'))
        self.assertGreaterEqual(1, sim.get_rnd('tiempo_llegada_int'))
        self.assertLessEqual(0, sim.get_rnd('tiempo_llegada_int'))

        self.assertEqual(3, sim.get_rnd('tiempo_llegada_ext'))
        self.assertEqual(4, sim.get_rnd('tiempo_llegada_ext'))
        self.assertGreaterEqual(1, sim.get_rnd('tiempo_llegada_ext'))
        self.assertLessEqual(0, sim.get_rnd('tiempo_llegada_ext'))

        self.assertEqual(5, sim.get_rnd('duracion_int'))
        self.assertEqual(6, sim.get_rnd('duracion_int'))
        self.assertGreaterEqual(1, sim.get_rnd('duracion_int'))
        self.assertLessEqual(0, sim.get_rnd('duracion_int'))

        self.assertEqual(7, sim.get_rnd('duracion_ext'))
        self.assertEqual(8, sim.get_rnd('duracion_ext'))
        self.assertGreaterEqual(1, sim.get_rnd('duracion_ext'))
        self.assertLessEqual(0, sim.get_rnd('duracion_ext'))

        self.assertEqual(9, sim.get_rnd('interno_origen'))
        self.assertEqual(10, sim.get_rnd('interno_origen'))
        self.assertGreaterEqual(1, sim.get_rnd('interno_origen'))
        self.assertLessEqual(0, sim.get_rnd('interno_origen'))

        self.assertEqual(11, sim.get_rnd('interno_destino'))
        self.assertEqual(12, sim.get_rnd('interno_destino'))
        self.assertGreaterEqual(1, sim.get_rnd('interno_destino'))
        self.assertLessEqual(0, sim.get_rnd('interno_destino'))

        with self.assertRaises(ValueError):
            sim.get_rnd('otro_valor')

    def test_get_rnd_integer(self):
        sim = Simulador()
        self.assertEqual(1, sim.get_rnd_integer(0, 10))
        self.assertEqual(1, sim.get_rnd_integer(0.09999, 10))
        self.assertEqual(2, sim.get_rnd_integer(0.1, 10))
        self.assertEqual(2, sim.get_rnd_integer(0.19999, 10))
        self.assertEqual(10, sim.get_rnd_integer(0.9999, 10))
        # Nunca llega a 1
        self.assertEqual(11, sim.get_rnd_integer(1, 10))

        self.assertEqual(1, sim.get_rnd_integer(0.33333333, 3))
        self.assertEqual(2, sim.get_rnd_integer(0.33333334, 3))
        self.assertEqual(3, sim.get_rnd_integer(0.66666667, 3))

    # Atributos de la simulacion
    def test_set_proxima_llegada_int(self):
        sim = Simulador()
        sim.set_rnd(tiempo_llegada_int=[0.0463538119218031])
        sim.set_proxima_llegada_int()

        self.assertEqual(0.0463538119218031, sim.rnd_tiempo_llegada_int)
        self.assertAlmostEqual(0.09492509672, sim.tiempo_llegada_int, delta=0.000001)
        self.assertAlmostEqual(0.09492509672, sim.proxima_llegada_int, delta=0.000001)

    def test_set_proxima_llegada_ext(self):
        sim = Simulador()
        sim.set_rnd(tiempo_llegada_ext=[0.527674118744456])
        sim.set_proxima_llegada_ext()

        self.assertEqual(0.527674118744456, sim.rnd_tiempo_llegada_ext)
        self.assertAlmostEqual(3.750430526, sim.tiempo_llegada_ext, delta=0.000001)
        self.assertAlmostEqual(3.750430526, sim.proxima_llegada_ext, delta=0.000001)

    def test_set_fin_llamada_int(self):
        sim = Simulador()
        sim.set_rnd(duracion_int=[0.949147020851263, 0.482405844102685])
        sim.num_llamada_int_total = 3

        sim.set_fin_llamada_int()
        self.assertEqual(0.949147020851263, sim.rnd_duracion_int)
        self.assertAlmostEqual(3.84744106255379, sim.duracion_int, delta=0.000001)
        self.assertAlmostEqual(3.84744106255379, sim.fin_llamada, delta=0.000001)
        self.assertEqual({3: 3.847441062553789}, sim.fin_llamada_interna)

        sim.num_llamada_int_total = 4
        sim.set_fin_llamada_int()
        self.assertEqual({3: 3.847441062553789, 4: 2.4472175323080547}, sim.fin_llamada_interna)

    def test_set_fin_llamada_ext(self):
        sim = Simulador()
        sim.set_rnd(duracion_ext=[0.554989281341822, 0.583440963508874])
        sim.num_llamada_ext_total = 5

        sim.set_fin_llamada_ext()
        self.assertEqual(0.554989281341822, sim.rnd_duracion_ext)
        self.assertAlmostEqual(6.43991425073458, sim.duracion_ext, delta=0.000001)
        self.assertAlmostEqual(6.43991425073458, sim.fin_llamada, delta=0.000001)
        self.assertEqual({5: 6.439914250734576}, sim.fin_llamada_externa)

        sim.num_llamada_ext_total = 2
        sim.set_fin_llamada_ext()
        self.assertEqual({5: 6.439914250734576, 2: 6.667527708070992}, sim.fin_llamada_externa)

    def test_set_interno_origen(self):
        sim = Simulador()
        sim.set_rnd(interno_origen=[0.881222963703666, 0.777759066106611])

        sim.set_interno_origen()
        self.assertEqual(0.881222963703666, sim.rnd_interno_origen)
        self.assertAlmostEqual(9, sim.interno_origen, delta=0.000001)

        sim.set_interno_origen()
        self.assertAlmostEqual(8, sim.interno_origen, delta=0.000001)

    def test_set_interno_destino(self):
        sim = Simulador()
        sim.set_rnd(interno_destino=[0.536524711262778, 0.199421975971938])

        sim.set_interno_destino()
        self.assertEqual(0.536524711262778, sim.rnd_interno_destino)
        self.assertAlmostEqual(6, sim.interno_destino, delta=0.000001)

        sim.set_interno_destino()
        self.assertAlmostEqual(2, sim.interno_destino, delta=0.000001)

    def test_set_linea_externa(self):
        sim = Simulador()
        sim.set_rnd(linea_externa=[0.711000714835721, 0.445582430452375, 0.1, 0.1])

        sim.set_linea_externa()
        self.assertEqual(0.711000714835721, sim.rnd_linea_externa)
        self.assertAlmostEqual(3, sim.linea_externa, delta=0.0001)

        sim.set_linea_externa()
        self.assertAlmostEqual(2, sim.linea_externa, delta=0.0001)


        #con 1 ocupado
        sim.set_rnd(linea_externa=[0.1, 0.1, 0.1])

        sim.llamada_linea_externa = [True, False, False]
        sim.set_linea_externa()
        self.assertEqual(2, sim.linea_externa)

        sim.llamada_linea_externa = [False, True, False]
        sim.set_linea_externa()
        self.assertEqual(1, sim.linea_externa)

        sim.llamada_linea_externa = [False, False, True]
        sim.set_linea_externa()
        self.assertEqual(1, sim.linea_externa)

        # Con 1 libre
        sim.set_rnd(linea_externa=[0.9, 0.9, 0.9])

        sim.llamada_linea_externa = [True, True, False]
        sim.set_linea_externa()
        self.assertEqual(3, sim.linea_externa)

        sim.llamada_linea_externa = [True, False, True]
        sim.set_linea_externa()
        self.assertEqual(2, sim.linea_externa)

        sim.llamada_linea_externa = [False, True, True]
        sim.set_linea_externa()
        self.assertEqual(1, sim.linea_externa)

        # Cuando no hay disponibles
        sim.set_rnd(linea_externa=[0.9, .5, .1])

        sim.llamada_linea_externa = [True, True, True]
        sim.set_linea_externa()
        self.assertEqual(3, sim.linea_externa)

        sim.set_linea_externa()
        self.assertEqual(2, sim.linea_externa)

        sim.set_linea_externa()
        self.assertEqual(1, sim.linea_externa)

    # Guardar iteracion
    def test_guardar_iteracion(self):
        sim = Simulador()
        sim.guardar_iteracion()

        self.assertEqual(1, len(sim.iteraciones))
        sim.guardar_iteracion()
        self.assertEqual(2, len(sim.iteraciones))

    # Eventos
    def test_inicializacion(self):
        sim = Simulador()
        sim.set_rnd(tiempo_llegada_int=[0.0463538119218031], tiempo_llegada_ext=[0.527674118744456])

        sim.inicializacion()
        self.assertAlmostEqual(0.09492509672, sim.proxima_llegada_int, delta=0.000001)
        self.assertAlmostEqual(3.750430526, sim.proxima_llegada_ext, delta=0.000001)

        self.assertEqual(['Libre'] * 10, sim.estado_int)
        self.assertEqual(['Libre'] * 3, sim.estado_ext)

        # Estado
        self.assertEqual('Inicialización', sim.as_dict()['evento'])

    def test_get_evento(self):
        sim = Simulador()
        # Inicializacion
        self.assertEqual('Inicialización', sim.get_evento())

        # Interna
        sim.tipo_llamada_actual = True
        sim.num_llamada_int_total = 3
        sim.evento = 'llamada_interna'
        self.assertEqual('llamada_interna (3)', sim.get_evento())

        # Externa
        sim.tipo_llamada_actual = False
        sim.num_llamada_ext_total = 2
        sim.evento = 'llamada_externa'
        self.assertEqual('llamada_externa (2)', sim.get_evento())


    def test_set_proximo_evento(self):
        sim = Simulador()
        sim.proxima_llegada_int = 1
        sim.proxima_llegada_ext = 2
        sim.fin_llamada_interna = {1: 5, 2: 2.5}
        sim.fin_llamada_externa = {1: 3, 2: 6}

        sim.set_proximo_evento()
        self.assertEqual('llegada_llamada_interna', sim.evento)
        self.assertEqual(1, sim.reloj)

        sim.proxima_llegada_int = 10
        sim.set_proximo_evento()
        self.assertEqual('llegada_llamada_externa', sim.evento)
        self.assertEqual(2, sim.reloj)

        sim.proxima_llegada_ext = 15
        sim.set_proximo_evento()
        self.assertEqual('fin_llamada_interna', sim.evento)
        self.assertEqual(2.5, sim.reloj)

        sim.fin_llamada_interna = {1: 15, 2: 20}
        sim.set_proximo_evento()
        self.assertEqual('fin_llamada_externa', sim.evento)
        self.assertEqual(3, sim.reloj)

    def test_llegada_llamada_interna(self):
        sim = Simulador()
        sim.set_rnd(tiempo_llegada_int=[0.0463538119218031, 0.857985064561771],
                    tiempo_llegada_ext=[0.527674118744456, 0.847304643698668],
                    duracion_int=[0.949147020851263, 0.482405844102685],
                    duracion_ext=[0.554989281341822, 0.583440963508874],
                    interno_origen=[0.881222963703666, 0.777759066106611],
                    interno_destino=[0.536524711262778, 0.199421975971938],
                    linea_externa=[0.711000714835721, 0.445582430452375]
                    )
        # Inicializo todos los datos
        sim.inicializacion()
        sim.set_proximo_evento()
        sim.llegada_llamada_interna()
        # LLegadas
        self.assertAlmostEqual(3.99857119225736, sim.proxima_llegada_int, delta=0.000001)
        self.assertAlmostEqual(3.750430526, sim.proxima_llegada_ext, delta=0.000001)
        # Reloj
        self.assertAlmostEqual(0.0949250967186512, sim.reloj, delta=0.000001)
        # Estado
        self.assertEqual('llegada_llamada_interna', sim.evento)
        # Duracion
        # Resultados del historico
        self.assertAlmostEqual(3.84744106255379, sim.iteraciones[-1]['duracion_int'], delta=0.0001)
        self.assertAlmostEqual(3.94236615927244, sim.iteraciones[-1]['fin_llamada'], delta=0.0001)
        self.assertEqual({1: 3.9423661592724404}, sim.iteraciones[-1]['fin_llamada_interna'])
        self.assertEqual({}, sim.fin_llamada_externa)
        # Se deben eliminar los valores temporales
        self.assertEqual('', sim.rnd_duracion_int)
        self.assertEqual('', sim.duracion_int)
        self.assertEqual({1: 3.9423661592724404}, sim.fin_llamada_interna)


        #Resultados
        self.assertEqual(0, sim.llamadas_int_perdidas)
        self.assertEqual(1, sim.num_llamada_int_total)

        #Servidor
        # print(sim.tipo_llamada_interno, sim.num_llamada_a_int)
        self.assertEqual([None, None, None, None, None, True, None, None, True, None], sim.tipo_llamada_interno)
        self.assertEqual([0, 0, 0, 0, 0, 1, 0, 0, 1, 0], sim.num_llamada_a_int)
        self.assertEqual(['Libre', 'Libre', 'Libre', 'Libre', 'Libre', 'Atendiendo int. 1',
                          'Libre', 'Libre', 'Atendiendo int. 1', 'Libre'], sim.estado_int)

        #Objetos
        self.assertEqual({1: 'En proceso'}, sim.estado_llamada_int)
        self.assertEqual({}, sim.estado_llamada_ext)

        # LLamada perdida
        sim = Simulador()
        sim.set_rnd(tiempo_llegada_int=[0.0463538119218031, 0.857985064561771],
                    tiempo_llegada_ext=[0.527674118744456, 0.847304643698668],
                    duracion_int=[0.949147020851263, 0.482405844102685],
                    duracion_ext=[0.554989281341822, 0.583440963508874],
                    interno_origen=[0.881222963703666, 0.777759066106611],
                    interno_destino=[0.536524711262778, 0.199421975971938],
                    linea_externa=[0.711000714835721, 0.445582430452375]
                    )
        # Inicializo todos los datos
        sim.inicializacion()
        sim.set_proximo_evento()

        sim.tipo_llamada_interno = [None, None, None, None, None, True, None, None, True, None]
        sim.num_llamada_a_int = [0, 0, 0, 0, 0, 1, 0, 0, 1, 0]

        sim.llegada_llamada_interna()

        self.assertEqual([None, None, None, None, None, True, None, None, True, None], sim.tipo_llamada_interno)
        self.assertEqual([0, 0, 0, 0, 0, 1, 0, 0, 1, 0], sim.num_llamada_a_int)
        self.assertEqual(['Libre', 'Libre', 'Libre', 'Libre', 'Libre', 'Atendiendo int. 1',
                          'Libre', 'Libre', 'Atendiendo int. 1', 'Libre'], sim.estado_int)

        # print(sim.iteraciones[-1])
        # La llamada queda guardada como perdida por esa iteracion
        self.assertEqual({1: 'perdida'}, sim.iteraciones[-1]['estado_llamada_int'])
        # Pero es eliminada para las proximas iteraciones
        self.assertEqual({}, sim.estado_llamada_int)

        # Resultados
        self.assertEqual(1, sim.llamadas_int_perdidas)
        self.assertEqual(1, sim.num_llamada_int_total)

    def test_llegada_llamada_externa(self):
        sim = Simulador()
        sim.set_rnd(tiempo_llegada_int=[0.0463538119218031, 0.857985064561771],
                    tiempo_llegada_ext=[0.527674118744456, 0.847304643698668],
                    duracion_int=[0.949147020851263, 0.482405844102685],
                    duracion_ext=[0.554989281341822, 0.583440963508874],
                    interno_origen=[0.881222963703666, 0.777759066106611],
                    interno_destino=[0.536524711262778, 0.515272640056872],
                    linea_externa=[0.711000714835721, 0.445582430452375]
                    )
        # Inicializo todos los datos
        sim.inicializacion()
        sim.set_proximo_evento()
        sim.llegada_llamada_interna()
        sim.set_proximo_evento()
        sim.llegada_llamada_externa()

        # LLegadas
        self.assertAlmostEqual(3.99857119225736, sim.proxima_llegada_int, delta=0.000001)
        self.assertAlmostEqual(13.1469829153132, sim.proxima_llegada_ext, delta=0.000001)
        # Reloj
        self.assertAlmostEqual(3.75043052621183, sim.reloj, delta=0.000001)
        # Estado
        self.assertEqual('llegada_llamada_externa', sim.evento)

        # Duracion
        # Resultados del historico
        self.assertAlmostEqual(6.43991425073458, sim.iteraciones[-1]['duracion_ext'], delta=0.0001)
        self.assertAlmostEqual(10.1903447769464, sim.iteraciones[-1]['fin_llamada'], delta=0.0001)
        self.assertEqual({1: 10.190344776946413}, sim.iteraciones[-1]['fin_llamada_externa'])
        # Se deben eliminar los valores temporales
        self.assertEqual('', sim.rnd_duracion_ext)
        self.assertEqual('', sim.duracion_ext)
        self.assertEqual({1: 10.190344776946413}, sim.fin_llamada_externa)

        self.assertEqual(6, sim.iteraciones[-1]['interno_destino'])
        #Resultados
        self.assertEqual(1, sim.llamadas_ext_perdidas)
        self.assertEqual(1, sim.num_llamada_ext_total)

        #Servidor
        # print(sim.tipo_llamada_interno, sim.num_llamada_a_int)
        self.assertEqual([False, False, False], sim.llamada_linea_externa)
        self.assertEqual([0, 0, 0], sim.num_llamada_a_ext)
        self.assertEqual(['Libre', 'Libre', 'Libre'], sim.estado_ext)

        # La llamada queda guardada como perdida por esa iteracion
        self.assertEqual({1: 'perdida'}, sim.iteraciones[-1]['estado_llamada_ext'])
        # Pero es eliminada para las proximas iteraciones
        self.assertEqual({}, sim.estado_llamada_ext)

        # LLamada no perdida
        sim = Simulador()
        sim.set_rnd(tiempo_llegada_int=[0.0463538119218031, 0.857985064561771],
                    tiempo_llegada_ext=[0.527674118744456, 0.847304643698668],
                    duracion_int=[0.949147020851263, 0.482405844102685],
                    duracion_ext=[0.554989281341822, 0.583440963508874],
                    interno_origen=[0.881222963703666, 0.777759066106611],
                    interno_destino=[0.536524711262778, 0.015272640056872],
                    linea_externa=[0.711000714835721, 0.445582430452375]
                    )
        # Inicializo todos los datos
        sim.inicializacion()
        sim.set_proximo_evento()
        sim.llegada_llamada_interna()
        sim.set_proximo_evento()
        sim.llegada_llamada_externa()

        self.assertEqual(3, sim.iteraciones[-1]['linea_externa'])
        self.assertEqual(1, sim.iteraciones[-1]['interno_destino'])
        # Resultados
        self.assertEqual(0, sim.llamadas_ext_perdidas)
        self.assertEqual(1, sim.num_llamada_ext_total)

        # Servidor
        # print(sim.tipo_llamada_interno, sim.num_llamada_a_int)
        self.assertEqual([False, False, True], sim.llamada_linea_externa)
        self.assertEqual([0, 0, 1], sim.num_llamada_a_ext)
        self.assertEqual(['Libre', 'Libre', 'Atendiendo 1'], sim.estado_ext)

        self.assertEqual([False, None, None, None, None, True, None, None, True, None], sim.tipo_llamada_interno)
        self.assertEqual([1, 0, 0, 0, 0, 1, 0, 0, 1, 0], sim.num_llamada_a_int)
        self.assertEqual(['Atendiendo ext. 1', 'Libre', 'Libre', 'Libre', 'Libre', 'Atendiendo int. 1',
                          'Libre', 'Libre', 'Atendiendo int. 1', 'Libre'], sim.estado_int)

    def test_simular(self):
        sim = Simulador(cant_iteraciones=100)
        sim.simular()
        # self.assertEqual(21, len(sim.iteraciones))

        # sim = Simulador(cant_iteraciones=100)
        # sim.simular(1000000)
        # # self.assertEqual(41, len(sim.iteraciones))

        sim = Simulador()
        sim.set_rnd(tiempo_llegada_int=[0.0463538119218031, 0.857985064561771],
                    tiempo_llegada_ext=[0.527674118744456, 0.847304643698668],
                    duracion_int=[0.949147020851263, 0.482405844102685],
                    duracion_ext=[0.554989281341822, 0.583440963508874],
                    interno_origen=[0.881222963703666, 0.777759066106611],
                    interno_destino=[0.536524711262778, 0.015272640056872],
                    linea_externa=[0.711000714835721, 0.445582430452375]
                    )
        # sim.simular()
        # self.assertEqual('llegada_llamada_interna', sim.evento)
        # sim.simular(1)
        # self.assertEqual('llegada_llamada_externa', sim.evento)
        # sim.simular(1)
        # self.assertEqual('fin_llamada_interna', sim.evento)
