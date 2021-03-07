from Internet import Internet
from TecnicoRed import TecnicoRed
from Interface import InterfaceEntrada
from Interface import InterfaceSalida
import Factor
class Integral:
    def __init__(self):
        self.internet = Internet()
        self.interfaceEntrada = InterfaceEntrada()
        self.interfaceSalida = InterfaceSalida()
        self.tecnicoRed = TecnicoRed()

    def ponerAltura(self):
        r = self.interfaceEntrada.ordenameInput2(Factor.entradaTexto1)
        self.tecnicoRed.ponleAlturas(r)
        self.interfaceSalida.generarTxtDePuntos(r, Factor.entradaTexto1)

if __name__=="__main__":
    inte = Integral()
    inte.ponerAltura()

