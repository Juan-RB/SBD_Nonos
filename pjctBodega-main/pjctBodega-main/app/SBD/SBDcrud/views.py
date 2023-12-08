from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import *
import logging
from django.contrib import messages
from SBDcrud.models import (
    Usuario,
    Trabajadores,
    Administrador,
    Bodega,
    Bodeguero,
    Clasificadores,
    Recolectores,
    Artesano,
    ColorPrincipal,
    ColorSecundario,
    TipoTela,
    Patron,
    Tela,
    Ubicacion
)

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from .models import Comuna
from django.db import IntegrityError
from django.http import HttpResponseServerError, HttpResponse
from django.http.response import JsonResponse
from django.db.models import Q
from django.utils import timezone

# Create your views here.


# vistas univesrales


def acceso_no_autorizado(request):
    return render(request, "templateSBD/noaccesso.html")


def inicio(request):
    form = UsuarioLogin()
    return render(request, "templateSBD/index.html", {"form": form})

def sinCredencial(request):
    return render(request, "templateSBD/sin_credencial.html")

def handler404(request, exception):
    return render(request, 'templateSBD/404.html', status=404)


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect(
        "iniciar_sesion"
    )  # indico a donde se redirigira luego de apretar el boton


def iniciar_sesion(request):
    logger = logging.getLogger(__name__)
    if request.method == "POST":
        form = UsuarioLogin(request.POST)
        if form.is_valid():
            codUser = form.cleaned_data[
                "codUser"
            ]  # Usar 'codUser' en lugar de 'username'
            password = form.cleaned_data["passW"]
            # Corregido, debe ser 'codTra'
            logger.debug(
                f"Intento de inicio de sesión con usuario: {codUser} y contraseña: {password}"
            )

            user = authenticate(
                request, codUser=codUser, password=password
            )  # Usar 'codUser' en lugar de 'username'

            if user is not None:
                logger.debug(
                    f"Inicio de sesión correcto con usuario: {codUser} y contraseña: {password}"
                )
                login(request, user)  # Inicia sesión al
                trabajador = Trabajadores.objects.get(codTra=user.codTra.codTra)

                if request.user.codPer.codPer == 1:
                    funcion = Administrador.objects.get(
                        codTra=user.codTra.codTra
                    )  #  usuario super administrador
                    bodega = Bodega.objects.get(codBod=funcion.codBod)
                    return render(
                        request,
                        "templateSBD/s_admin.html",
                        {
                            "trabajador": trabajador,
                            "funcion": funcion,
                            "actividad": "S.administrador",
                            "bodega": bodega,
                        },
                    )

                elif request.user.codPer.codPer == 2:  # usuario administrador de bodega
                    funcion = Administrador.objects.get(codTra=user.codTra.codTra)
                    bodega = Bodega.objects.get(codBod=funcion.codBod)
                    return render(
                        request,
                        "templateSBD/a_bodega.html",
                        {
                            "trabajador": trabajador,
                            "funcion": funcion,
                            "actividad": "Administrador Bodega",
                            "bodega": bodega,
                        },
                    )

                elif request.user.codPer.codPer == 3:  # usuario bodeguero
                    funcion = Bodeguero.objects.get(codTra=user.codTra.codTra)
                    bodega = Bodega.objects.get(codBod=funcion.codBod.codBod)
                    return render(
                        request,
                        "templateSBD/bodeguero.html",
                        {
                            "trabajador": trabajador,
                            "funcion": funcion,
                            "actividad": "Bodeguero",
                            "bodega": bodega,
                        },
                    )

                elif request.user.codPer.codPer == 4:  # usuario artesano
                    funcion = Artesano.objects.get(codTra=user.codTra.codTra)
                    bodega = Bodega.objects.get(codBod=funcion.codBod.codBod)

                    return render(
                        request,
                        "templateSBD/artesano.html",
                        {
                            "trabajador": trabajador,
                            "funcion": funcion,
                            "actividad": "Artesano",
                            "bodega": bodega,
                        },
                    )

                elif request.user.codPer.codPer == 5:  # usuario clasificador
                    funcion = Clasificadores.objects.get(codTra=user.codTra.codTra)
                    bodega = Bodega.objects.get(codBod=funcion.codBod.codBod)

                    return render(
                        request,
                        "templateSBD/clasificador.html",
                        {
                            "trabajador": trabajador,
                            "funcion": funcion,
                            "actividad": "Clasificador",
                            "bodega": bodega,
                        },
                    )

                elif request.user.codPer.codPer == 6:  # usuario recolector
                    funcion = Recolectores.objects.get(codTra=user.codTra.codTra)
                    bodega = Bodega.objects.get(codBod=funcion.codBod.codBod)

                    return render(
                        request,
                        "templateSBD/recolector.html",
                        {
                            "trabajador": trabajador,
                            "funcion": funcion,
                            "actividad": "Recolector",
                            "bodega": bodega,
                        },
                    )
                
                else:
                    return render(request, "templateSBD/index.html", {"form": form})

            else:
                logger.debug(
                    f"Intento de inicio de sesión con usuario: {codUser} y contraseña: {password}"
                )
                form.add_error(
                    "codUser", "Credenciales incorrectas"
                )  # Usar 'codUser' en lugar de 'username'

    else:
        form = UsuarioLogin()

    return render(request, "templateSBD/index.html", {"form": form})


# vistas que requieren login


def recolector(request):
    usuario = request.user
    
    if usuario.is_authenticated:  # Verificar si el usuario está autenticado
        # Verificar si el usuario tiene el permiso adecuado
        if usuario.codPer.codPer != 6:
            return redirect("acceso_no_autorizado")

        # Obtener información del usuario autenticado
        trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
        funcion = Recolectores.objects.get(codTra=usuario.codTra.codTra)
        bodega = Bodega.objects.get(codBod=funcion.codBod.codBod)

        return render(
            request,
            "templateSBD/recolector.html",
            {
                "trabajador": trabajador,
                "funcion": funcion,
                "actividad": "Recolector",
                "bodega": bodega,
            },
        )
    else:
        # El usuario no está autenticado, realizar acción específica
        return render(request, "templateSBD/sin_credenciales.html")




def ingreso_fardoBD(request):
    usuario = request.user


    if usuario.codPer.codPer != 6:
        return redirect('acceso_no_autorizado')
    
    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion= Recolectores.objects.get(codTra=usuario.codTra.codTra)
    bodega= Bodega.objects.get(codBod=funcion.codBod.codBod)
    form3= Formfardo()
    form3 = Formfardo(initial={'codRec': funcion.codRec})

    return render(request,'templateSBD/r_ingresofardo.html', {'trabajador': trabajador , 'funcion':funcion, 'actividad': "Recolector", 'bodega':bodega,'form':form3})




def guardar_fardo(request):
    usuario = request.user

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion= Recolectores.objects.get(codTra=usuario.codTra.codTra)
    bodega= Bodega.objects.get(codBod=funcion.codBod.codBod)
    form3= Formfardo()
    fardos =None
    
    print("recibiendo formulario")
    if request.method == 'POST':
        if 'crearFardo' in request.POST:
            form3= Formfardo(request.POST)
            print("Formulario recibido2")

            codRec_nombre=request.POST['codRec']
            print(codRec_nombre)
            codTf_nombre = request.POST['codTf']
            print(codTf_nombre)
            exiStF = request.POST.get('exiSt', False)
            print(exiStF)

            print("vamos a crear el objeto")

            codigo_recolector =Recolectores.objects.get(codRec=codRec_nombre)
            codigo_tipoFardo = TipoFardo.objects.get(codTf=codTf_nombre)


            fardo = Fardos(
                codRec=codigo_recolector,
                codTf=codigo_tipoFardo,  
                exiStF=True
                )

            print("CodFar:",fardo.codFar)
            print("codRec:", fardo.codRec)
            print("codTf:", fardo.codTf)
            print("existe?:", fardo.exiStF)


            print("Previo al validar datos")
            print(form3.errors)

            if form3.is_valid():
                print(form3.errors)
                print("Formulario válido")
                fardo.save()

                fardo_guardado = Fardos.objects.get(pk=fardo.pk)

                print("Formulario guardado")

                return render(request, 'templateSBD/r_ingresofardo.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Recolector','bodega': bodega,
                'form': form3,'fardo_guardado':fardo_guardado # Pasa el objeto tela guardado al contexto
                })
            
            else:
                print("datos invalidos")
                print(form3.errors)

    return render(request, 'templateSBD/r_ingresofardo.html', {
        'trabajador': trabajador,
        'funcion': funcion,
        'actividad': 'Recolector',
        'bodega': bodega,
        'form':form3,
        'fardos':fardos,
    })


def Ringreso_busqueda(request):
    usuario = request.user
    if usuario.codPer.codPer != 6:
        return redirect('acceso_no_autorizado')
    
    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Recolectores.objects.get(codTra=usuario.codTra.codTra)
    bodega = Bodega.objects.get(codBod=funcion.codBod.codBod)
    form=formBusquedaTipoFardo()

    return render(request, 'templateSBD/r_busqueda.html', {'trabajador': trabajador, 'funcion': funcion, 'actividad': 'Recolector', 'bodega': bodega, 'form': form})


def Rbusqueda_muestra(request):
    usuario = request.user
    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Recolectores.objects.get(codTra=usuario.codTra.codTra)
    bodega = Bodega.objects.get(codBod=funcion.codBod.codBod)
    form=formBusquedaTipoFardo()

    fardos = None
    print("previo a recibir el formulario")

    if 'busqueda_far' in request.POST:  
            
        print("recibi el formulario")

        form=formBusquedaTipoFardo(request.POST)
        codTf_nombre = request.POST['codTf']
        print(codTf_nombre)

        print("Formulario recibido 2")

        
        if form.is_valid():
            print("formulario 2 validado")
            fardos = Fardos.objects.filter(codTf=codTf_nombre)

            print(fardos)
                
                
            return render(request, 'templateSBD/r_busqueda.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Recolector','bodega': bodega,
            'form': form,'fardos': fardos })# Pasa el objeto tela guardado al contexto                 
            
        else:
            print(form.errors)
            fardos = None
            


            
    elif 'procesado' in request.POST:
            print("recibi el formulario")
            form=formBusquedaTipoFardo(request.POST)
            exiStF_nombre = request.POST.get('exiStF', False)
            print(exiStF_nombre)
            print("formulario recibido")

       
            print("formulario 2 validado")
            fardos = Fardos.objects.filter(exiStF=exiStF_nombre)
            print(fardos)

            return render(request, 'templateSBD/r_busqueda.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Recolector','bodega': bodega,
                    'form': form,'fardos': fardos# Pasa el objeto tela guardado al contexto
                    })
            
    

    

    return render(request, 'templateSBD/r_busqueda.html', {
        'trabajador': trabajador,
        'funcion': funcion,
        'actividad': 'Recolector',
        'bodega': bodega,
        'form': form,
        'fardos':fardos,
    })

# vistas de clasificador


@login_required
def clasificador(request):
    usuario = request.user
    if usuario.codPer.codPer != 5:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Clasificadores.objects.get(codTra=usuario.codTra.codTra)
    bodega = Bodega.objects.get(codBod=funcion.codBod.codBod)

    return render(
        request,
        "templateSBD/clasificador.html",
        {
            "trabajador": trabajador,
            "funcion": funcion,
            "actividad": "Clasificador",
            "bodega": bodega,
        },
    )


@login_required
def ingreso_muestrasBD(request):

    usuario = request.user
    if usuario.codPer.codPer != 5:
        return redirect('acceso_no_autorizado')
    
    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Clasificadores.objects.get(codTra=usuario.codTra.codTra)
    bodega = Bodega.objects.get(codBod=funcion.codBod.codBod)
    form1 = FormMuestra(initial={'codCla': funcion.codCla}, data=request.POST if request.method == 'POST' else None)


    telas = None

    if 'crearMuestra' in request.POST:
            form1=FormMuestra(request.POST)
            print("Formulario recibido1")


            codCla_nombre=request.POST['codCla']
            print(codCla_nombre)
            codCp_nombre = request.POST['codCp']
            print(codCp_nombre)
            codCs_nombre = request.POST['codCs']
            print(codCs_nombre)
            codTt_nombre = request.POST['codTt']
            print(codTt_nombre)
            codPt_nombre = request.POST['codPt']
            print(codPt_nombre)
            exiSt = request.POST.get('exiSt', False)
            print(exiSt)

            print("vamos a crear el objeto")

            codigo_clasificador =Clasificadores.objects.get(codCla=codCla_nombre)
            color_principal = ColorPrincipal.objects.get(codCp=codCp_nombre)
            color_secundario = ColorSecundario.objects.get(codCs=codCs_nombre)
            tipo_tela = TipoTela.objects.get(codTt=codTt_nombre)
            patron = Patron.objects.get(codPt=codPt_nombre)

            tela = Tela(
                codCla=codigo_clasificador,
                codCp=color_principal, 
                codCs=color_secundario,  
                codTt=tipo_tela,
                codPt=patron, 
                exiSt=True
                )

            print("codCla:", tela.codCla)
            print("codCp:", tela.codCp)
            print("codCs:", tela.codCs)
            print("codTt:", tela.codTt)
            print("codPt:", tela.codPt)
            print("exiSt:", tela.exiSt)

            print("Previo al validar datos")
            print(form1.errors)

            if form1.is_valid():
                print(form1.errors)
                print("Formulario válido")
                tela.save()

                tela_guardada = Tela.objects.get(pk=tela.pk)

                print("Formulario guardado")

                return render(request, 'templateSBD/c_ingresomuestrasbd.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Clasificador','bodega': bodega,
                'form1': form1,'tela_guardada': tela_guardada # Pasa el objeto tela guardado al contexto
                })

            else:
                print("datos invalidos")
                print(form1.errors)



    return render(request, 'templateSBD/c_ingresomuestrasbd.html', {'trabajador': trabajador, 'funcion': funcion, 'actividad': 'Clasificador', 'bodega': bodega, 'form1': form1})


def Cingreso_busqueda(request):
    usuario = request.user
    telas = None

    if usuario.codPer.codPer != 5:
        return redirect('acceso_no_autorizado')
    
    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Clasificadores.objects.get(codTra=usuario.codTra.codTra)
    bodega = Bodega.objects.get(codBod=funcion.codBod.codBod)
    
    form_principal = FormbusquedaCp(request.POST if request.method == 'POST' else None)
    form_secundario = FormbusquedaCs(request.POST if request.method == 'POST' else None)
    form_patron = FormbusquedaPt(request.POST if request.method == 'POST' else None)
    form_tipo_tela = FormbusquedaTt(request.POST if request.method == 'POST' else None)
    form_cod_tela = FormbusquedaTela(request.POST if request.method == 'POST' else None)

    if request.method == 'POST':
        if form_principal.is_valid():
            # Procesar búsqueda por color principal
            telas = Tela.objects.filter(codCp=form_principal.cleaned_data['codCp'],exiSt=True)
        elif form_secundario.is_valid():
            # Procesar búsqueda por color secundario
            telas = Tela.objects.filter(codCs=form_secundario.cleaned_data['codCs'],exiSt=True)
        elif form_patron.is_valid():
        # Procesar búsqueda por patrón
            telas = Tela.objects.filter(codPt=form_patron.cleaned_data['codPt'],exiSt=True)
        elif form_tipo_tela.is_valid():
        # Procesar búsqueda por tipo de tela
            telas = Tela.objects.filter(codTt=form_tipo_tela.cleaned_data['codTt'],exiSt=True)
        elif form_cod_tela.is_valid():
            # Procesar búsqueda por código de tela
            cod_tela = form_cod_tela.cleaned_data['codTela'].codTela
            telas = Tela.objects.filter(codTela=cod_tela,exiSt=True)
        
                

    return render(request, 'templateSBD/c_busqueda.html', {
        'form_principal': form_principal,
        'form_secundario': form_secundario,
        'form_patron': form_patron,
        'form_tipo_tela': form_tipo_tela,
        'form_cod_tela': form_cod_tela,

        'telas': telas,
        'trabajador': trabajador,
        'funcion': funcion,
        'actividad': 'Clasificador',
        'bodega': bodega,
        # Pasa el objeto tela guardado al contexto
    })



@login_required
def Cbusqueda_muestras(request):
    usuario = request.user
    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Clasificadores.objects.get(codTra=usuario.codTra.codTra)
    bodega = Bodega.objects.get(codBod=funcion.codBod.codBod)
    form2 = FormbusquedaCp()

    telas = None

    if 'busqueda_cp' in request.POST:   
            form2=FormbusquedaCp(request.POST)

            codCp_nombre = request.POST['codCp']
            print(codCp_nombre)
            color_principal = ColorPrincipal.objects.get(codCp=codCp_nombre)

            print("Formulario recibido 2")
        
            if form2.is_valid():
                print("formulario 2 validado")
                telas = Tela.objects.filter(codCp=color_principal)
                return render(request, 'templateSBD/c_busqueda.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Clasificador','bodega': bodega,
                'form2': form2,'telas': telas# Pasa el objeto tela guardado al contexto
                })
            
            else:
                telas = None

    return render(request, 'templateSBD/c_ingresomuestrasbd.html', {
        'trabajador': trabajador,
        'funcion': funcion,
        'actividad': 'Clasificador',
        'bodega': bodega,
        'form2': form2,
        'telas': telas,
    })


def artesano(request):
    usuario = request.user

    if usuario.is_authenticated:  # Verificar si el usuario está autenticado
        if usuario.codPer.codPer != 4:
            return redirect("acceso_no_autorizado")

        trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
        funcion = Artesano.objects.get(codTra=usuario.codTra.codTra)
        bodega = Bodega.objects.get(codBod=funcion.codBod.codBod)

        return render(
            request,
            "templateSBD/artesano.html",
            {
                "trabajador": trabajador,
                "funcion": funcion,
                "actividad": "Artesano",
                "bodega": bodega,
            },
        )
    else:
        # El usuario no está autenticado, realizar acción específica
        return render(request, "templateSBD/sin_credenciales.html")


@login_required
def art_busqueda_telas(request):
    usuario = request.user
    telas = None

    if usuario.codPer.codPer != 4:
        return redirect('acceso_no_autorizado')

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Artesano.objects.get(codTra=usuario.codTra.codTra)
    bodega = Bodega.objects.get(codBod=funcion.codBod.codBod)

    # Define los formularios para los cuatro filtros
    form_principal = FormbusquedaCp(request.POST if request.method == 'POST' else None)
    form_secundario = FormbusquedaCs(request.POST if request.method == 'POST' else None)
    form_patron = FormbusquedaPt(request.POST if request.method == 'POST' else None)
    form_tipo_tela = FormbusquedaTt(request.POST if request.method == 'POST' else None)
    form_cod_tela = FormbusquedaTela(request.POST if request.method == 'POST' else None)



    if request.method == 'POST':
        if form_principal.is_valid():
            # Procesar búsqueda por color principal
            telas = Tela.objects.filter(codCp=form_principal.cleaned_data['codCp'], exiSt=True)
        elif form_secundario.is_valid():
            # Procesar búsqueda por color secundario
            telas = Tela.objects.filter(codCs=form_secundario.cleaned_data['codCs'], exiSt=True)
        elif form_patron.is_valid():
        # Procesar búsqueda por patrón
            telas = Tela.objects.filter(codPt=form_patron.cleaned_data['codPt'], exiSt=True)
        elif form_tipo_tela.is_valid():
        # Procesar búsqueda por tipo de tela
            telas = Tela.objects.filter(codTt=form_tipo_tela.cleaned_data['codTt'], exiSt=True)
 
        elif form_cod_tela.is_valid():
            # Procesar búsqueda por código de tela
            cod_tela = form_cod_tela.cleaned_data['codTela'].codTela
            telas = Tela.objects.filter(codTela=cod_tela, exiSt=True )
       
                

    return render(request, 'templateSBD/art_busqueda.html', {
        'form_principal': form_principal,
        'form_secundario': form_secundario,
        'form_patron': form_patron,
        'form_tipo_tela': form_tipo_tela,
        'form_cod_tela': form_cod_tela,
        'telas': telas,
        'trabajador': trabajador,
        'funcion': funcion,
        'actividad': "Artesano",
        'bodega': bodega,
    })


# vistas del bodeguero
@login_required
def bodeguero(request):
    usuario = request.user

    if usuario.codPer.codPer != 3:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Bodeguero.objects.get(codTra=usuario.codTra.codTra)
    bodega = Bodega.objects.get(codBod=funcion.codBod.codBod)
    return render(
        request,
        "templateSBD/bodeguero.html",
        {
            "trabajador": trabajador,
            "funcion": funcion,
            "actividad": "Bodeguero",
            "bodega": bodega,
        },
    )



@login_required
def bod_g_muestras(request):
    usuario = request.user

    if usuario.codPer.codPer != 3:
        return redirect('acceso_no_autorizado')

    # Obtén la información del bodeguero y su bodega
    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Bodeguero.objects.get(codTra=usuario.codTra.codTra)
    bodega = funcion.codBod
    ubicaciones = Ubicacion.objects.filter(codBod=bodega, ubiStat=True)
    tela = Tela.objects.filter(exiSt=True)
    datos_ingresados = None


    if request.method == 'POST':
        form_regbodegam = RegBodegaMuestraForm(request.POST)
        if form_regbodegam.is_valid():
            codUbi = form_regbodegam.cleaned_data['codUbi']
            if codUbi.codBod != bodega:
                return redirect('bodeguero')  # Redirigir a una página de error 

            # Configura la fecha de ingreso automáticamente
            form_regbodegam.instance.fechaIngM = timezone.now()
            form_regbodegam.instance.codBode = funcion

            # sumar 1 a la ubicacion en cuanto a stock
            


            # Guarda el formulario directamente en la base de datos
            form_regbodegam.save()
            datos_ingresados = form_regbodegam.cleaned_data
            print(datos_ingresados)
            print(f"Datos del formulario: {form_regbodegam.cleaned_data}")
             # Crear un nuevo formulario limpio
            form_regbodegam = RegBodegaMuestraForm()

            # Puedes redirigir a una página de éxito o hacer lo que consideres apropiado
            return render(request, 'templateSBD/b_muestras.html', 
                  {'trabajador': trabajador, 
                    'funcion': funcion, 
                    'actividad': "Bodeguero", 
                    'bodega': bodega, 
                    'ubicaciones': ubicaciones,
                    'datos_ingresados': datos_ingresados,
                    'form_regbodegam': form_regbodegam})

    else:
        form_regbodegam = RegBodegaMuestraForm()
        form_regbodegam.fields['codUbi'].queryset = ubicaciones
        form_regbodegam.fields['codTela'].queryset = tela
        form_regbodegam.initial['cantidad'] = 1

    

    trabajador = usuario.codTra
    return render(request, 'templateSBD/b_muestras.html', 
                  {'trabajador': trabajador, 
                    'funcion': funcion, 
                    'actividad': "Bodeguero", 
                    'bodega': bodega, 
                    'ubicaciones': ubicaciones,
                    'form_regbodegam': form_regbodegam})

                   





@login_required
def bod_g_fardos(request):
    usuario = request.user
    

    if usuario.codPer.codPer != 3:
        return redirect('acceso_no_autorizado')

    # Obtén la información del bodeguero y su bodega
    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Bodeguero.objects.get(codTra=usuario.codTra.codTra)
    bodega = funcion.codBod
    ubicaciones = Ubicacion.objects.filter(codBod=bodega, ubiStat=True)
    fardos = Fardos.objects.filter(exiStF=True)
    datos_ingresados = None

    


    if request.method == 'POST':
        form_regbodegaf = RegBodegaFardoForm(request.POST)

        if form_regbodegaf.is_valid():
            codUbi = form_regbodegaf.cleaned_data['codUbi']
            if codUbi.codBod != bodega:
                return redirect('bodeguero')  # redirigir a una página de error 

            # Configura la fecha de ingreso automáticamente
            form_regbodegaf.instance.fechaIngFar = timezone.now()
            form_regbodegaf.instance.codBode = funcion

            # Guarda el formulario directamente en la base de datos
            form_regbodegaf.save()
            datos_ingresados = form_regbodegaf.cleaned_data
            print(f"Datos del formulario: {form_regbodegaf.cleaned_data}")
            form_regbodegaf = RegBodegaFardoForm()

            # Agregar declaraciones de print
            

            # Puedes redirigir a una página de éxito o hacer lo que consideres apropiado
            return render(request, 'templateSBD/b_fardos.html', 
                  {'trabajador': trabajador, 
                    'funcion': funcion, 
                    'actividad': "Bodeguero", 
                    'bodega': bodega, 
                    'ubicaciones': ubicaciones,
                    'datos_ingresados': datos_ingresados,
                    'form_regbodegaf': form_regbodegaf})
    else:
        # Si la solicitud no es un envío de formulario, crea una instancia del formulario
        form_regbodegaf = RegBodegaFardoForm()
        form_regbodegaf.fields['codUbi'].queryset = ubicaciones
        form_regbodegaf.fields['codFar'].queryset = fardos 
        form_regbodegaf.initial['cantidad'] = 1
        

    trabajador = usuario.codTra
    return render(request, 'templateSBD/b_fardos.html', 
                  {'trabajador': trabajador, 
                   'funcion': funcion, 
                   'actividad': "Bodeguero", 
                   'bodega': bodega, 
                   'ubicaciones': ubicaciones,
                   'form_regbodegaf': form_regbodegaf})

@login_required
def bod_espacios(request):
    usuario = request.user
    

    if usuario.codPer.codPer != 3:
        return redirect('acceso_no_autorizado')
    
    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion= Bodeguero.objects.get(codTra=usuario.codTra.codTra)
    bodega= Bodega.objects.get(codBod=funcion.codBod.codBod)

    ubicaciones = Ubicacion.objects.filter(codBod=bodega, ubiStat=True)
    

    return render(request, 'templateSBD/b_espacios.html', {
        'trabajador': trabajador,
        'funcion': funcion,
        'ubicaciones': ubicaciones,
        'actividad': "Bodeguero",
        'bodega': bodega,
    })


@login_required
def bod_busqueda_telas(request):
    usuario = request.user
    telas = None

    if usuario.codPer.codPer != 3:
        return redirect('acceso_no_autorizado')
    
    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion= Bodeguero.objects.get(codTra=usuario.codTra.codTra)
    bodega= Bodega.objects.get(codBod=funcion.codBod.codBod)

    # Define los formularios para los cuatro filtros
    form_principal = FormbusquedaCp(request.POST if request.method == 'POST' else None)
    form_secundario = FormbusquedaCs(request.POST if request.method == 'POST' else None)
    form_patron = FormbusquedaPt(request.POST if request.method == 'POST' else None)
    form_tipo_tela = FormbusquedaTt(request.POST if request.method == 'POST' else None)
    form_cod_tela = FormbusquedaTela(request.POST if request.method == 'POST' else None)



    if request.method == 'POST':
        if form_principal.is_valid():
            # Procesar búsqueda por color principal
            telas = Tela.objects.filter(codCp=form_principal.cleaned_data['codCp'],exiSt=True)
        elif form_secundario.is_valid():
            # Procesar búsqueda por color secundario
            telas = Tela.objects.filter(codCs=form_secundario.cleaned_data['codCs'],exiSt=True)
        elif form_patron.is_valid():
        # Procesar búsqueda por patrón
            telas = Tela.objects.filter(codPt=form_patron.cleaned_data['codPt'],exiSt=True)
        elif form_tipo_tela.is_valid():
        # Procesar búsqueda por tipo de tela
            telas = Tela.objects.filter(codTt=form_tipo_tela.cleaned_data['codTt'],exiSt=True)
        elif form_cod_tela.is_valid():
            # Procesar búsqueda por código de tela
            cod_tela = form_cod_tela.cleaned_data['codTela'].codTela
            telas = Tela.objects.filter(codTela=cod_tela)
        
                

    return render(request, 'templateSBD/b_busqueda.html', {
        'form_principal': form_principal,
        'form_secundario': form_secundario,
        'form_patron': form_patron,
        'form_tipo_tela': form_tipo_tela,
        'form_cod_tela': form_cod_tela,

        'telas': telas,
        'trabajador': trabajador,
        'funcion': funcion,
        'actividad': "Bodeguero",
        'bodega': bodega,
    })
# vistas del administrador de bodega


@login_required
def administrador_bodega(request):
    usuario = request.user

    if usuario.codPer.codPer != 2:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)
    return render(
        request,
        "templateSBD/a_bodega.html",
        {
            "trabajador": trabajador,
            "funcion": funcion,
            "actividad": "Administrador Bodega",
            "bodega": bodega,
        },
    )


@login_required
def bod_historico(request):
    usuario = request.user
    form=formMovFar(request.POST if request.method == 'POST' else None)
    if usuario.codPer.codPer != 2:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)
    ubicaciones = Ubicacion.objects.filter(codBod=bodega)   # LINEA PARA BUSCAR LAS UBICACIONES PERTENECIENTES A LA BODEGA
    bodegueros = Bodeguero.objects.filter(codBod=bodega)    #  Filtra los bodegueros correspondientes a una bodega

    consulta1 =Q()  # Variable vacia para almacenar multiples consultas 
 

    for ubicacion in ubicaciones: # linea para agregar multiples consultas a la variable vacia
        consulta1 |= Q(codUbi=ubicacion)


    registros_fardos=RegBodegaFar.objects.filter(consulta1)   # LINEA PARA ejecutar las multiples consultas y filtrar
    form.fields['codUbi'].queryset = Ubicacion.objects.filter(consulta1)  # ajusta los campos de acuerdo a las consultas anteriores

    form.fields['codBode'].queryset = bodegueros



    if "ubicacion" in request.POST :
        print("recibo la informacion")
        busqueda_ubicacion= request.POST['codUbi']
        print(busqueda_ubicacion)
        registros_fardos=RegBodegaFar.objects.filter(codUbi=busqueda_ubicacion)
        print(registros_fardos)
        print(len(registros_fardos))


        return render(request, 'templateSBD/a_movimientos.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Administrador Bodega','bodega': bodega,
                'form': form,"registros":registros_fardos # Pasa el objeto tela guardado al contexto
            })
    
    
    elif "tipo_mov" in request.POST :
        print("recibo la informacion")
        busqueda_movimiento= request.POST['codMovF']
        print(busqueda_movimiento)
        registros_fardos=RegBodegaFar.objects.filter(codMovF=busqueda_movimiento)   # rimera consulta para obtener por tipo de movimiento
        registros_fardos = registros_fardos.filter(codUbi__codBod=bodega)  # Segunda consulta para filtrar por bodega


        return render(request, 'templateSBD/a_movimientos.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Administrador Bodega','bodega': bodega,
                'form': form,"registros":registros_fardos # Pasa el objeto tela guardado al contexto
            })
    
    elif "bodeguero" in request.POST :
        print("recibo la informacion")
        busqueda_bodeguero= request.POST['codBode']
        print(busqueda_bodeguero)
        registros_fardos=RegBodegaFar.objects.filter(codBode=busqueda_bodeguero)

        return render(request, 'templateSBD/a_movimientos.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Administrador Bodega','bodega': bodega,
                'form': form,"registros":registros_fardos # Pasa el objeto tela guardado al contexto
            })

    elif "fecha" in request.POST:
        print("recibo la informacion")
        busqueda_mes= request.POST['mes']
        print(busqueda_mes)
        registros_fardos = RegBodegaFar.objects.filter(fechaIngFar__month=busqueda_mes)
        registros_fardos = registros_fardos.filter(codUbi__codBod=bodega) 

        return render(request, 'templateSBD/a_movimientos.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Administrador Bodega','bodega': bodega,
                'form': form,"registros":registros_fardos # Pasa el objeto tela guardado al contexto
            })

    elif "year" in request.POST:
        print("recibo la informacion")
        busqueda_year = request.POST['years']
        print(busqueda_year)

        registros_fardos = RegBodegaFar.objects.filter(fechaIngFar__year=busqueda_year)
        registros_fardos = registros_fardos.filter(codUbi__codBod=bodega) 

        return render(request, 'templateSBD/a_movimientos.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Administrador Bodega','bodega': bodega,
                'form': form,"registros":registros_fardos # Pasa el objeto tela guardado al contexto
            })

    elif "fecha_c" in request.POST:
        print("recibo la informacion")
        busqueda_fechaC= request.POST['fechaIngFar']
        print(busqueda_fechaC)
        registros_fardos = RegBodegaFar.objects.filter(fechaIngFar=busqueda_fechaC)
        registros_fardos = registros_fardos.filter(codUbi__codBod=bodega) 

        return render(request, 'templateSBD/a_movimientos.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Administrador Bodega','bodega': bodega,
                'form': form,"registros":registros_fardos # Pasa el objeto tela guardado al contexto
            })


    return render(
            request,
            "templateSBD/a_movimientos.html",
            {
                "trabajador": trabajador,
                "funcion": funcion,
                "actividad": "Administrador Bodega",
                "bodega": bodega,
                "form":form,
                "registros":registros_fardos
            },
        )


def bod_historico_muestras(request):
    usuario = request.user
    form=formMovMuestra(request.POST if request.method == 'POST' else None)
    if usuario.codPer.codPer != 2:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)
    ubicaciones = Ubicacion.objects.filter(codBod=bodega)   # LINEA PARA BUSCAR LAS UBICACIONES PERTENECIENTES A LA BODEGA
    bodegueros = Bodeguero.objects.filter(codBod=bodega)    #  Filtra los bodegueros correspondientes a una bodega

    consulta1 =Q()  # Variable vacia para almacenar multiples consultas 
 

    for ubicacion in ubicaciones: # linea para agregar multiples consultas a la variable vacia
        consulta1 |= Q(codUbi=ubicacion)

    
    registros_muestras=RegBodegaMuestra.objects.filter(consulta1)
    registros_muestras = registros_muestras.filter(codUbi__codBod=bodega) 
    registros_muestras = registros_muestras.filter(codUbi__codBod=bodega).order_by('-fechaIngM')
    print(registros_muestras)

    form.fields['codUbi'].queryset = Ubicacion.objects.filter(consulta1)
    form.fields['codBode'].queryset = bodegueros  


    if "ubicacion_m" in request.POST :
        print("recibo la informacion")
        busqueda_ubicacion= request.POST['codUbi']
        print(busqueda_ubicacion)
        registros_muestras=RegBodegaMuestra.objects.filter(codUbi=busqueda_ubicacion)
        print(registros_muestras)

        return render(request, 'templateSBD/a_movimientos_m.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Administrador Bodega','bodega': bodega,
                'form': form,"registros":registros_muestras # Pasa el objeto tela guardado al contexto
            })
    
    
    elif "tipo_mov" in request.POST :
        print("recibo la informacion")
        busqueda_movimiento= request.POST['codMovM']
        print(busqueda_movimiento)
        registros_muestras=RegBodegaMuestra.objects.filter(codMovM=busqueda_movimiento)   # rimera consulta para obtener por tipo de movimiento
        registros_muestras = registros_muestras.filter(codUbi__codBod=bodega)  # Segunda consulta para filtrar por bodega


        return render(request, 'templateSBD/a_movimientos_m.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Administrador Bodega','bodega': bodega,
                'form': form,"registros":registros_muestras # Pasa el objeto tela guardado al contexto
            })
    
    elif "bodeguero" in request.POST :
        print("recibo la informacion")
        busqueda_bodeguero= request.POST['codBode']
        print(busqueda_bodeguero)
        registros_muestras=RegBodegaMuestra.objects.filter(codBode=busqueda_bodeguero)

        return render(request, 'templateSBD/a_movimientos_m.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Administrador Bodega','bodega': bodega,
                'form': form,"registros":registros_muestras # Pasa el objeto tela guardado al contexto
            })

    elif "fecha" in request.POST:
        print("recibo la informacion")
        busqueda_mes= request.POST['mes']
        print(busqueda_mes)
        registros_muestras= RegBodegaMuestra.objects.filter(fechaIngM__month=busqueda_mes)
        registros_muestras = registros_muestras.filter(codUbi__codBod=bodega) 

        return render(request, 'templateSBD/a_movimientos_m.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Administrador Bodega','bodega': bodega,
                'form': form,"registros":registros_muestras # Pasa el objeto tela guardado al contexto
            })

    elif "year" in request.POST:
        print("recibo la informacion")
        busqueda_year = request.POST['years']
        print(busqueda_year)

        registros_muestras = RegBodegaMuestra.objects.filter(fechaIngM__year=busqueda_year)
        registros_muestras = registros_muestras.filter(codUbi__codBod=bodega) 

        return render(request, 'templateSBD/a_movimientos_m.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Administrador Bodega','bodega': bodega,
                'form': form,"registros":registros_muestras # Pasa el objeto tela guardado al contexto
            })

    elif "fecha_c" in request.POST:
        print("recibo la informacion")
        busqueda_fechaC= request.POST['fechaIngM']
        print(busqueda_fechaC)
        registros_muestras = RegBodegaMuestra.objects.filter(fechaIngM=busqueda_fechaC)
        registros_muestras = registros_muestras.filter(codUbi__codBod=bodega) 


        return render(request, 'templateSBD/a_movimientos_m.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Administrador Bodega','bodega': bodega,
                'form': form,"registros":registros_muestras # Pasa el objeto tela guardado al contexto
            })

    return render(
            request,
            "templateSBD/a_movimientos_m.html",
            {
                "trabajador": trabajador,
                "funcion": funcion,
                "actividad": "Administrador Bodega",
                "bodega": bodega,
                "form":form,
                "registros":registros_muestras
            },
        )






@login_required
def gestion_espacios(request):
    usuario = request.user
    pasillo_creado= None
    

    if usuario.codPer.codPer != 2:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)
    ubicaciones=Ubicacion.objects.filter(codBod=bodega)

    form1 = formPasillos(
    initial={'codBod': bodega.codBod},  # Datos iniciales para el formulario (prellenar el campo codBod)
    data=request.POST if request.method == 'POST' else None)


 
    if "pasillos_y_espacios" in request.POST:

        print("Recibi el formulario en el primero")

        codigo_bodega=request.POST['codBod']
        print(codigo_bodega)
        numero_pasillo = int(request.POST['num_pasillo'])
        print(numero_pasillo)
        division_pasillo=request.POST['division']
        print(division_pasillo)

        cod_bod=Bodega.objects.get(codBod=codigo_bodega)

        if not division_pasillo or division_pasillo.isspace() or not numero_pasillo :
            messages.error(request, "Error en campo division, no pueden estar vacio")
            print("datos invalidos")

        elif not (1 <= numero_pasillo <= bodega.cantPas):
            messages.error(request, "Error en campo numerico, no pueden ser menor que 1 o mayor que el numero pasillos")
            print("datos invalidos")

        elif len(division_pasillo) > 13:
            messages.error(request, "El division pasillo no puede tener mas de 13 caracteres")
            print("datos inválidos")

        else:
            pasillo_completo = str(numero_pasillo) + "-"+division_pasillo
            if form1.is_valid():

                pasillo_creado = Ubicacion(
                codUbi=pasillo_completo,
                codBod=cod_bod,
                ubiStat=True,
                stock=0
                )

            pasillo_creado.save()

            print("he creado el pasillo")

            pasillo_guardado=Ubicacion.objects.get(pk=pasillo_creado.pk)

            print("Formulario guardado")

            

            return render(request, 'templateSBD/a_pasillos.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Administrador Bodega','bodega': bodega,
                'form1': form1,'pasillo_guardado': pasillo_guardado,"form2":ubicaciones, # Pasa el objeto tela guardado al contexto
                })

    elif "activar" in request.POST:
        cod_Ubi = request.POST.get('activar')
        pasillo_modificar=Ubicacion.objects.get(codUbi=cod_Ubi)
        print(pasillo_modificar)
        pasillo_modificar=Ubicacion.objects.get(codUbi=cod_Ubi)
        print(pasillo_modificar)
        pasillo_modificar.ubiStat = True
        pasillo_modificar.save()

        return render(request, 'templateSBD/a_pasillos.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Administrador Bodega','bodega': bodega,
                'form1': form1,"form2":ubicaciones, # Pasa el objeto tela guardado al contexto
                })
    
    elif "desactivar" in request.POST:
        print(request.POST)
        print("Recibi la info")
        cod_Ubi = request.POST.get('desactivar')  
        print(cod_Ubi)
        pasillo_modificar=Ubicacion.objects.get(codUbi=cod_Ubi)
        print(pasillo_modificar)
        pasillo_modificar.ubiStat = False
        pasillo_modificar.save()

        print("Pasillo desactivado")

        return render(request, 'templateSBD/a_pasillos.html', {'trabajador': trabajador,'funcion': funcion,'actividad': 'Administrador Bodega','bodega': bodega,
                'form1': form1,"form2":ubicaciones, # Pasa el objeto tela guardado al contexto
                })

    
    return render(
        request,
        "templateSBD/a_pasillos.html",
        {
            "trabajador": trabajador,
            "funcion": funcion,
            "actividad": "Administrador Bodega",
            "bodega": bodega,
            "form1":form1,
            "form2":ubicaciones,
        },
    )


# vistas del super admin


@login_required
def s_administrador(request):
    usuario = request.user

    if usuario.codPer.codPer != 1:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)

    return render(
        request,
        "templateSBD/s_admin.html",
        {
            "trabajador": trabajador,
            "funcion": funcion,
            "actividad": "S.administrador",
            "bodega": bodega,
        },
    )


@login_required
def gestion_bodegaF(request):
    usuario = request.user

    if usuario.codPer.codPer != 1:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)

    desactivar_bodega = DesactivarBodegaForm()
    modificar_bodega = ModificarBodegaForm()
    if request.method == "POST":
        formBodega = FormBodega(request.POST)
        if formBodega.is_valid():
            # Obten los datos del formulario
            nomBod = formBodega.cleaned_data["nomBod"].upper()
            dirBod = formBodega.cleaned_data["dirBod"].upper()
            cantPas = formBodega.cleaned_data["cantPas"]
            comuna = formBodega.cleaned_data["codCom"]
            status = formBodega.cleaned_data["status"]
            # Crea una nueva bodega en la base de datos
            bodega = Bodega.objects.create(
                nomBod=nomBod,
                dirBod=dirBod,
                cantPas=cantPas,
                codCom=comuna,
                status=status,
            )
            # Redirige al usuario a una página de éxito o donde desees
            return redirect("listar_bodegas")
        else:
            return HttpResponse("El formulario no es válido. Verifica los campos.")
    else:
        formBodega = FormBodega()

    return render(
        request,
        "templateSBD/s_gestionbodegaF.html",
        {
            "trabajador": trabajador,
            "funcion": funcion,
            "actividad": "S.administrador",
            "bodega": bodega,
            "formBodega": formBodega,
            "desactivar_bodega": desactivar_bodega,
            "modificar_bodega": modificar_bodega,
        },
    )


@login_required
def desactivar_bodega(request):
    usuario = request.user

    if usuario.codPer.codPer != 1:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)

    if request.method == "POST":
        formDB = DesactivarBodegaForm(request.POST)
        if formDB.is_valid():
            bodega_instance = formDB.cleaned_data[
                "bodega"
            ]  # Obtiene la instancia de la bodega
            bodega_id = (
                bodega_instance.pk
            )  # Obtiene la clave primaria (número) de la bodega
            # Desactivar la bodega (establecer status en False)
            bodega = Bodega.objects.get(pk=bodega_id)
            bodega.status = False
            bodega.save()
            # Redirigir a una página de éxito o donde desees
            return redirect("listar_bodegas")
        else:
            print(formDB.errors)
            return HttpResponse("El formulario no es válido. Verifica los campos.")
    else:
        formDB = DesactivarBodegaForm()

    return render(
        request,
        "templateSBD/s_gestionbodegaF.html",
        {
            "trabajador": trabajador,
            "funcion": funcion,
            "actividad": "S.administrador",
            "bodega": bodega,
            "formDB": formDB,
        },
    )



# vista para modificar nombre y direccion de las bodegas fisicas en el superAdministrador
@login_required
def modificar_bodega(request):
    usuario = request.user

    if usuario.codPer.codPer != 1:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)

    if request.method == "POST":
        formMB = ModificarBodegaForm(request.POST)
        if formMB.is_valid():
            codBod = formMB.cleaned_data["bodega"].codBod  # Usar codBod en lugar de id
            nomBod = formMB.cleaned_data["nomBod"].upper()
            dirBod = formMB.cleaned_data["dirBod"].upper()

            # Actualiza la información de la bodega
            bodega = Bodega.objects.get(codBod=codBod)  # Usar codBod en lugar de id
            if nomBod:
                bodega.nomBod = nomBod
            if dirBod:
                bodega.dirBod = dirBod

            bodega.save()

            return redirect("listar_bodegas")
        else:
            print(formMB.errors)
            return HttpResponse("El formulario no es válido. Verifica los campos.")

    else:
        formMB = ModificarBodegaForm()

    return render(
        request,
        "templateSBD/s_gestionbodegaF.html",
        {
            "trabajador": trabajador,
            "funcion": funcion,
            "actividad": "S.administrador",
            "bodega": bodega,
            "formMB": formMB,
        },
    )

@login_required
def listar_bodegas(request):
    usuario = request.user

    if usuario.codPer.codPer != 1:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)

    listar_bodegas= Bodega.objects.all()
   
      
    return render(
        request,
        "templateSBD/s_listar_bodegas.html",
        {
            "trabajador": trabajador,
            "funcion": funcion,
            "actividad": "S.administrador",
            "bodega": bodega,
            'listar_bodegas':listar_bodegas
        },
    )

    
@login_required
def gestion_clasificacion(request):
    usuario = request.user

    if usuario.codPer.codPer != 1:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)

    agregar_colores_p =FormAgregarColorP() 
    agregar_colores_s =FormAgregarColorS()
    agregar_patrones_tela =FormAgregarPatronesT()
    agregar_tipos_tela = FormAgregartiposT()
    return render(
        request,
        "templateSBD/s_gestionclasificacion.html",
        {
            "trabajador": trabajador,
            "funcion": funcion,
            "actividad": "S.administrador",
            "bodega": bodega,
            'agregar_colores_p': agregar_colores_p,
            'agregar_colores_s': agregar_colores_s,
            'agregar_patrones_tela': agregar_patrones_tela,
            'agregar_tipos_tela': agregar_tipos_tela,
        },
    )

@login_required
def movimientos_historicos(request):
    usuario = request.user

    if usuario.codPer.codPer != 1:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)

    form = FiltrosMovimientosForm(request.GET)
    
    registros_far = RegBodegaFar.objects.all()
    registros_muestra = RegBodegaMuestra.objects.all()
    

    show_tables_far = False
    show_tables_muestra = False

    if request.GET and form.is_valid():
        codigo_movimiento_far = form.cleaned_data.get('codigo_movimiento_far')
        codigo_movimiento_muestra = form.cleaned_data.get('codigo_movimiento_muestra')
        cod_bodeguero_far = form.cleaned_data.get('cod_bodeguero_far')
        cod_bodeguero_muestra = form.cleaned_data.get('cod_bodeguero_muestra')
        print("Valor de cod_bodeguero_far:", cod_bodeguero_far)  # Agrega esta línea para imprimir el valor
        print("Valor de cod_bodeguero_muestra:", cod_bodeguero_muestra)  # Agrega esta línea para imprimir el valor
        if codigo_movimiento_far:
            registros_far = registros_far.filter(codMovF=codigo_movimiento_far)
            show_tables_far = True
        
        if cod_bodeguero_far:
            registros_far = registros_far.filter(codBode=cod_bodeguero_far)
            show_tables_far = True

        if codigo_movimiento_muestra:
            registros_muestra = registros_muestra.filter(codMovM=codigo_movimiento_muestra)
            show_tables_muestra = True
        
        if cod_bodeguero_muestra:
            registros_muestra = registros_muestra.filter(codBode=cod_bodeguero_muestra)
            show_tables_muestra = True

    return render(
        request, 
        'templateSBD/s_movimientos.html', 
        {
            "trabajador": trabajador,
            "funcion": funcion,
            "actividad": "S.administrador",
            "bodega": bodega,
            'RegBodegaFar': registros_far,
            'RegBodegaMuestra': registros_muestra,
            'form': form,
            'show_tables_far': show_tables_far,
            'show_tables_muestra': show_tables_muestra,
        }
    )


@login_required
def gestion_trabajadores(request):
    usuario = request.user

    if usuario.codPer.codPer != 1:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)
    
    agregar_trabajadores = FormAgregarTrabajadores()
    
    formMT=FormModificarTrabajadores()
    # desactivar_trabajador = DesactivarTrabajadorForm
    return render(
        request,
        "templateSBD/s_gestiontrabajadores.html",
        {
            "trabajador": trabajador,
            "funcion": funcion,
            "actividad": "S.administrador",
            "bodega": bodega,
            'agregar_trabajadores':agregar_trabajadores,
            'formMT':formMT
        },
    )

@login_required
def agregar_clasificacion(request, tipo):
    usuario = request.user

    if usuario.codPer.codPer != 1:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)
    bodega = Bodega.objects.get(codBod=funcion.codBod)

    if tipo == "color_p":
        form_class = FormAgregarColorP
        model = ColorPrincipal
        field_name = "nomCp"
    elif tipo == "color_s":
        form_class = FormAgregarColorS
        model = ColorSecundario
        field_name = "nomCs"
    elif tipo == "patron_tela":
        form_class = FormAgregarPatronesT
        model = Patron
        field_name = "nomPt"
    elif tipo == "tipo_tela":
        form_class = FormAgregartiposT
        model = TipoTela
        field_name = "nomTt"
    else:
        return HttpResponse("Tipo de clasificación no válido.")

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            data = {field_name: form.cleaned_data[field_name].upper()}
            model.objects.create(**data)
            return redirect("gestion_clasificacion")
        else:
            print(form.errors)
            return HttpResponse("El formulario no es válido, verifique los campos.")
    else:
        form = form_class()

    return render(
        request,
        "templateSBD/s_gestionclasificacion.html",
        {
            "trabajador": trabajador,
            "funcion": funcion,
            "actividad": "S.administrador",
            "bodega": bodega,
            "form": form,
        },
    )

@login_required
def agregar_trabajadores(request):
    usuario = request.user

    if usuario.codPer.codPer != 1:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)

    if request.method == 'POST':
        formAgregarTrabajador = FormAgregarTrabajadores(request.POST)
        if formAgregarTrabajador.is_valid():
            rutTra = formAgregarTrabajador.cleaned_data["rutTra"]
            nomTra = formAgregarTrabajador.cleaned_data["nomTra"].upper()
            dirTra = formAgregarTrabajador.cleaned_data["dirTra"].upper()
            telTra = formAgregarTrabajador.cleaned_data["telTra"]
            emailTra = formAgregarTrabajador.cleaned_data["emailTra"]
            codCom = formAgregarTrabajador.cleaned_data["codCom"]

            nuevo_trabajador = Trabajadores.objects.create(
                rutTra = rutTra,
                nomTra = nomTra, 
                dirTra = dirTra,
                telTra = telTra ,
                emailTra = emailTra, 
                codCom = codCom ,
            )
            return redirect('listar_trabajadores')
        else: 
            return HttpResponse("El formulario no es valido, verifica los campos.")
    else:
        formAgregarTrabajador = FormAgregarTrabajadores()
    return render(
        request,
        "templateSBD/s_gestiontrabajadores.html",
        {
            "trabajador": trabajador,
            "funcion": funcion,
            "actividad": "S.administrador",
            "bodega": bodega,
            'formAgregarTrabajador':formAgregarTrabajador,
        },
    )

@login_required
def listar_trabajadores(request):
    usuario = request.user

    if usuario.codPer.codPer != 1:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)

    listar_trabajadores= Trabajadores.objects.all()
   
      
    return render(
        request,
        "templateSBD/s_listar_trabajadores.html",
        {
            "trabajador": trabajador,
            "funcion": funcion,
            "actividad": "S.administrador",
            "bodega": bodega,
            'listar_trabajadores':listar_trabajadores
        },
    )


@login_required
def modificar_trabajador(request,codTra):
    usuario = request.user

    if usuario.codPer.codPer != 1:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)

    trabajador_1 = Trabajadores.objects.get(codTra=codTra)
    formMT = FormModificarTrabajadores(instance=trabajador_1)
    if request.method == 'POST' :
        formMT = FormModificarTrabajadores(request.POST, instance=trabajador_1)
        if formMT.is_valid():
            formMT.save()
        return redirect('listar_trabajadores')
    
    return render(request, 'templateSBD/s_modificar_trabajador.html', {
                "trabajador": trabajador,
                "funcion": funcion,
                "actividad": "S.administrador",
                "bodega": bodega,
                'formMT' : formMT,
                })

def asignar_usuario(request, codTra):
    
    trabajador = Trabajadores.objects.get(codTra=codTra)

    # Verificar si el trabajador ya tiene un usuario asignado
    if Usuario.objects.filter(codTra=trabajador).exists():
        # Puedes manejar la situación aquí, por ejemplo, redirigiendo a otra página o mostrando un mensaje de error.
        
        return HttpResponse("El formulario no es valido, verifica los campos.")

    if request.method == 'POST':
        # Procesar el formulario enviado
        formAS = FormAsignarUsuarios(request.POST)
        if formAS.is_valid():
            # Crear el usuario asignado
            nuevo_usuario = formAS.save(commit=False)

            passW = formAS.cleaned_data.get('passW')
            nuevo_usuario.set_password(passW)

            nuevo_usuario.codTra = trabajador
            nuevo_usuario.save()

            
            return redirect('listar_trabajadores')  # Cambia esto a la URL correcta
    else:
        # Mostrar el formulario con datos precargados
        formAS = FormAsignarUsuarios(initial={'codTra': trabajador, 'codUser': trabajador.rutTra})

    return render(request, 'templateSBD/s_asignarUsuario.html', {
        'trabajador': trabajador,
        'formAS': formAS,
    })


@login_required
def asignarFuncion(request, codTra):
    usuario = request.user

    if usuario.codPer.codPer != 1:
        return redirect("acceso_no_autorizado")

    trabajador = Trabajadores.objects.get(codTra=usuario.codTra.codTra)
    funcion = Administrador.objects.get(codTra=usuario.codTra.codTra)  #
    bodega = Bodega.objects.get(codBod=funcion.codBod)
    form = FormAsignarFuncion(initial={'codTra': codTra})

    if request.method == 'POST':
        form = FormAsignarFuncion(request.POST)
        if form.is_valid():
            tipo_funcion = form.cleaned_data['tipo_funcion']
            codBod = form.cleaned_data['codBod']

            trabajador = Trabajadores.objects.get(pk=codTra)

            if tipo_funcion == 'bodeguero':
                nuevo_funcionario = Bodeguero.objects.create(
                    codTra=trabajador,
                    codBod=codBod
                )
            elif tipo_funcion == 'artesano':
                nuevo_funcionario = Artesano.objects.create(
                    codTra=trabajador,
                    codBod=codBod
                )
            elif tipo_funcion == 'recolector':
                nuevo_funcionario = Recolectores.objects.create(
                    codTra=trabajador,
                    codBod=codBod
                )
            elif tipo_funcion == 'clasificador':
                nuevo_funcionario = Clasificadores.objects.create(
                    codTra=trabajador,
                    codBod=codBod
                )

            return redirect('listar_trabajadores')

    return render(request, 'templateSBD/s_asignarFuncion.html', {
        "trabajador": trabajador,
        "funcion": funcion,
        "actividad": "S.administrador",
        "bodega": bodega,
        'form': form,
        'codTra': codTra,
    })


def desactivar_trabajador(request, codTra):
    # Buscar al trabajador
    trabajador = Trabajadores.objects.get(codTra=codTra)

    # Buscar al usuario asociado al trabajador
    usuario = Usuario.objects.get(codTra=trabajador)

    # Buscar el perfil 'INACTIVO'
    perfil_inactivo = Perfil.objects.get(codPer=7)

    # Actualizar el perfil del usuario al perfil 'INACTIVO'
    usuario.codPer = perfil_inactivo
    usuario.save()

    return redirect('listar_trabajadores')