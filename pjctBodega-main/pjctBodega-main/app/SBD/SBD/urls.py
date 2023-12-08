"""
URL configuration for SBD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from SBDcrud import views
from SBDcrud.views import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('noaccesso/', views.acceso_no_autorizado, name='acceso_no_autorizado'),
    path('sin_credenciales/',views.sinCredencial, name='sin_credencial'),

    path('recolector/', views.recolector, name='recolector'),
    path('r_ingresofardo/', views.ingreso_fardoBD, name='ingreso_fardo'),
    path('crear_fardo/',views.guardar_fardo,name='guardar_fardo'),
    path('R_busqueda/', views.Ringreso_busqueda,name='Rbusqueda_muestras'),
    path('buscar_Tf/', views.Rbusqueda_muestra,name='R_portipofardo'),

    path('clasificador/', views.clasificador, name='clasificador'),
    path('c_ingresomuestrasbd/', views.ingreso_muestrasBD,name='ingreso_muestrasbd'),
    path('c_busqueda/', views.Cingreso_busqueda,name='Cbusqueda_muestras'),
    path('c_busqueda_muestra/', views.Cbusqueda_muestras,name='busqueda_muestrasC'),
    

    path('artesano/', views.artesano, name='artesano'),
    path('art_busqueda', views.art_busqueda_telas, name='artesano_busqueda'),

    path('bodeguero/', views.bodeguero, name='bodeguero'),
    path('b_muestrasg/', views.bod_g_muestras, name='g_muestras'),
    path('b_busqueda/', views.bod_busqueda_telas, name='busqueda'),
    path('b_fardos/', views.bod_g_fardos, name='g_fardos'),
    path('b_espacios/', views.bod_espacios, name='b_espacios'),


    path('a_bodega/', views.administrador_bodega, name='administrador_bodega'),
    path('a_movimientos/', views.bod_historico, name='movimientos_bodega'),
    path('a_pasillos/', views.gestion_espacios, name='pasillos_y_espacios'),
    path('a_movimientos_m/', views.bod_historico_muestras, name='movimientos_bodega_m'),

    path('s_admin/', views.s_administrador, name='s_admin'),
    path('s_gestiontrabajadores/',views.gestion_trabajadores, name='gestionPlanilla'),
    path('s_movimimientos/', views.movimientos_historicos, name='movimientos'),
    path('s_gestionbodegaF/', views.gestion_bodegaF, name='gestion_bodegaF'),
    path('s_gestionclasificacion/', views.gestion_clasificacion,name='gestion_clasificacion'),
    
    path('agregar_clasificacion/color_p/', views.agregar_clasificacion, {'tipo': 'color_p'}, name='agregar_colorP'),
    path('agregar_clasificacion/color_s/', views.agregar_clasificacion, {'tipo': 'color_s'}, name='agregar_colorS'),
    path('agregar_clasificacion/patron_tela/', views.agregar_clasificacion, {'tipo': 'patron_tela'}, name='agregar_patronT'),
    path('agregar_clasificacion/tipo_tela/', views.agregar_clasificacion, {'tipo': 'tipo_tela'}, name='agregar_tipoT'),

    path('crear_bodega/', views.gestion_bodegaF, name='crear_bodega'),
    path('desactivar_bodega/', views.desactivar_bodega, name='desactivar_bodega'),

    path('modificar_bodega/', views.modificar_bodega, name='modificar_bodega'),
    path('listar/', views.listar_bodegas, name='listar_bodegas'),
    
    path('agregar_trabajadores/', views.agregar_trabajadores, name='agregar_trabajadores'),
    path('modificar_trabajador/<int:codTra>', views.modificar_trabajador, name='modificar_trabajador'),
    path('listar_trabajadores/', views.listar_trabajadores, name='listar_trabajadores'),
    path('asignarUsuario/<int:codTra>', views.asignar_usuario, name='asignarUsuario'),
    path('desactivar_trabajador/<int:codTra>/', views.desactivar_trabajador, name='desactivar_trabajador'),
    path('asignarFuncion/<int:codTra>', views.asignarFuncion, name='asignarFuncion'),
    

]

handler404 = 'SBDcrud.views.handler404'