# -*- coding: utf-8 -*-

class Terme:
    def __init__(self, coeff, puiss = 1, var = 'x'):
        if (not (isinstance(puiss, int))) or (not (isinstance(var, str))):
            print "Erreur de définition ! La puissance doit être un nombre relatif !"
        self.puiss = puiss # Nombre entier
        self.coeff = coeff # Coeff devant le terme
        self.var = var # Lettre pour la var

    def __add__(self, other):
        if not (isinstance(other, Terme)):
            return str(self) + " + " + str(other)
        if (self.puiss == other.puiss) and (self.var == other.var):
            return Terme(self.coeff + other.coeff, self.puiss, self.var)
        else:
            return str(self) + " + " + str(other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if not (isinstance(other, Terme)):
            return str(self) + " + " + str(other)
        if (self.puiss == other.puiss) and (self.var == other.var):
            return Terme(self.coeff - other.coeff, self.puiss, self.var)
        else:
            return str(self) + " - " + str(other)

    def __rsub__(self, other):
        return -(self - other)

    def __mul__(self, other):
        if (isinstance(other, float)) or (isinstance(other, int)):
            return Terme(self.coeff * other, self.puiss, self.var)
        elif self.var == other.var:
            return Terme(self.coeff * other.coeff, self.puiss + other.puiss, self.var)
        else:
            return Terme(self.coeff * other.coeff, self.puiss + other.puiss, self.var + other.var)

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        if (isinstance(other, float)) or (isinstance(other, int)):
            return Terme(self.coeff / other, self.puiss, self.var)
        elif self.var == other.var:
            return Terme(self.coeff / other.coeff, self.puiss - other.puiss, self.var)
        else:
            return str(self.coeff / other.coeff) + str(Terme(1, self.puiss, self.var)) + " / " + str(Terme(1, other.puiss, other.var))

    def __rdiv__(self, other):
        return self.inv() * other

    def inv(self):
        return Terme(1.0 / self.coeff, - self.puiss, self.var)

    def __str__(self):
        if self.coeff == 1:
            coeff = ''
        elif self.coeff == -1:
            coeff = '-'
        else:
            coeff = str(self.coeff) + ' '
        if self.puiss == 1:
            terme = self.var
        elif (self.puiss == 0) and ((self.coeff == 1) or (self.coeff == -1)):
            terme = '1'
        elif self.puiss == 0:
            terme = ''
        else:
            terme = self.var + u'^' + str(self.puiss)
        return coeff + terme
                
