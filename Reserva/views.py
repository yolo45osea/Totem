import base64
from io import BytesIO
from django.shortcuts import redirect, render
from django.db.models import Q
import qrcode
from Reserva.forms import ReservaForm
from Reserva.models import Admin, Chofer, Comuna, TipoAdmin, Totem, Vehiculo, ZonaViaje, MetodoPago, Pasajero, Reserva
import datetime
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

def index(request):

    admin_id = request.session.get('admin_id')  # Recuperar ID del admin desde la sesión
    context = {}
    if admin_id:
        admin = Admin.objects.get(idAdmin=admin_id)
        context['admin'] = admin

    return render(request, 'index.html', context)

def codigoqr(request, chofer, cupos, nombre, zona, horario, nombre1, nombre2, nombre3):
    # Recuperar datos del chofer, vehículo y destino
    choferSeleccionado = Chofer.objects.filter(idChofer=chofer).first()
    vehiculo = Vehiculo.objects.filter(idVehiculo=choferSeleccionado.vehiculo).first()
    destino = ZonaViaje.objects.filter(idZona=zona).first()
    comuna = Comuna.objects.filter(idComuna=choferSeleccionado.destino).first()

    # Generar los datos para el QR
    data = f"Nombre: {nombre}, Horario: {horario}, Destino: {comuna.nombreComuna}"

    # Generar el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convertir el código QR a Base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Renderizar la plantilla con los datos
    return render(request, 'codigoqr.html', {
        'id_chofer': choferSeleccionado,
        'nombre': nombre,
        'nombre1': nombre1,
        'nombre2': nombre2,
        'nombre3': nombre3,
        'cupos': cupos,
        'vehiculo': vehiculo,
        'zona': zona,
        'destino': destino,
        'horario': horario,
        'qr_code': img_base64  # Código QR codificado en Base64
    })

def reserva(request):
    # Inicializar variables
    choferes = []
    zona = None
    horario = None
    cupos = None
    horarioViaje = None

    if request.method == 'GET':
        zona = request.GET.get('zona')
        horario = request.GET.get('horario')
        

        print(cupos)

        if zona and horario:  # Verifica que ambos valores estén presentes
            id_comunas = Comuna.objects.filter(ZonaViaje_id=zona).values_list('idComuna', flat=True)
            choferes = Chofer.objects.filter(
                Q(horario1=horario) | Q(horario2=horario) | Q(horario3=horario),
                destino_id__in=id_comunas
            )
            horarioViaje = horario
        

        print(f"Choferes encontrados: {choferes}")
        print(f"Zona: {zona}, Horario: {horario}")

    if request.method == 'POST':
        cupos = request.POST.get('cupos')
        chofer = request.POST.get('chofer')
        zonaViaje = request.POST.get('zonaViaje')
        horario = request.GET.get('horario')

        if zonaViaje and horario and chofer :
            return redirect('datos', id_chofer=chofer, cupos=cupos, zona=zonaViaje, horario=horario)
    # Renderiza la plantilla con valores inicializados (aunque sean vacíos)
    return render(request, 'reserva.html', {"choferes": choferes, "zona": zona, "horario": horario, "horarioViaje": horarioViaje})

#------------------------------------------------------------------------------------------

def pago(request, chofer, cupos, nombre, email, rut, zona, horario, nombre1, email1, rut1, nombre2, email2, rut2, nombre3, email3, rut3):
    # Aquí tienes los valores pasados desde el formulario
    print(f"Chofer: {chofer}, Cupos: {cupos}, Nombre: {nombre}")
    
    if request.method == 'POST':
        choferSeleccionado = Chofer.objects.filter(idChofer = chofer).first()
        choferSeleccionado.cupos -= cupos
        choferSeleccionado.save()
        pasajeros = Pasajero.objects.all().last()
        nuevo_id = int(pasajeros.idPasajero) + 1 if pasajeros else 1
        validacionPasajero = Pasajero.objects.filter(rut = rut).first()
        validacionAcompanante1 = Pasajero.objects.filter(rut = rut1).first()
        validacionAcompanante2 = Pasajero.objects.filter(rut = rut2).first()
        validacionAcompanante3 = Pasajero.objects.filter(rut = rut3).first()

        #Pasajero
        if cupos == 1:
            if not validacionPasajero:
                idViajante = Pasajero.objects.create(
                    idPasajero= nuevo_id,
                    nombre=nombre,
                    email=email,
                    rut=rut
                )
            else:
                idViajante = validacionPasajero

        #Acompañante1
        elif cupos == 2:
            if not validacionPasajero:
                idViajante = Pasajero.objects.create(
                    idPasajero= nuevo_id,
                    nombre=nombre,
                    email=email,
                    rut=rut
                )
                nuevo_id += 1
            else:
                idViajante = validacionPasajero

            if not validacionAcompanante1:
                idViajante = Pasajero.objects.create(
                    idPasajero= nuevo_id,
                    nombre=nombre1,
                    email=email1,
                    rut=rut1
                )
                nuevo_id += 1
            else:
                idViajante = validacionPasajero

        #Acompañante2
        elif cupos == 3:
            if not validacionPasajero:
                idViajante = Pasajero.objects.create(
                    idPasajero= nuevo_id,
                    nombre=nombre,
                    email=email,
                    rut=rut
                )
                nuevo_id += 1
            else:
                idViajante = validacionPasajero

            if not validacionAcompanante1:
                idViajante = Pasajero.objects.create(
                    idPasajero= nuevo_id,
                    nombre=nombre1,
                    email=email1,
                    rut=rut1
                )
                nuevo_id += 1
            else:
                idViajante = validacionAcompanante1

            if not validacionAcompanante2:
                idViajante = Pasajero.objects.create(
                    idPasajero= nuevo_id,
                    nombre=nombre2,
                    email=email2,
                    rut=rut2
                )
                nuevo_id += 1
            else:
                idViajante = validacionAcompanante2
        
        #Acompañante3
        elif cupos == 4:
            if not validacionPasajero:
                idViajante = Pasajero.objects.create(
                    idPasajero= nuevo_id,
                    nombre=nombre,
                    email=email,
                    rut=rut
                )
                nuevo_id += 1
            else:
                idViajante = validacionPasajero

            if not validacionAcompanante1:
                idViajante = Pasajero.objects.create(
                    idPasajero= nuevo_id,
                    nombre=nombre1,
                    email=email1,
                    rut=rut1
                )
                nuevo_id += 1
            else:
                idViajante = validacionAcompanante1

            if not validacionAcompanante2:
                idViajante = Pasajero.objects.create(
                    idPasajero= nuevo_id,
                    nombre=nombre2,
                    email=email2,
                    rut=rut2
                )
                nuevo_id += 1
            else:
                idViajante = validacionAcompanante2
            if not validacionAcompanante3:
                idViajante = Pasajero.objects.create(
                    idPasajero= nuevo_id,
                    nombre=nombre3,
                    email=email3,
                    rut=rut3
                )
                nuevo_id += 1
            else:
                idViajante = validacionAcompanante3

        reservas = Reserva.objects.all().last()
        nuevo_id_reserva = int(reservas.idReserva) + 1 if reservas else 1
        Reserva.objects.create(
            idReserva = nuevo_id_reserva,
            fecha = datetime.date.today(),
            vehiculo = choferSeleccionado.vehiculo,
            estado = 1,
            estadoTexto = "activa",
            pasajero = idViajante,
            horario = horario,
            chofer = choferSeleccionado,
            calificacion = 0,
            resena = "",
            respuesta = "",

            nombreAcompanante1 = nombre1 or None,
            emailAcompanante1 = email1 or None,
            rutAcompanante1 = rut1 or None,

            nombreAcompanante2 = nombre2 or None,
            emailAcompanante2 = email2 or None,
            rutAcompanante2 = rut2 or None,

            nombreAcompanante3 = nombre3 or None,
            emailAcompanante3 = email3 or None,
            rutAcompanante3 = rut3 or None
        )

        return redirect('codigoqr', chofer=choferSeleccionado.idChofer, cupos=cupos, nombre=nombre, zona=zona, horario=horario, nombre1=nombre1, nombre2=nombre2, nombre3=nombre3)
    
    return render(request, 'pago.html', {
        'chofer': chofer, 
        'cupos': cupos, 
        'nombre': nombre, 
        'nombre1': nombre1, 
        'nombre2': nombre2, 
        'nombre3': nombre3
        })

def a(request):
    choferes = Chofer.objects.all()
    zonas = ZonaViaje.objects.all()
    comunas = Comuna.objects.all()
    vehiculos = Vehiculo.objects.all()
    pasajeros = Pasajero.objects.all()
    pago = MetodoPago.objects.all()
    reservas = Reserva.objects.all()
    return render (request, 'a.html', {
        "choferes": choferes, 
        "zonas": zonas,
        "comunas": comunas,
        "vehiculos": vehiculos,
        "pasajeros": pasajeros,
        "pago": pago,
        "reservas": reservas
    })

def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar la nueva reserva en la base de datos
            return redirect('index')  # Redirigir a la lista de reservas o a cualquier página que desees
    else:
        form = ReservaForm()
    
    return render(request, 'crear_reserva.html', {'form': form})

def datos(request, id_chofer, cupos, zona, horario):
    chofer = Chofer.objects.get(idChofer=id_chofer)
    #cupos = request.GET.get('cupos')  # Obtén el valor de "cupos" desde la URL
    #cupos = int(cupos)
    print(f"cupos: {cupos}")

    if cupos > chofer.cupos:
        error_message = f"los cupos del/la chofer {chofer} son insuficientes {chofer.cupos}"
    else:
        error_message = None
    
    if request.method == 'POST':
        #Pasajero 
        nombre = request.POST.get('name')
        email = request.POST.get('email')
        rut = request.POST.get('rut')

        # Acompañante 1
        nombre1 = request.POST.get('name1')
        email1 = request.POST.get('email1')
        rut1 = request.POST.get('rut1')

        # Acompañante 2
        nombre2 = request.POST.get('name2')
        email2 = request.POST.get('email2')
        rut2 = request.POST.get('rut2')

        # Acompañante 3
        nombre3 = request.POST.get('name3')
        email3 = request.POST.get('email3')
        rut3 = request.POST.get('rut3')
        return redirect('pago', chofer=chofer.idChofer, cupos=cupos, nombre=nombre, email=email, rut=rut, zona=zona, horario=horario, nombre1=nombre1, email1=email1, rut1=rut1, nombre2=nombre2, email2=email2, rut2=rut2, nombre3=nombre3, email3=email3, rut3=rut3)

    return render(request, 'datos.html', {
        'chofer': chofer, 
        'cupos': cupos,
        'zona': zona,
        'horario': horario,
        'error_message': error_message,
    })

def admin(request):
    mensaje = None
    tipo = TipoAdmin.objects.filter(idTipo = 1).first()
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pswd')
        validacion = Admin.objects.filter(email=email).first()
        sistema = TipoAdmin.objects.filter(idTipo = 1).first()
        aeropuerto = TipoAdmin.objects.filter(idTipo = 2).first()
        Transfer = TipoAdmin.objects.filter(idTipo = 3).first()
        if validacion:
            if check_password(password, validacion.password):
                print('bien')
                request.session['admin_id'] = validacion.idAdmin
                if validacion.tipo == sistema:
                    return redirect('adminSistema')
                elif validacion.tipo == aeropuerto:
                    return redirect('adminAeropuerto')
                elif validacion.tipo == Transfer:
                    return redirect('adminTransfer')
                else:
                    return redirect('index')
            elif not check_password(password, validacion.password):
                print('mal')
                username = User.objects.get(email=email)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                        login(request, user)
                        return redirect('index')
            else:
                mensaje = "Contraseña Incorrecta"
        
        else:
            mensaje = "El usuario no es valido"

    return render(request, 'inicio_admin.html', {'mensaje': mensaje})

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def adminSistema(request):
    return render(request, 'adminSistema.html')

def adminAeropuerto(request):
    return render(request, 'adminAeropuerto.html')

def adminTransfer(request):
    return render(request, 'adminTransfer.html')


def gestionUsuarios(request):

    choferes = Chofer.objects.all()  # Obtén todos los choferes
    admins = Admin.objects.all()     

    usuarios = {
        'choferes': choferes,
        'admins': admins,
    }

    if request.method == 'POST':
        nombre = request.POST.get('name')
        email = request.POST.get('email')
        rut = request.POST.get('rut')
        password = make_password(request.POST.get('pass'))
        rol = request.POST.get('rol')
        rolAdmin = request.POST.get('rolAdmin')
        estado = request.POST.get('estado')

        if nombre and email and rut and password and rol and rolAdmin and estado:
            if rol == "Administrador":
                admin = Admin.objects.all().last()
                nuevo_id_admin = int(admin.idAdmin) + 1 if admin else 1
                tipo = TipoAdmin.objects.filter(idTipo = rolAdmin).first()
                if estado == 1:
                    estadoUsuario = True
                else:
                    estadoUsuario = False
                Admin.objects.create(
                    idAdmin = nuevo_id_admin,
                    nombre = nombre,
                    email = email,
                    rut = rut,
                    password = password,
                    tipo = tipo,
                    activo = estado,
                    fechaRegistro = datetime.date.today()
                )
            elif rol == "Chofer":
                chofer = Chofer.objects.all().last()
                nuevo_id_chofer = int(chofer.idChofer) + 1 if chofer else 1
                vehiculo = Vehiculo.objects.filter(idVehiculo = 1).first()
                Chofer.objects.create(
                    idChofer = nuevo_id_chofer,
                    nombreChofer = nombre,
                    email = email,
                    rut = rut,
                    password = password,
                    activo = estado,
                    vehiculo = vehiculo,
                    cupos = 10,
                    fechaRegistro = datetime.date.today()
                )
            else:
                print('mal')



    return render(request, 'gestionUsuarios.html', {'usuarios': usuarios})


def monitoreo(request):
    choferes = Chofer.objects.all()  # Obtén todos los choferes
    admins = Admin.objects.all()     # Obtén todos los administradores

    # Combina los resultados en un solo diccionario
    usuarios = {
        'choferes': choferes,
        'admins': admins,
    }

    if request.method == 'POST':
        nombre = request.POST.get('name')
        email = request.POST.get('email')
        rut = request.POST.get('rut')
        password = make_password(request.POST.get('pass'))
        rol = request.POST.get('rol')
        rolAdmin = request.POST.get('rolAdmin')
        estado = request.POST.get('estado')

        if nombre and email and rut and password and rol and rolAdmin and estado:
            if rol == "Administrador":
                admin = Admin.objects.all().last()
                nuevo_id_admin = int(admin.idAdmin) + 1 if admin else 1
                tipo = TipoAdmin.objects.filter(idTipo = rolAdmin).first()
                if estado == 1:
                    estadoUsuario = True
                else:
                    estadoUsuario = False
                Admin.objects.create(
                    idAdmin = nuevo_id_admin,
                    nombre = nombre,
                    email = email,
                    rut = rut,
                    password = password,
                    tipo = tipo,
                    activo = estado,
                    fechaRegistro = datetime.date.today()
                )
            elif rol == "Chofer":
                chofer = Chofer.objects.all().last()
                nuevo_id_chofer = int(chofer.idChofer) + 1 if chofer else 1
                vehiculo = Vehiculo.objects.filter(idVehiculo = 1).first()
                Chofer.objects.create(
                    idChofer = nuevo_id_chofer,
                    nombreChofer = nombre,
                    email = email,
                    rut = rut,
                    password = password,
                    activo = estado,
                    vehiculo = vehiculo,
                    cupos = 10,
                    fechaRegistro = datetime.date.today()
                )
            else:
                print('mal')

    return render(request, 'monitoreo.html', {'usuarios': usuarios})


def gestionarTotem(request):

    totems = Totem.objects.all()

    if request.method == 'POST':
        id = request.POST.get('name')
        ip = request.POST.get('ip')
        serie = request.POST.get('serie')
        modelo = request.POST.get('modelo')
        ubicacion = request.POST.get('ubicacion')
        fechaInstalacion = request.POST.get('fechaInstalacion')
        estado = 1
        validacion = Totem.objects.filter(idTotem = id)
        if validacion:
            mensaje = f"el totem  con id {id} ya existe"
            #return
        else:
            mensaje = None
            Totem.objects.create(
            idTotem = id,
            ip = ip,
            serie = serie,
            modelo = modelo,
            ubicacion = ubicacion,
            estado = estado,
            fecha = fechaInstalacion
        )

    return render(request, 'gestionarTotem.html',{
        'totems': totems,
        'mensaje': mensaje
    })


def monitorearReservas(request):

    reservas = Reserva.objects.all()

    return render(request, 'monitorearReservas.html', {'reservas': reservas})

def GestionChoferes(request):

    chofer = Chofer.objects.all()

    return render(request, 'GestionChoferes.html', {'chofer': chofer})

def gestionZonas(request):

    zona = ZonaViaje.objects.all()

    return render(request, 'gestionZonas.html', {'zona': zona})
