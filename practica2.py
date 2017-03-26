from flask import*
from functools import wraps
import sqlite3 as sql
#from flask_mail import Mail, Message

DATABASE = 'p2.db'

app = Flask(__name__)
# Se crea una instancia de la clase correo
#mail = Mail(app)
app.config.from_object(__name__)
app.secret_key = 'cualquier_cosa'

# Se configura el servidor
#app.config['MAIL_SERVER']='smtp.gmail.com'
#app.config['MAIL_PORT'] = 465
#app.config['MAIL_USERNAME'] = 'wifran10@gmail.com'
#app.config['MAIL_PASSWORD'] = 'db2008000014'
#app.config['MAIL_USE_TLS'] = False
#app.config['MAIL_USE_SSL'] = True
#mail = Mail(app)


@app.route('/')
def index():
    session['usuario_ses'] = None
    session['cuenta_actual'] = None
    return redirect(url_for('login'))


def connect_db():
    return sql.connect(app.config['DATABASE'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    mal = None
    esta = False
    if request.method == 'POST':
        user = request.form['usu']
        contra = request.form['pass']
        codigo = request.form['cod']
        g.db = connect_db()
        querry = "select usuario,contrasena,codigo from persona where usuario='" + user + "' and contrasena='" + contra + "' and codigo=" + codigo
        cur = g.db.execute(querry)
        log = cur.fetchall()
        g.db.close()
        print log
        esta = verificar_login(user, contra, codigo, log)
        if esta:
            session['usuario_ses'] = user
            session['cuenta_actual'] = codigo
            return redirect(url_for('usuario'))
        else:
            mal = "No Tiene un Usuario"

    return render_template('login.html', mal=mal)


def verificar_login(user, contra, cod, log):
    esta = False
    for r in log:
        if user == r[0] and contra == r[1] and int(cod) is r[2]:
            esta = True
            break
    return esta


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nomb = request.form['nombre']
        usuario = request.form['usuario']
        correo = request.form['correo']
        contra = request.form['contra']
        flag = verificar_usuario(usuario)
        if flag is True:
            g.db = connect_db()
            query = "INSERT INTO persona('contrasena', 'nombre', 'saldo', 'usuario', 'correo') VALUES('" + contra + \
                    "', '" + nomb + "', 0, '" + usuario + "', '" + correo + "')"
            msj = g.db.execute(query)
            g.db.commit()
            g.db.close()
            codigo = obtener_codigo(usuario)
            #msg = Message('Te has registrado exitosamente', sender='wifran10@gmail.com', recipients=[' ' + correo + ''])
            #msg.body = "Hola " + nomb + " te has registrado con exito, acontinuacion te presentamos tus datos:" \
            #                          " \n\nUsuario: " + usuario + "\nPassword: " + contra + "\nCodigo de cuenta: " + \
            #         str(codigo[0][0]) + "\n\nGracias por preferirnos."
            #mail.send(msg)
            return redirect(url_for('login'))
        return redirect(url_for('registro'))
    return render_template('registro.html')


def obtener_codigo(usuario_nuevo):
    g.db = connect_db()
    verificar = "select codigo from persona where usuario='" + usuario_nuevo + "'"
    ver = g.db.execute(verificar)
    log = ver.fetchall()
    g.db.close()
    return log


def verificar_usuario(usuario_nuevo):
    g.db = connect_db()
    verificar = "select usuario from persona where usuario='" + usuario_nuevo  + "'"
    ver = g.db.execute(verificar)
    log = ver.fetchall()
    g.db.close()
    print log
    if len(log) == 0:
        print 'No existe'
        return True
    else:
        print 'Existe'
        return False


@app.route('/logout')
def logout():
    session['usuario_ses'] = None
    session['cuenta_actual'] = None
    mal='Ha cerrado sesion'
    return redirect(url_for('login', mal=mal))


@app.route('/usuario', methods=['GET', 'POST'])
def usuario():
    if session['usuario_ses'] is None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['btn_pago'] == "Pagar":
            print 'Pago de Servicio'
            monto = request.form['monto_pagar']
            log_combo = request.form['logCombo']
            print monto
            print log_combo
            saldo = saldo_cuenta(session['cuenta_actual'])
            print "SALDO CUENTA"
            print saldo
            if int(saldo) > int(monto):
                descrip = "Pago de "+log_combo+" con un saldo sobrante de: " + str(int(saldo)-int(monto))
                modificar_actual_credito(session['cuenta_actual'], monto,saldo, tipo_serv(log_combo), descrip)
            else:
                print 'No tiene suficiente money'
                flash("No tiene suficiente dinero", 'error')
        # Seccion para hacer la transferencia a otra cuenta
        if request.form['btn_pago'] == "Transferir":
            print "Transferir"
            cuenta = request.form['t_cuenta']
            monto = request.form['t_monto']
            # Verificar si existe la cuenta destino
            flag = verificar_cuenta(cuenta)
            if flag is True:
                flash("La cuenta no existe", 'error')
            else:
                # Verificar si tengo suficiente dinero para hacer la transferencia
                dif = verificar_saldo(session['cuenta_actual'], monto)
                if dif is True:
                    g.db = connect_db()
                    query = "UPDATE persona SET saldo = saldo + " + monto + " WHERE codigo = " + cuenta + ";"
                    print query
                    exe = g.db.execute(query)
                    g.db.commit()
                    query = "UPDATE persona SET saldo = saldo - " + monto + " WHERE codigo = " + session['cuenta_actual'] + ";"
                    print query
                    exe = g.db.execute(query)
                    g.db.commit()
                    g.db.close()
                    flash("Se ha hecho la transferencia con exito")
                else:
                    flash("No tiene suficiente saldo")
        # Seccion para consultar saldo
        if request.form['btn_pago'] == "Consultar":
            saldo = saldo_cuenta(session['cuenta_actual'])
            flash("Su saldo es: Q" + str(saldo))
        if request.form['btn_pago'] == "Realizar":
            print 'Pago de Servicio'
            cuenta = request.form['num_cuenta']
            monto = request.form['monto_cuenta']
            Ecombo = request.form['E_combo']
            # ***************************************DEBITO****************************************************
            if Ecombo == "Debito":
                print "Debito"
                if verificar_cuenta(cuenta):
                    flash("Cuenta a Debitar no Existe", "Error")
                    return render_template('acciones.html')
                saldo = saldo_cuenta(cuenta)
                if verificar_monto(saldo, monto) == False:
                    flash("Cuenta a Debitar no tiene suficiente saldo")
                    return render_template('acciones.html')
                saldo2 = saldo_cuenta(session['cuenta_actual'])
                descrip = "Se Debito a la Cuenta: " + str(cuenta) + " El monto de: " + str(monto)
                modificar_actual_credito(cuenta, monto, saldo, tipo_serv("Debito"), descrip)
                print "Cuenta OTRO"
                descrip = "Se Acredtio a la cuenta: " + str(session['cuenta_actual']) + " El monto de: " + str(monto)
                modificar_actual_debito(session['cuenta_actual'], monto, saldo2, tipo_serv("Debito"), descrip)
                print "Cuenta ESTA"
                flash("Debito realizado con exito")
                # ****************************************ACREDITAR****************************************************
            if Ecombo == "Credito":
                print "CREDITO"
                if verificar_cuenta(cuenta):
                    flash("Cuenta a Acreditar no Existe", "Error")
                    return render_template('acciones.html')
                saldo = saldo_cuenta(cuenta)
                saldo2 = saldo_cuenta(session['cuenta_actual'])
                if verificar_monto(saldo2, monto) == False:
                    flash("SU cuenta no tiene suficiente Saldo para Acreditar")
                    return render_template('acciones.html')
                descrip = "Se acredita a la Cuenta: " + str(cuenta) + " EL monto de: " + str(monto)
                modificar_actual_debito(cuenta, monto, saldo, tipo_serv("Credito"), descrip)
                descrip = "Se debita de la cuenta: " + str(session['cuenta_actual']) + " El monto de: " + str(monto)
                modificar_actual_credito(session['cuenta_actual'], monto, saldo2, tipo_serv("Credito"), descrip)
                flash("Credito realizado con exito")
    return render_template('acciones.html')


def verificar_monto(saldo,monto):
    esta = False
    if int(saldo) >= int(monto):
        esta = True
    return esta

def modificar_actual_credito(codigo,monto,saldo, tipo,descripcion):
    g.db = connect_db()
    query = "UPDATE persona SET saldo = " + str(int(saldo) - int(monto)) + " WHERE codigo = " + str(codigo)
    g.db.execute(query)
    g.db.commit()
    query = "INSERT INTO debito_credito('descripcion','tipo','monto','codigo') Values('" \
            + descripcion + "'," + str(tipo) + "," + str(monto) + "," + codigo + ")"
    g.db.execute(query)
    g.db.commit()
    g.db.close()


def modificar_actual_debito(codigo, monto, saldo,tipo,descripcion):
    g.db = connect_db()
    query = "UPDATE persona SET saldo = " + str(int(saldo) + int(monto)) + " WHERE codigo = " + str(codigo)
    g.db.execute(query)
    g.db.commit()
    query = "INSERT INTO debito_credito('descripcion','tipo','monto','codigo') Values('" \
            + descripcion + "'," + str(tipo) + "," + str(monto) + "," + codigo + ")"
    g.db.execute(query)
    g.db.commit()
    g.db.close()



def modificar_monto(codigo, monto, saldo, tipo, descripcion):
    g.db = connect_db()
    query = "UPDATE persona SET saldo = " + str(int(saldo)-int(monto)) + " WHERE codigo = " + str(codigo)
    g.db.execute(query)
    g.db.commit()
    print "hizo update"
    query = "INSERT INTO debito_credito('descripcion','tipo','monto','codigo') Values('"\
            +descripcion+"',"+str(tipo)+","+str(monto)+","+codigo+")"
    g.db.execute(query)
    print "hizo insert: "+ str(tipo)
    g.db.commit()
    g.db.close()


def verificar_saldo(cuenta, monto):
    g.db = connect_db()
    query = "SELECT saldo FROM persona WHERE codigo = " + cuenta
    exe = g.db.execute(query)
    log = exe.fetchall()
    g.db.close()
    print log[0][0]
    print monto
    if int(log[0][0]) > int(monto):
        print 'Tiene saldo'
        return True
    else:
        print 'No tiene saldo'
        return False


def verificar_cuenta(cuenta):
    g.db = connect_db()
    verificar = "select usuario from persona where codigo='" + cuenta + "'"
    ver = g.db.execute(verificar)
    log = ver.fetchall()
    g.db.close()
    print log
    if len(log) == 0:
        print 'No existe'
        return True
    else:
        print 'Existe'
        print log[0][0]
        return False

def tipo_serv(tipo):
    if tipo == 'luz':
        return 2
    if tipo== 'agua':
        return 3
    if tipo == 'telefono':
        return 4
    if tipo == 'gas':
        return 5
    if tipo == 'Credito':
        return 0
    if tipo == 'Debito':
        return 1


#def modificar_monto(codigo, monto, tipo, descripcion):
#    i = sql.connect("p2.db")
#    g.db = connect_db()
#    query = "UPDATE persona SET saldo=" + str(monto) + " WHERE codigo=" + str(codigo)
#    g.db.execute(query)
#    g.db.commit()
#    query = "INSERT INTO debito_credito('descripcion','tipo','monto','codigo') Values('"\
#            + str(descripcion) + "'," +str(tipo)+ "," + str(monto) + "," + codigo + ")"
#    print query
#    g.db.execute(query)
#    g.db.commit()
#    g.db.close()


def saldo_cuenta(cuenta):
    g.db = sql.connect('p2.db')
    query = "select saldo from persona where codigo='"+cuenta+"'"
    var = g.db.execute(query)
    log = var.fetchall()
    g.db.close()
    return log[0][0]


if __name__ == "__main__":
    app.run(debug=True)
