from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create your models here.


class UsuarioManager(BaseUserManager):
    def create_user(self, codUser, passW, codTra, codPer, **extra_fields):
        if not codUser:
            raise ValueError('El campo "codUser" es requerido.')
        user = self.model(codUser=codUser, codTra=codTra, codPer=codPer, **extra_fields)
        user.set_password(passW)
        user.save(using=self._db)
        return user

    def create_superuser(self, codUser, passW, codTra, codPer, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser debe tener is_superuser=True.")

        return self.create_user(codUser, passW, codTra, codPer, **extra_fields)


class Comuna(models.Model):
    codCom = models.IntegerField(primary_key=True)
    nomCom = models.CharField(max_length=30)

    def __str__(self):
        return self.nomCom


class Perfil(models.Model):
    codPer = models.IntegerField(primary_key=True)
    nomPer = models.CharField(max_length=30)

    def __str__(self):
        return str(self.nomPer)


class Trabajadores(models.Model):
    codTra = models.AutoField(primary_key=True)
    rutTra = models.IntegerField()
    nomTra = models.CharField(max_length=30)
    dirTra = models.CharField(max_length=30)
    telTra = models.CharField(max_length=30)
    emailTra = models.CharField(max_length=30)
    codCom = models.ForeignKey(Comuna, on_delete=models.CASCADE)

    def __str__(self):
        return str(
            self.codTra
        )  # Puedes elegir el campo que quieras mostrar en lugar de 'nomTra'


class Administrador(models.Model):
    codAdmin = models.AutoField(primary_key=True)
    codTra = models.ForeignKey(Trabajadores, on_delete=models.CASCADE)
    codBod = models.IntegerField()


class Bodega(models.Model):
    codBod = models.AutoField(primary_key=True)
    nomBod = models.CharField(max_length=30)
    dirBod = models.CharField(max_length=30)
    cantPas = models.IntegerField()
    codCom = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.nomBod


class Bodeguero(models.Model):
    codBode = models.AutoField(primary_key=True)
    codTra = models.ForeignKey(Trabajadores, on_delete=models.CASCADE)
    codBod = models.ForeignKey(Bodega, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.codTra.nomTra}"

class Recolectores(models.Model):
    codRec = models.AutoField(primary_key=True)
    codTra = models.ForeignKey(Trabajadores, on_delete=models.CASCADE)
    codBod = models.ForeignKey(Bodega, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.codRec)

class TipoFardo(models.Model):
    codTf = models.AutoField(primary_key=True)
    nomTf = models.CharField(max_length=30)

    
    def __str__(self):
        return self.nomTf


class Clasificadores(models.Model):
    codCla = models.IntegerField(primary_key=True)
    codTra = models.ForeignKey(Trabajadores, on_delete=models.CASCADE)
    codBod = models.ForeignKey(Bodega, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.codCla)


class TipoMovFardo(models.Model):
    codMovF = models.AutoField(primary_key=True)
    nomFar = models.CharField(max_length=30)

    def __str__(self):
        return self.nomFar


class TipoMovimientoM(models.Model):
    codMovM = models.AutoField(primary_key=True)
    nomMov = models.CharField(max_length=30)

    def __str__(self):
        return self.nomMov




class Ubicacion(models.Model):
    codUbi = models.CharField(max_length=15, primary_key=True)
    codBod = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    ubiStat = models.BooleanField()
    stock = models.IntegerField()

    def __str__(self):
        return str(self.codUbi)


class ColorPrincipal(models.Model):
    codCp = models.AutoField(primary_key=True)
    nomCp = models.CharField(max_length=30)

    def __str__(self):
        return self.nomCp


class ColorSecundario(models.Model):
    codCs = models.AutoField(primary_key=True)
    nomCs = models.CharField(max_length=30)

    def __str__(self):
        return self.nomCs


class TipoTela(models.Model):
    codTt = models.AutoField(primary_key=True)
    nomTt = models.CharField(max_length=30)

    def __str__(self):
        return self.nomTt


class Patron(models.Model):
    codPt = models.AutoField(primary_key=True)
    nomPt = models.CharField(max_length=30)

    def __str__(self):
        return self.nomPt


class Fardos(models.Model):
    codFar = models.AutoField(primary_key=True)
    codRec = models.ForeignKey(Recolectores, on_delete=models.CASCADE)
    codTf = models.ForeignKey(TipoFardo, on_delete=models.CASCADE)
    exiStF = models.BooleanField()

    def __str__(self):
        return str(self.codFar)

    

class Tela(models.Model):
    codTela = models.AutoField(primary_key=True)
    codCla = models.ForeignKey(Clasificadores, on_delete=models.CASCADE)
    codCp = models.ForeignKey(ColorPrincipal, on_delete=models.CASCADE)
    codCs = models.ForeignKey(ColorSecundario, on_delete=models.CASCADE)
    codTt = models.ForeignKey(TipoTela, on_delete=models.CASCADE)
    codPt = models.ForeignKey(Patron, on_delete=models.CASCADE)
    exiSt = models.BooleanField()

    def __str__(self):
        return str(self.codTela)

class RegBodegaMuestra(models.Model):
    codRegM = models.AutoField(primary_key=True)
    codMovM = models.ForeignKey(TipoMovimientoM, on_delete=models.CASCADE)
    codTela = models.ForeignKey(Tela, on_delete=models.CASCADE)
    codUbi = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    fechaIngM = models.DateField()
    cantidad = models.IntegerField()
    codBode = models.ForeignKey(Bodeguero, on_delete=models.CASCADE)


class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    codUser = models.CharField(max_length=100, unique=True)
    codTra = models.ForeignKey(Trabajadores, on_delete=models.CASCADE)
    codPer = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    passW = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = "codUser"
    PASSWORD_FIELD = "passW"


class Artesano(models.Model):
    codArt = models.AutoField(primary_key=True)
    codBod = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    codTra = models.ForeignKey(Trabajadores, on_delete=models.CASCADE)

class RegBodegaFar(models.Model):
    codRegF = models.AutoField(primary_key=True)
    codUbi=models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    codFar = models.ForeignKey(Fardos, on_delete=models.CASCADE)
    codMovF = models.ForeignKey(TipoMovFardo, on_delete=models.CASCADE)
    fechaIngFar = models.DateField()
    cantidad=models.IntegerField()
    codBode = models.ForeignKey(Bodeguero, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.codRegF),self.cantidad