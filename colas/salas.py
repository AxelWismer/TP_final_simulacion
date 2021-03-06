# Salas (servidores)
from generador_pseudoaliatorio.generador import Generador

class Sala:

    def __init__(self, nombre, capacidad, decimales=4):
        self.nombre = nombre
        self.capacidad_inicial = capacidad
        self.generador = Generador(decimals=decimales, random=True)
        self.en_sala = []
        self.en_cola = []
        #Estadisticas extra
        #El lote ya tiene la propiedad de numero, pero esto es para contar lotes por sala
        self.contador_lotes = 0
        self.contador_cola = 0
        self.contador_cola_a_sala= 0
        self.contador_sala = 0
        self.tiempo_recorrido_medio = 0
        self.tiempo_espera_medio = 0
        self.contador_visitantes = 0

    def __str__(self):
        return str(self.as_dict)

    @property
    def tiempo_recorrido(self):
        pass

    def as_dict(self):
        return {
            'nombre': self.nombre,
            "cola": self.cola,
            "capacidad": self.capacidad,
            "cantidad_visitantes": self.contador_visitantes,
            "lotes_en_sala": self.contador_lotes,
            "lotes_en_cola": self.contador_cola,
            "tiempo_espera": round(self.tiempo_espera_medio, 2),
            "cola_a_sala": self.contador_cola_a_sala,

        }

    @property
    def capacidad(self):
        capacidad_ocupada = sum(lote.visitantes for lote in self.en_sala)
        return self.capacidad_inicial - capacidad_ocupada

    @property
    def cola(self):
        return sum(lote.visitantes for lote in self.en_cola)

    def hay_espacio(self, visitantes):
        """Verifica si un nuevo lote puede ingresar a la sala"""
        return visitantes <= self.capacidad

    #def hay_cola(self):
    #    "Verifica si hay cola para ingresar a la sala"
    #    if len(en_cola) > 0:
    #        return True
    #    else:
    #        return False

    def puede_entrar_a_sala_desde_cola(self):
        "Verifica si hay cola para ingresar a la sala, y en caso verdadero verifica si el primero de la cola puede ingresar"
        if len(self.en_cola) > 0:
            return self.hay_espacio(self.en_cola[0].visitantes)
        else:
            return False

    def add_lote(self, lote, reloj):
        "Agrega un nuevo lote, ya sea a la sala o a la cola"
        lote.sala_actual = self
        self.contador_lotes += 1
        if self.hay_espacio(lote.visitantes) and self.cola==0:
            lote.cola = False
            self.en_sala.append(lote)
            # Como el lote entra a la sala se calcula su fin de recorrido utilizando el tiempo actual
            lote.set_fin_recorrido(reloj)
            self.contador_sala += 1
            self.tiempo_recorrido_medio += (lote.fin_recorrido - reloj)
            self.contador_visitantes += lote.visitantes
            #if lote.tiempo_espera_cola != 0:
            #    #Hago la diferencia del momento en el que entro en la cola y el momento que lo agrregamos a la sala
            #    lote.tiempo_espera_cola = reloj - lote.tiempo_espera_cola
            #    self.tiempo_espera_medio += lote.tiempo_espera_cola
        else:
            #Solo la primera vez que entre a la cola
            if not lote.cola:
                self.contador_cola += 1
                lote.tiempo_espera_cola = reloj
            lote.cola = True
            self.en_cola.append(lote)


    def entrar_a_sala(self):
        """Mueve un lote de la cola a la sala"""
        if self.puede_entrar_a_sala():
            lote = self.en_cola.pop(0)
            self.add_lote(lote)

    def salir_de_sala(self, lote):
        """Saca un lote de la sala"""
        self.en_sala.remove(lote)

    def limpiar_sala(self):
        """Limpia las salas para una nueva simulacion"""
        self.en_sala = []
        self.en_cola = []
        self.contador_visitantes, self.tiempo_recorrido_medio, self.tiempo_espera_medio, self.contador_lotes, self.cantidad_visitantes, self.contador_cola_a_sala, self.contador_lotes_sala = 0, 0, 0, 0, 0, 0, 0


class SalaNormal(Sala):
    def __init__(self, nombre, capacidad, media, desviacion, decimales=4):
        super(SalaNormal, self).__init__(nombre, capacidad, decimales)
        self.media = media
        self.desviacion = desviacion

    @property
    def tiempo_recorrido(self):
        return self.generador.box_muller_next(media=self.media, desviacion=self.desviacion)


class SalaUniforme(Sala):
    def __init__(self, nombre, capacidad, minimo, maximo, decimales=4):
        super(SalaUniforme, self).__init__(nombre, capacidad, decimales)
        self.minimo = minimo
        self.maximo = maximo

    @property
    def tiempo_recorrido(self):
        return self.generador.uniforme_next(a=self.minimo, b=self.maximo)

