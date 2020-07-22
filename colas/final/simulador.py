import pprint
from random import random
import math
import copy

class Simulador:
    def __init__(self, media_int=2, min_int=1, max_int=4, media_ext=5, min_ext=2, max_ext=10,
                 rango_iteracion=((0,20), 20), cant_iteraciones=0, decimales=4, i_iteraciones=20, j_hora=0):
        # Parametros de las distribuciones
        # LLamada interna
        self.media_int = media_int
        self.min_int = min_int
        self.max_int = max_int

        # LLamada externa
        self.media_ext = media_ext
        self.min_ext = min_ext
        self.max_ext = max_ext

        # Variables de la simulacion
        self.evento = "Inicialización"
        self.reloj = 0

        # LLamada interna
        self.rnd_tiempo_llegada_int = ''
        self.tiempo_llegada_int = ''
        self.proxima_llegada_int = ''
        self.rnd_duracion_int = ''
        self.duracion_int = ''
        self.rnd_interno_origen = ''
        self.interno_origen = ''

        # LLamada externa
        self.rnd_tiempo_llegada_ext = ''
        self.tiempo_llegada_ext = ''
        self.proxima_llegada_ext = ''
        self.rnd_duracion_ext = ''
        self.duracion_ext = ''
        self.rnd_linea_externa = ''
        self.linea_externa = ''

        # LLamada
        self.rnd_interno_destino = ''
        self.interno_destino = ''

        # Fin llamada interna (i)
        self.fin_llamada = ''
        self.fin_llamada_interna = dict()
        self.fin_llamada_externa = dict()

        # Objetos
        # Servidores

        # Numero de llamada del interno
        self.num_llamada_a_int = [0] * 10
        # None significa libre
        self.tipo_llamada_interno = [None] * 10
        self.num_llamada_a_ext = [0] * 3
        # False significa libre
        self.llamada_linea_externa = [False] * 3

        # Estado (lo que realmente se guarda)
        self.estado_int = [''] * 10
        self.estado_ext = [''] * 3

        # Objetos
        # Estado llamadas
        self.estado_llamada_int = dict()
        self.estado_llamada_ext = dict()

        # Auxiliares:
        self.tipo_llamada_actual = None

        self.num_llamada_int_actual = 0
        self.num_llamada_ext_actual = 0

        # Resultados
        self.llamadas_int_perdidas = 0
        self.llamadas_ext_perdidas = 0
        self.num_llamada_int_total = 0
        self.num_llamada_ext_total = 0

        # Variables de programacion

        self.listas_rnd = {
            'tiempo_llegada_int': [],
            'tiempo_llegada_ext': [],
            'duracion_int': [],
            'duracion_ext': [],
            'interno_origen': [],
            'linea_externa': [],
            'interno_destino': [],
            'activo': False
        }
        # Formato ((inicio, fin), ultimas filas)
        self.rango_iteracion = rango_iteracion
        # iteraciones
        self.iteraciones = []
        self.num_iteracion = 0
        self.cantidad_iteraciones = cant_iteraciones

        self.decimales = decimales
        self.llamadas_guardadas_int = set()
        self.llamadas_guardadas_ext = set()

        self.i_iteraciones = i_iteraciones
        self.j_hora = j_hora
        self.iteraciones_guardadas = 0
        self.ultima_iteracion = None
        self.ante_ultima_iteracion = None

    def set_estado_interno(self):
        """Devuelve el estado de los internos con el numero y tipo de llamada que esta atendiendo"""
        for id in range(10):
            if self.tipo_llamada_interno[id] is None:
                self.estado_int[id] = "Libre"
            elif self.tipo_llamada_interno[id]:
                self.estado_int[id] = f"Atendiendo int. {self.num_llamada_a_int[id]}"
            else:
                self.estado_int[id] = f"Atendiendo ext. {self.num_llamada_a_int[id]}"

    def set_estado_linea_externa(self):
        """Devuelve el estado de las lineas externas con el numero de llamada que esta atendiendo"""
        for id in range(3):
            if self.llamada_linea_externa[id] is False:
                self.estado_ext[id] = "Libre"
            else:
                self.estado_ext[id] = f"Atendiendo {self.num_llamada_a_ext[id]}"

    def as_dict(self):
        """Guarda un diccionario con todos los valores de la iteracion actual"""
        # Crea un copia profunda de los elementos, es decir que las modificaciones posteriores
        # No afectaran al historico que se guarde
        dic = copy.deepcopy(self.__dict__)
        dic['evento'] = str(self.get_evento())
        # Exluidos
        dic.pop("media_int")
        dic.pop("min_int")
        dic.pop("max_int")
        dic.pop("media_ext")
        dic.pop("min_ext")
        dic.pop("max_ext")
        dic.pop("listas_rnd")
        dic.pop("num_llamada_int_actual")
        dic.pop("num_llamada_ext_actual")
        dic.pop("rango_iteracion")
        dic.pop("iteraciones")
        dic.pop("decimales")

        # Redondea todos los valores antes guardarlo
        for key in dic:
            if type(dic[key]) == float:
                dic[key] = round(dic[key], self.decimales)

        for key in dic['fin_llamada_interna']:
            if type(dic['fin_llamada_interna'][key]) == float:
                dic['fin_llamada_interna'][key] = round(dic['fin_llamada_interna'][key], 4)
        for key in dic['fin_llamada_externa']:
            if type(dic['fin_llamada_externa'][key]) == float:
                dic['fin_llamada_externa'][key] = round(dic['fin_llamada_externa'][key], 4)
        return dic

    def guardar_iteracion(self):

        if self.j_hora <= self.reloj and self.iteraciones_guardadas < self.i_iteraciones:
            self.iteraciones_guardadas += 1
            self.iteraciones.append(self.as_dict())

        if self.reloj > self.cantidad_iteraciones - 10:
            self.ante_ultima_iteracion = self.ultima_iteracion
            self.ultima_iteracion = self.as_dict()


        # if self.rango_iteracion[0][0] <= self.num_iteracion <= self.rango_iteracion[0][1] or \
        #         self.num_iteracion > self.cantidad_iteraciones - self.rango_iteracion[1]:

            # self.llamadas_guardadas_int.add(self.num_llamada_int_actual)
            # self.llamadas_guardadas_ext.add(self.num_llamada_ext_actual)

        # if self.num_iteracion == self.rango_iteracion[0][1] + 1:
        #     self.iteraciones.append({})


    def to_string(self):
        "Muestra los datos del diccionario de una iteracion"
        pp = pprint.PrettyPrinter()
        return pp.pformat(self.as_dict())

    def get_evento(self):
        if self.evento == 'llegada_llamada_interna' or self.evento == 'fin_llamada_interna':
            return self.evento + f' ({self.num_llamada_int_actual})'
        elif self.evento == 'llegada_llamada_externa' or self.evento == 'fin_llamada_externa':
            return self.evento + f' ({self.num_llamada_ext_actual})'
        else:
            # Caso de la inicializacion
            return self.evento

    # Funciones para devolver los random de cada tipo
    def get_rnd(self, atributo):
        if atributo not in ('tiempo_llegada_int', 'tiempo_llegada_ext', 'duracion_int', 'duracion_ext',
                            'interno_origen', 'linea_externa', 'interno_destino', 'activo'):
            raise ValueError("Nombre de atributo incorrecto")

        # Si el atributo activo es verdadero devuelve el proximo aleatorio de una lista de aleatorios
        if self.listas_rnd['activo']:
            if len(self.listas_rnd[atributo]) > 0:
                return self.listas_rnd[atributo].pop(0)
        # Sino devuelve un nuevo aleatorio
        return random()

    def set_rnd(self, tiempo_llegada_int=[], tiempo_llegada_ext=[], duracion_int=[], duracion_ext=[],
                interno_origen=[], linea_externa=[], interno_destino=[], activo=True):
        """Permite setear todos las listas de numeros aleatorios"""

        self.listas_rnd = {
            'tiempo_llegada_int': tiempo_llegada_int,
            'tiempo_llegada_ext': tiempo_llegada_ext,
            'duracion_int': duracion_int,
            'duracion_ext': duracion_ext,
            'interno_origen': interno_origen,
            'linea_externa': linea_externa,
            'interno_destino': interno_destino,
            'activo': activo
        }

    def set_proxima_llegada_int(self):
        """Calcula la proxima llegada guardando todos los valores"""
        self.rnd_tiempo_llegada_int = self.get_rnd('tiempo_llegada_int')
        self.tiempo_llegada_int = - self.media_int * math.log(1 - self.rnd_tiempo_llegada_int)
        self.proxima_llegada_int = self.reloj + self.tiempo_llegada_int

    def set_proxima_llegada_ext(self):
        """Calcula la proxima llegada guardando todos los valores"""
        self.rnd_tiempo_llegada_ext = self.get_rnd('tiempo_llegada_ext')
        self.tiempo_llegada_ext = - self.media_ext * math.log(1 - self.rnd_tiempo_llegada_ext)
        self.proxima_llegada_ext = self.reloj + self.tiempo_llegada_ext

    def set_fin_llamada_int(self):
        """Calcula el fin de la llamada interna guardando todos los valores"""
        # Calculo del fin de llamada
        self.rnd_duracion_int = self.get_rnd('duracion_int')
        self.duracion_int = self.min_int + self.rnd_duracion_int * (self.max_int - self.min_int)
        self.fin_llamada = self.reloj + self.duracion_int
        # Se guarda el resultado
        self.fin_llamada_interna[self.num_llamada_int_total] = self.fin_llamada

    def set_fin_llamada_ext(self):
        """Calcula el fin de la llamada externa guardando todos los valores"""
        self.rnd_duracion_ext = self.get_rnd('duracion_ext')
        self.duracion_ext = self.min_ext + self.rnd_duracion_ext * (self.max_ext - self.min_ext)
        self.fin_llamada = self.reloj + self.duracion_ext
        self.fin_llamada_externa[self.num_llamada_ext_total] = self.fin_llamada

    def get_rnd_integer(self, rnd, num):
        return math.trunc(rnd * num) + 1

    def set_interno_origen(self):
        """Muestra el interno de origen en base a un numero aleatoreo"""
        self.rnd_interno_origen = self.get_rnd('interno_origen')
        self.interno_origen = self.get_rnd_integer(self.rnd_interno_origen, 10)

    def set_interno_destino(self):
        """Muestra el interno de destino en base a un numero aleatorio"""
        self.rnd_interno_destino = self.get_rnd('interno_destino')
        self.interno_destino = self.get_rnd_integer(self.rnd_interno_destino, 10)

    def set_linea_externa(self):
        """Muestra el interno de destino en base a un numero aleatorio"""
        self.rnd_linea_externa = self.get_rnd('linea_externa')
        # Encontrar los servidores que estan libres y enumerarlos

        # Obtengo los numeros de los servidores libres
        libres = []
        for num in range(len(self.llamada_linea_externa)):
            if self.llamada_linea_externa[num] is False:
                libres.append(num + 1)

        if len(libres) == 2:
            rnd_intergrer = self.get_rnd_integer(self.rnd_linea_externa, 2)
            # Encontrar los numeros de los servidores libres
            if rnd_intergrer == 1:
                self.linea_externa = libres[0]
            else:
                self.linea_externa = libres[1]

        elif len(libres) == 1:
            self.linea_externa = libres[0]
        # Ya sea 3 o 0 devuelve un valor al azar
        else:
            self.linea_externa = self.get_rnd_integer(self.rnd_linea_externa, 3)

    def set_proximo_evento(self):
        """Determina el proximo evento y llegada"""
        # Defino un diccionario con todos los valores que pueden ser minimos y uso como clave los nombres
        # de los eventos
        proximo_evento = {
            'llegada_llamada_interna': self.proxima_llegada_int,
            'llegada_llamada_externa': self.proxima_llegada_ext,
        }
        # Obtengo el menor de los valores y lo agrego al diccionario (si existe alguno)
        if len(self.fin_llamada_interna) > 0:
            self.num_llamada_int_actual = min(self.fin_llamada_interna, key=self.fin_llamada_interna.get)
            proximo_evento['fin_llamada_interna'] = self.fin_llamada_interna[self.num_llamada_int_actual]
        if len(self.fin_llamada_externa) > 0:
            self.num_llamada_ext_actual = min(self.fin_llamada_externa, key=self.fin_llamada_externa.get)
            proximo_evento['fin_llamada_externa'] = self.fin_llamada_externa[self.num_llamada_ext_actual]

        # Calculo del menor valor entre todos los eventos
        self.evento = min(proximo_evento, key=proximo_evento.get)
        self.reloj = proximo_evento[self.evento]

    def inicializacion(self):
        """Evento de inicializacion"""
        # Proxima llegada
        self.set_proxima_llegada_int()
        self.set_proxima_llegada_ext()
        # Calcular estado de los servidores
        self.set_estado_interno()
        self.set_estado_linea_externa()

        self.guardar_iteracion()

        self.rnd_tiempo_llegada_ext = ''
        self.tiempo_llegada_ext = ''
        self.rnd_tiempo_llegada_int = ''
        self.tiempo_llegada_int = ''

    def llegada_llamada_interna(self):
        """Evento de la llegada de una llamada interna"""
        # Setear la llamada actual
        self.num_llamada_int_total += 1
        self.num_llamada_int_actual = self.num_llamada_int_total

        self.tipo_llamada_actual = True

        # Calcular la llegada de la proxima llamada
        self.set_proxima_llegada_int()

        # Fin de la llamada
        self.set_fin_llamada_int()
        # Calcular los internos
        self.set_interno_origen()
        self.set_interno_destino()

        # Si los dos internos estan libres los marco como ocupados
        if self.tipo_llamada_interno[self.interno_origen - 1] is None and \
                self.tipo_llamada_interno[self.interno_destino - 1] is None:
            # Marcar como ocupado por una llamada interna
            self.tipo_llamada_interno[self.interno_origen - 1] = self.tipo_llamada_interno[self.interno_destino - 1] = True
            # Numero de la llamada
            self.num_llamada_a_int[self.interno_origen - 1] = self.num_llamada_a_int[self.interno_destino - 1] = self.num_llamada_int_total

            self.estado_llamada_int[self.num_llamada_int_total] = 'En proceso'
        # En caso de que alguno de los servidores este ocupado se registra la llamada como perdida
        else:
            self.llamadas_int_perdidas += 1
            self.estado_llamada_int[self.num_llamada_int_total] = 'perdida'

            # Se elimina el evento de fin de llamada
            self.fin_llamada_interna[self.num_llamada_int_actual] = 'perdida'


        # Calcular estado de los servidores
        self.set_estado_interno()
        self.guardar_iteracion()

        # Si la llamada fue marcada como perdida se la elimina inmediatamente
        if self.estado_llamada_int[self.num_llamada_int_total] == 'perdida':
            self.estado_llamada_int.pop(self.num_llamada_int_total)
            self.fin_llamada_interna.pop(self.num_llamada_int_actual)

        #
        # Se resetea los valores de la llamada los cuales son temporales
        self.rnd_tiempo_llegada_int = ''
        self.tiempo_llegada_int = ''
        self.rnd_duracion_int = ''
        self.duracion_int = ''
        self.rnd_interno_origen = ''
        self.interno_origen = ''
        self.rnd_interno_destino = ''
        self.interno_destino = ''
        self.fin_llamada = ''


    def llegada_llamada_externa(self):
        """Evento de la llegada de una llamada externa"""
        # Setear la llamada actual
        self.num_llamada_ext_total += 1
        self.num_llamada_ext_actual = self.num_llamada_ext_total

        self.tipo_llamada_actual = False

        # Calcular la llegada de la proxima llamada
        self.set_proxima_llegada_ext()
        # Fin de la llamada
        self.set_fin_llamada_ext()

        # Calcular los internos
        self.set_linea_externa()
        self.set_interno_destino()

        # Si los dos internos estan libres los marco como ocupados
        if self.llamada_linea_externa[self.linea_externa - 1] is False and \
                self.tipo_llamada_interno[self.interno_destino - 1] is None:
            # Marcar como ocupado por una llamada externa
            self.llamada_linea_externa[self.linea_externa - 1] = True
            # False indica que la llamada que ocupa al interno es externa
            self.tipo_llamada_interno[self.interno_destino - 1] = False
            # Numero de la llamada
            self.num_llamada_a_ext[self.linea_externa - 1] = self.num_llamada_a_int[self.interno_destino - 1] \
                = self.num_llamada_ext_total

            self.estado_llamada_ext[self.num_llamada_ext_total] = 'En proceso'
        # En caso de que alguno de los servidores este ocupado se registra la llamada como perdida
        else:
            self.llamadas_ext_perdidas += 1
            self.estado_llamada_ext[self.num_llamada_ext_total] = 'perdida'
            self.fin_llamada_externa[self.num_llamada_ext_actual] = 'perdida'

        # Calcular estado de los servidores
        self.set_estado_interno()
        self.set_estado_linea_externa()
        self.guardar_iteracion()

        # Si la llamada fue marcada como perdida se la elimina inmediatamente
        if self.estado_llamada_ext[self.num_llamada_ext_total] == 'perdida':
            self.estado_llamada_ext.pop(self.num_llamada_ext_total)
            self.fin_llamada_externa.pop(self.num_llamada_ext_actual)

        self.rnd_tiempo_llegada_ext = ''
        self.tiempo_llegada_ext = ''
        self.rnd_duracion_ext = ''
        self.duracion_ext = ''
        self.rnd_linea_externa = ''
        self.linea_externa = ''
        self.rnd_interno_destino = ''
        self.interno_destino = ''
        self.fin_llamada = ''

    def set_fin_llamada_interna(self):
        """Fin de llamada interna marcando todos los atributos como libres"""
        # Servidores
        for id in range(len(self.num_llamada_a_int)):
            # Se busca los servidores ocupados con esa llamada
            if self.num_llamada_a_int[id] == self.num_llamada_int_actual:
                # Se los marca como libres nuevamente
                self.num_llamada_a_int[id] = 0
                self.tipo_llamada_interno[id] = None

        # Fin llamada
        self.fin_llamada_interna[self.num_llamada_int_actual] = 'finalizado'
        # Fin de estado
        self.estado_llamada_int[self.num_llamada_int_actual] = 'finalizado'

        self.guardar_iteracion()
        # Se elimina la llamada finalizada
        self.fin_llamada_interna.pop(self.num_llamada_int_actual)
        self.estado_llamada_int.pop(self.num_llamada_int_actual)

    def set_fin_llamada_externa(self):
        """Fin de llamada externa marcando todos los atributos como libres"""
        # Servidores
        # Interno
        for id in range(len(self.num_llamada_a_int)):
            # Se busca los servidores ocupados con esa llamada
            if self.num_llamada_a_int[id] == self.num_llamada_ext_actual:
                # Se los marca como libres nuevamente
                self.num_llamada_a_int[id] = 0
                self.tipo_llamada_interno[id] = None

        # Lineas externas
        for id in range(len(self.num_llamada_a_ext)):
            # Se busca los servidores ocupados con esa llamada
            if self.num_llamada_a_ext[id] == self.num_llamada_ext_actual:
                # Se los marca como libres nuevamente
                self.num_llamada_a_ext[id] = 0
                self.llamada_linea_externa[id] = False

        # Fin llamada
        self.fin_llamada_externa[self.num_llamada_ext_actual] = 'finalizado'
        # Fin de estado
        self.estado_llamada_ext[self.num_llamada_ext_actual] = 'finalizado'

        self.guardar_iteracion()
        # Se elimina la llamada finalizada
        self.fin_llamada_externa.pop(self.num_llamada_ext_actual)
        self.estado_llamada_ext.pop(self.num_llamada_ext_actual)

    def simular(self, n=None):
        if n is not None:
            self.cantidad_iteraciones = n

        # Inicio de la iteracion
        if self.num_iteracion == 0:
            self.inicializacion()

        # for iteracion in range(self.cantidad_iteraciones):
        while True:
            self.num_iteracion += 1
            # print(f"iteracion {iteracion}")
            self.set_proximo_evento()

            # Condicion de corte
            if self.reloj > self.cantidad_iteraciones:
                self.iteraciones.append(self.ultima_iteracion)
                break

            if self.evento == 'llegada_llamada_interna':
                self.llegada_llamada_interna()
            elif self.evento == 'llegada_llamada_externa':
                self.llegada_llamada_externa()
            elif self.evento == 'fin_llamada_interna':
                self.set_fin_llamada_interna()
            else:
                self.set_fin_llamada_externa()

        # La iteracion que se pasa
        # self.iteraciones.append(self.as_dict())

    def get_llamadas_guardadas_int(self):
        guardadas = set()
        for iteracion in self.iteraciones:
            guardadas.update(list(iteracion['fin_llamada_interna'].keys()))
        return guardadas

    def get_llamadas_guardadas_ext(self):
        guardadas = set()
        for iteracion in self.iteraciones:
            guardadas.update(list(iteracion['fin_llamada_externa'].keys()))
        return guardadas

if __name__ == '__main__':
    d = {1:5, 2:3}
    print(min(d, key=d.get()))

    sim = Simulador()
    print(sim.as_dict())
    print(sim.to_string())
    print(random())