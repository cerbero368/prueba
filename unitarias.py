import unittest
import practica2
import sqlite3 as sql


class TestPractica2(unittest.TestCase):

    def test_verficiar_login(self):
        log = [(u'willy', u'1234', 26)]
        self.assertEqual(practica2.verificar_login('willy', '1234', log), True)

    def test_prueba(self):
       self.assertEqual(saldo_cuenta(1), 200)

    def test_tipo_serv(self):
        self.assertEqual(tipo_serv("luz"), 2)

    def test_veri_cuenta(self):
        self.assertEqual(verificar_cuenta(1), False)

    def test_veri_saldo(self):
        self.assertEqual(verificar_saldo(1, 100), True)

    def test_registro(self):
        print("TEST REGISTRO")
        g = sql.connect('p2.db')
        query = "Insert into persona(contrasena, nombre, saldo, usuario,correo) values " \
                +"(1234,'minie',100,'minie','mmouse@gmail.com')"
        g.execute(query)
        g.commit()
        g.close()
        self.assertEqual(verificar_registro(1234, "minie", "minie", "mmouse@gmail.com"), True)

    def test_codigo(self):
        self.assertEqual(retorno_codigo("wmaradiaga", 19), True)

    def test_trans(self):
        self.assertEqual(trans_datos(1, 19, 200.0, 600.0), True)


def trans_datos(cuenta, cuenta_destino, p_saldo, p_saldo_destino):
    g = sql.connect('p2.db')
    query = "SELECT saldo FROM persona WHERE codigo = " + str(cuenta)
    exe = g.execute(query)
    saldo = exe.fetchall()
    query = "SELECT saldo FROM persona WHERE codigo = " + str(cuenta_destino)
    exe = g.execute(query)
    saldo_destino = exe.fetchall()
    g.close()
    if str(p_saldo) == str(saldo[0][0]) and str(p_saldo_destino) == str(saldo_destino[0][0]):
        return True
    else:
        return False


def verificar_saldo(cuenta, monto):
    g = sql.connect('p2.db')
    query = "SELECT saldo FROM persona WHERE codigo = " + str(cuenta)
    exe = g.execute(query)
    log = exe.fetchall()
    g.close()
    print log[0][0]
    print monto
    if int(log[0][0]) > int(monto):
        print 'Tiene saldo'
        return True
    else:
        print 'No tiene saldo'
        return False


def retorno_codigo(usuario, codigo):
    g = sql.connect('p2.db')
    query = "SELECT codigo FROM persona WHERE usuario = '" + str(usuario) + "'"
    exe = g.execute(query)
    log = exe.fetchall()
    g.close()
    if str(codigo) == str(log[0][0]):
        print 'Codigo bien'
        return True
    else:
        print 'Codigo mal'
        return False


def verificar_registro(contra, nombre, usuario, correo):
    g = sql.connect('p2.db')
    query = "SELECT contrasena, nombre, correo FROM persona WHERE usuario = '" + str(usuario) + "'"
    exe = g.execute(query)
    log = exe.fetchall()
    g.close()
    if str(log[0][0]) == str(contra) and str(log[0][1]) == str(nombre) and str(log[0][2]) == str(correo):
        print 'Registro correcto'
        return True
    else:
        print "Registro Incorrecto"
        print log
        return False


def verificar_cuenta(cuenta):
    g = sql.connect('p2.db')
    verificar = "select usuario from persona where codigo='" + str(cuenta) + "'"
    ver = g.execute(verificar)
    log = ver.fetchall()
    g.close()
    print log
    if len(log) == 0:
        print 'No existe'
        return True
    else:
        print 'Existe'
        print log[0][0]
        return False


def saldo_cuenta(cuenta):
    g = sql.connect('p2.db')
    query = "select saldo from persona where codigo='" + str(cuenta)+"'"
    var = g.execute(query)
    log = var.fetchall()
    g.close()
    return log[0][0]


def cuenta_serv(tipo):
    if tipo == 'luz':
        return 22
    if tipo== 'agua':
        return 23
    if tipo == 'telefono':
        return 24
    if tipo == 'gas':
        return 25

def tipo_serv(tipo):
    if tipo == 'luz':
        return 2
    if tipo== 'agua':
        return 3
    if tipo == 'telefono':
        return 4
    if tipo == 'gas':
        return 5
    if tipo == 'credito':
        return 0
    if tipo == 'debito':
        return 1

if __name__ == "__main__":
    unittest.main()