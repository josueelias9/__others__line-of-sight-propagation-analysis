class Punto:
    """
    Entidad que representa un punto geográfico (antena/torre).

    Pertenece a la capa de Dominio. No depende de ninguna capa exterior.
    """

    def __init__(
        self,
        nombre: str,
        ubigeo: int,
        longitud: float,
        latitud: float,
        altura_antena: float,
        tipo: str,
        metros_sobre_nivel_mar: float,
    ) -> None:
        self.nombre = nombre
        self.ubigeo = ubigeo
        self.longitud = longitud
        self.latitud = latitud
        self.altura_antena = altura_antena
        self.tipo = tipo
        self.metros_sobre_nivel_mar = metros_sobre_nivel_mar
        self.green_asociado: str = ""

    def __str__(self) -> str:
        return (
            f"Punto: nombre={self.nombre}, longitud={self.longitud}, "
            f"latitud={self.latitud}, altura_antena={self.altura_antena}, "
            f"msnm={self.metros_sobre_nivel_mar}"
        )
