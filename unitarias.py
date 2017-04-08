import unittest
import practica2
import sqlite3 as sql


class TestPractica2(unittest.TestCase):

    def test_verficiar_login(self):
        print("########VERIFICAR LOGIN########")
        self.assertEqual(verificar_login('rgerson', '1234', 1),False)

    def test_transferencias(self):
        print("########TRANSFERENCIAS########")
        self.assertEqual(test_transferencias(1, 10, 19), True)

    def test_debito(self):
        print("######## DEBITO ########")
        self.assertEqual(test_debito(1, 5, 19), True)

    def test_credito(self):
        print("######## CREDITO ########")
        self.assertEqual(test_credito(1, 5, 19), True)

    def test_prueba(self):
        print("######## TEST PRUEBA ########")
        self.assertEqual(saldo_cuenta(1), 200)

    def test_tipo_serv(self):
        print("######## TIPO SERVICIO ########")
        self.assertEqual(tipo_serv("luz"), 2)

    def test_veri_cuenta(self):
        print("######## VERFICAR CUENTA ########")
        self.assertEqual(verificar_cuenta(1), False)

    def test_veri_saldo(self):
        print("######## VERIFICAR SALDO ########")
        self.assertEqual(verificar_saldo(1, 100), True)

    def test_registro(self):
        print("##### TEST REGISTRO####")
        g = sql.connect('p2.db')
        query = "Insert into persona(contrasena, nombre, saldo, usuario,correo) values " \
                +"(1234,'jack',100,'jack','jack@gmail.com')"
        g.execute(query)
        g.commit()
        g.close()
        self.assertEqual(verificar_registro(1234, "jack", "jack", "jack@gmail.com"), True)

    def test_codigo(self):
        print("######## CODIGO ########")
        self.assertEqual(retorno_codigo("wmaradiaga", 19), True)


def verificar_login(user, contra, cod):
    g = sql.connect('p2.db')
    query = "SELECT codigo FROM persona WHERE codigo = " + str(cod) + " and contrasena='"+contra+"'"
    exe = g.execute(query)
    log = exe.fetchall()
    if len(log) == 0:
        return False
    return True

def verificar_pago(cuenta_ori,tipo_ser,monto):
    print 'Pago de Servicio'
    log_combo = tipo_ser
    print monto
    print log_combo
    saldo = saldo_cuenta(cuenta_ori)
    print "SALDO CUENTA"
    print saldo
    if int(saldo) > int(monto):
        descrip = "Pago de " + log_combo + " con un saldo sobrante de: " + str(int(saldo) - int(monto))
        modificar_actual_credito(cuenta_ori, monto, saldo, tipo_serv(log_combo), descrip)
        print("Realizara Pago")
        saldo1 = saldo_cuenta(cuenta_serv(log_combo))
        modificar_pago(cuenta_serv(log_combo), monto, saldo1)
        print("Realizo Pago")
        return True
    else:
        print 'No tiene suficiente money'
        return False


def modificar_pago(codigo, monto,saldo):
    g = sql.connect('p2.db')
    query = "UPDATE persona SET saldo = " + str(int(saldo) + int(monto)) + " WHERE codigo = " + str(codigo)
    g.execute(query)
    g.commit()
    g.close()


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

#############################################################3
def test_transferencias(cuenta_ori, monto, cuenta):
            # Verificar si existe la cuenta destino
            flag = verificar_cuenta(cuenta)
            if flag is True:
                return False
            else:
                # Verificar si tengo suficiente dinero para hacer la transferencia
                dif = verificar_saldo(cuenta_ori, monto)
                if dif is True:
                    g = sql.connect('p2.db')
                    query = "UPDATE persona SET saldo = saldo + " + str(monto) + " WHERE codigo = " + str(cuenta) + ";"
                    print query
                    exe = g.execute(query)
                    g.commit()
                    query = "UPDATE persona SET saldo = saldo - " + str(monto) + " WHERE codigo = " + str(cuenta) + ";"
                    print query
                    exe = g.execute(query)
                    g.commit()
                    g.close()
                    return True
                else:
                    return False


def verificar_saldo(cuenta, monto):
    g = sql.connect('p2.db')
    query = "SELECT saldo FROM persona WHERE codigo = " + cuenta
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


def test_debito(cuenta, monto, cuenta_actual):
    print "Debito"
    if verificar_cuenta(cuenta):
        return False
    saldo = saldo_cuenta(cuenta)
    if verificar_monto(saldo, monto) == False:
        return False
    saldo2 = saldo_cuenta(cuenta_actual)
    descrip = "Se Debito a la Cuenta: " + str(cuenta) + " El monto de: " + str(monto)
    modificar_actual_credito(cuenta, monto, saldo, 1, descrip)
    print "Cuenta OTRO"
    descrip = "Se Acredtio a la cuenta: " + str(cuenta_actual) + " El monto de: " + str(monto)
    modificar_actual_debito(cuenta_actual, monto, saldo2, 1, descrip)
    print "Cuenta ESTA"
    return True


def test_credito(cuenta, monto, cuenta_actual):
    if verificar_cuenta(cuenta):
        return False
    saldo = saldo_cuenta(cuenta)
    saldo2 = saldo_cuenta(cuenta_actual)
    if verificar_monto(saldo2, monto) == False:
        return False
    descrip = "Se acredita a la Cuenta: " + str(cuenta) + " EL monto de: " + str(monto)
    modificar_actual_debito(cuenta, monto, saldo, 0, descrip)
    descrip = "Se debita de la cuenta: " + str(cuenta_actual) + " El monto de: " + str(monto)
    modificar_actual_credito(cuenta_actual, monto, saldo2, 0, descrip)
    return True


def verificar_monto(saldo, monto):
    esta = False
    if int(saldo) >= int(monto):
        esta = True
    return esta


def modificar_actual_credito(codigo, monto, saldo, tipo, descripcion):
    g = sql.connect('p2.db')
    query = "UPDATE persona SET saldo = " + str(int(saldo) - int(monto)) + " WHERE codigo = " + str(codigo)
    g.execute(query)
    g.commit()
    query = "INSERT INTO debito_credito('descripcion','tipo','monto','codigo') Values('" \
            + str(descripcion) + "'," + str(tipo) + "," + str(monto) + "," + str(codigo) + ")"
    g.execute(query)
    g.commit()
    g.close()


def modificar_actual_debito(codigo, monto, saldo, tipo, descripcion):
    g = sql.connect('p2.db')
    query = "UPDATE persona SET saldo = " + str(int(saldo) + int(monto)) + " WHERE codigo = " + str(codigo)
    g.execute(query)
    g.commit()
    query = "INSERT INTO debito_credito('descripcion','tipo','monto','codigo') Values('" \
            + str(descripcion) + "'," + str(tipo) + "," + str(monto) + "," + str(codigo) + ")"
    g.execute(query)
    g.commit()
    g.close()


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


if __name__ == "__main__":
    unittest.main()
