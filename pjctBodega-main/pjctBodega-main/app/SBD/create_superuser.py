from SBDcrud.models import Usuario, Trabajadores,Perfil

# Asegúrate de que haya un registro en Trabajadores con id=1
try:
    trabajador = Trabajadores.objects.get(pk=1)
    perfil = Perfil.objects.get(pk=1)
except Trabajadores.DoesNotExist:
    print("No se encontró un registro de Trabajadores con id=1")
    trabajador = None

if trabajador:
    # Crea el usuario
    usuario = Usuario.objects.create(codUser=123456789, passW='nonos123', codTra=trabajador, codPer=perfil)
    usuario.set_password('nonos123')
    usuario.is_superuser = True  # Establece a True para otorgar permisos de superusuario
    usuario.is_staff = True
    usuario.save()
    print('Usuario creado con éxito')
else:
     print("No se pudo crear el usuario debido a que no se encontró un registro de Trabajadores con id=1.")
