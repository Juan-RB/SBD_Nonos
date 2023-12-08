from django import forms
from SBDcrud.models import *
from django.core.validators import MaxLengthValidator

from datetime import datetime



# este es el formulario del login
class UsuarioLogin(forms.Form):
    codUser = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    passW = forms.CharField(
        label="Contraseña", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


# este es el formulario de ingreso de muestras
class FormMuestra(forms.ModelForm):
    class Meta:
        model = Tela
        fields = ['codCla', 'codCp', 'codCs', 'codTt', 'codPt', 'exiSt']


    codCla = forms.ModelChoiceField(
        queryset=Clasificadores.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Codigo del Clasificador',

    )

    codCp = forms.ModelChoiceField(
        queryset=ColorPrincipal.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control barra'}),
        label='Color principal',
        empty_label='Selecciona un color principal'

    )
    codCs = forms.ModelChoiceField(
        queryset=ColorSecundario.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Color secundario',
        empty_label='Selecciona un color secundario si existe'

    )

    codTt = forms.ModelChoiceField(
        queryset=TipoTela.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo de tela',
        empty_label='Selecciona un tipo de tela'

    )

    codPt = forms.ModelChoiceField(
        queryset=Patron.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo de Patrón',
        empty_label='Selecciona un tipo de patrón o dibujo'

    )

    exiSt = forms.BooleanField(
    initial=True,
    required=False,
    widget=forms.HiddenInput(attrs={'value': True}),
    label='',
)


# formulario de creacion de bodega fisicia (NO BORRAR)


class FormBodega(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = ["nomBod", "dirBod", "cantPas", "codCom", "status"]

    nomBod = forms.CharField(
        label="Nombre de la bodega",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            MaxLengthValidator(limit_value=30)
        ],  # Agrega el validador de longitud máxima
    )

    dirBod = forms.CharField(
        label="Dirección de la bodega",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            MaxLengthValidator(limit_value=30)
        ],  # Agrega el validador de longitud máxima
    )

    cantPas = forms.IntegerField(
        label="Cantidad de pasillos",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    codCom = forms.ModelChoiceField(
        queryset=Comuna.objects.all(),
        empty_label="Seleccione una comuna",
        label="Código de Comuna",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    STATUS_CHOICES = (
        (True, "Activo"),
        (False, "Inactivo"),
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Estatus",
    )


class DesactivarBodegaForm(forms.Form):
    bodega = forms.ModelChoiceField(
        queryset=Bodega.objects.filter(status=True),
        empty_label="Seleccione una bodega a desactivar",
        label="Bodega a Desactivar",
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class ModificarBodegaForm(forms.Form):
    bodega = forms.ModelChoiceField(
        queryset=Bodega.objects.filter(status=True),
        empty_label="Seleccione una bodega a modificar",
        label="Bodega a Modificar",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    nomBod = forms.CharField(
        label="Nombre de la bodega",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )

    dirBod = forms.CharField(
        label="Dirección de la bodega",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )

class FormbusquedaCp(forms.ModelForm):
    class Meta:
        model =Tela
        fields =['codCp']

    codCp = forms.ModelChoiceField(
        queryset=ColorPrincipal.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Color principal',
        empty_label='Selecciona un color principal'
    )

class FormbusquedaCs(forms.ModelForm):
    class Meta:
        model =Tela
        fields =['codCs']

    codCs = forms.ModelChoiceField(
        queryset=ColorSecundario.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Color secundario',
        empty_label='Selecciona un color secundario'
    )


class FormbusquedaPt(forms.ModelForm):
    class Meta:
        model =Tela
        fields =['codPt']

    codPt = forms.ModelChoiceField(
        queryset=Patron.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Patron',
        empty_label='Selecciona un patrón'
    )

class FormbusquedaTt(forms.ModelForm):
    class Meta:
        model =Tela
        fields =['codTt']

    codTt = forms.ModelChoiceField(
        queryset=TipoTela.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo de tela',
        empty_label='Selecciona un tipo de tela'
    )

class FormbusquedaTela(forms.ModelForm):
    class Meta:
        model =Tela
        fields =['codTela']

    codTela = forms.ModelChoiceField(
        queryset=Tela.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}, choices=Tela.objects.all().values_list('codTela', 'codTela')),
        label='Codigo tela',
        empty_label='Selecciona un codigo de tela'
    )

class FormbusquedaCla(forms.ModelForm):
    class Meta:
        model =Tela
        fields =['codCla']

    codCla = forms.ModelChoiceField(
        queryset=Clasificadores.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Clasificador',
        empty_label='Selecciona un clasificador'
    )


class Formfardo(forms.ModelForm):
    class Meta:
        model = Fardos
        fields = ['codRec', 'codTf']

    codRec = forms.ModelChoiceField(
        queryset=Recolectores.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Recolector',
        empty_label='Selecciona un recolector'
    )

    codTf = forms.ModelChoiceField(
        queryset=TipoFardo.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo de Fardo',
        empty_label='Selecciona un tipo de fardo'
    )

    exiStF = forms.BooleanField(
    initial=True,
    required=False,
    widget=forms.HiddenInput(attrs={'value': True}),
    label='',
)


class formBusquedaTipoFardo(forms.ModelForm):
    class Meta:
        model = Fardos
        fields = ['codTf','exiStF']


    codTf = forms.ModelChoiceField(
    queryset=TipoFardo.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control'}),
    label='Tipo de fardo',
    empty_label='Selecciona el tipo de fardo que deseas encontrar')

    exiStF = forms.ChoiceField(
        choices=[('', 'Seleccione el status')] + [(True, 'En proceso'), (False, 'Procesado')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )



class formPasillos(forms.ModelForm):
    class Meta:
        model=Ubicacion
        fields = ["codBod"]


    codBod = forms.ModelChoiceField(
    queryset=Bodega.objects.all(),
    widget=forms.Select(attrs={'class':'form-control'}),
    label='Bodega',
    empty_label=('elige la bodega que quieres modificar'))



    
class FormAgregarColorP(forms.ModelForm):
    class Meta:
        model = ColorPrincipal
        fields = ['nomCp']

    nomCp = forms.CharField(
        label="Ingrese el nuevo color primario",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            MaxLengthValidator(limit_value=30)
        ],  # Agrega el validador de longitud máxima
    )

class FormAgregarColorS(forms.ModelForm):
    class Meta:
        model = ColorSecundario
        fields = ['nomCs']

    nomCs = forms.CharField(
        label="Ingrese el nuevo color secundario",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            MaxLengthValidator(limit_value=30)
        ],  # Agrega el validador de longitud máxima
    )

class FormAgregarPatronesT(forms.ModelForm):
    class Meta:
        model = Patron
        fields = ['nomPt']

    nomPt = forms.CharField(
        label="Ingrese el nuevo Patrón",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            MaxLengthValidator(limit_value=30)
        ],  # Agrega el validador de longitud máxima
    )

class FormAgregartiposT(forms.ModelForm):
    class Meta:
        model = TipoTela
        fields = ['nomTt']

    nomTt = forms.CharField(
        label="Ingrese el nuevo tipo de tela",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            MaxLengthValidator(limit_value=30)
        ],  # Agrega el validador de longitud máxima
    )

class FormAgregarTrabajadores(forms.ModelForm):
    class Meta:
        model = Trabajadores
        fields = ('rutTra','nomTra','dirTra','telTra','emailTra','codCom')
        
    rutTra = forms.IntegerField(
        label="Rut del trabajardor",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    nomTra = forms.CharField(
        label="Ingrese el nombre del trabajador",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            MaxLengthValidator(limit_value=30)
        ], 
    )
    dirTra = forms.CharField(
        label="Ingrese la dirección del trabajador",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            MaxLengthValidator(limit_value=30)
        ], 
    )
    telTra = forms.CharField(
        label="Ingrese telefono del trabajador",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            MaxLengthValidator(limit_value=30)
        ], 
    )
    emailTra = forms.CharField(
        label="Ingrese email del trabajador",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            MaxLengthValidator(limit_value=30)
        ], 
    )
    codCom = forms.ModelChoiceField(
        queryset=Comuna.objects.all(),
        empty_label="Seleccione una comuna",
        label="Código de Comuna",
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class RegBodegaMuestraForm(forms.ModelForm):
    class Meta:
        model = RegBodegaMuestra
        fields = ["codMovM", "codTela", "codUbi", "cantidad"]
        widgets = {
            "codMovM": forms.Select(attrs={"class": "form-control"}),
            "codTela": forms.Select(attrs={"class": "form-control"}),
            "codUbi": forms.Select(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "style": "display: none;"}),

        }

        labels = {
            "codMovM": "Seleccione el movimiento que realizará ",
            "codTela": "Seleccione la tela ",
            "cantidad": "",
            "codUbi": "Seleccione la ubicación",
        }

class RegBodegaFardoForm(forms.ModelForm):

    class Meta:
        model = RegBodegaFar
        fields = ["codUbi", "codFar", "codMovF", "cantidad"]
        widgets = {
            "codUbi": forms.Select(attrs={"class": "form-control"}),
            "codFar": forms.Select(attrs={"class": "form-control"}),
            "codMovF": forms.Select(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "style": "display: none;"}),



        }

        labels = {
            "codUbi": "Seleccione la ubicación",
            "codFar": "Seleccione el fardo ",
            "codMovF": "Seleccione el movimiento que realizará ",
            "cantidad": "",

        }


class formMovFar(forms.ModelForm):
        MES_CHOICES = [
        (1, 'Enero'),(2, 'Febrero'),(3, 'Marzo'),(4, 'Abril'),(5, 'Mayo'),(6,'Junio'),
        (7, 'Julio'),(8, 'Agosto'),(9, 'Septiembre'),(10, 'Octubre'),(11, 'Noviembre'),(12, 'Diciembre')]

        YEARS_CHOICES = [ (2022,"2022"),(2023,"2023"),(2024,"2024")]



        mes = forms.ChoiceField(
            choices=MES_CHOICES,
            widget=forms.Select(attrs={'class': 'form-control'},),
            label='Mes')
        

        
        years = forms.ChoiceField(
            choices=YEARS_CHOICES,
            widget=forms.Select(attrs={'class': 'form-control'},),
            label='Mes')

                

        class Meta:
            model=RegBodegaFar
            fields = ['codUbi','codMovF','fechaIngFar','codBode']
        
        codUbi = forms.ModelChoiceField(
        queryset=Ubicacion.objects.all(),  # Debes usar Ubicacion, no RegBodegaFar
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Ubicación ',
        empty_label=('Elige la ubicación')
    )

        codMovF = forms.ModelChoiceField(
        queryset=TipoMovFardo.objects.all(),  # Debes usar TipoMovFardo, no RegBodegaFar
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Movimiento ',
        empty_label=('Elige el tipo de movimiento')
    )
        
        codBode = forms.ModelChoiceField(
        queryset=Trabajadores.objects.all(),  # Debes usar TipoMovFardo, no RegBodegaFar
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='codBode',
        label='Colaborador ',
        empty_label=('Elige el colaborador')
        
    )

        fechaIngFar = forms.ModelChoiceField(
        queryset=RegBodegaFar.objects.all(),
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha',
        empty_label=('elige la fecha exacta'))

class formMovMuestra(forms.ModelForm):
        MES_CHOICES = [
            (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'),
            (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
        ]

        YEARS_CHOICES = [(2022, "2022"), (2023, "2023"), (2024, "2024")]

        mes = forms.ChoiceField(
            choices=MES_CHOICES,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Mes'
        )

        years = forms.ChoiceField(
            choices=YEARS_CHOICES,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Año'
        )

        class Meta:
            model = RegBodegaMuestra
            fields = ['codUbi', 'codMovM', 'codBode']

        codUbi = forms.ModelChoiceField(
            queryset=Ubicacion.objects.all(),
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Ubicación',
            empty_label='Elige la ubicación'
        )

        codMovM = forms.ModelChoiceField(
            queryset=TipoMovimientoM.objects.all(),
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Movimiento',
            empty_label='Elige el tipo de movimiento'
        )

        codBode = forms.ModelChoiceField(
            queryset=Trabajadores.objects.all(),
            widget=forms.Select(attrs={'class': 'form-control'}),
            to_field_name='codBode',
            label='Colaborador',
            empty_label='Elige el colaborador'
        )

        fechaIngM = forms.ModelChoiceField(
            queryset=RegBodegaFar.objects.all(),
            widget=forms.DateInput(attrs={'type': 'date'}),
            label='Fecha',
            empty_label=('elige la fecha exacta'))


class FormModificarTrabajadores(forms.ModelForm):
    class Meta:
        model = Trabajadores
        fields= ['codTra','dirTra','telTra','emailTra','codCom']

    codTra = forms.ModelChoiceField(
        queryset=Trabajadores.objects.all(),
        empty_label="Seleccione un trabajador a modificar",
        label="Trabajador a Modificar",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    dirTra = forms.CharField(
        label="Ingrese la dirección del trabajador",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            MaxLengthValidator(limit_value=30)
        ], 

    )
    telTra = forms.CharField(
        label="Ingrese telefono del trabajador",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            MaxLengthValidator(limit_value=30)
        ], 
    )
    emailTra = forms.CharField(
        label="Ingrese email del trabajador",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            MaxLengthValidator(limit_value=30)
        ], 
    )
    codCom = forms.ModelChoiceField(
        queryset=Comuna.objects.all(),
        empty_label="Seleccione una comuna",
        label="Comuna",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

class FormAsignarUsuarios(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['codUser', 'passW', 'codPer', 'codTra']

    codUser = forms.CharField(
        label="Rut / Usuario",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    passW = forms.CharField(
        label="Ingrese una contraseña",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[MaxLengthValidator(limit_value=30)],
    )
    codPer = forms.ModelChoiceField(
        queryset=Perfil.objects.all(),
        empty_label="Seleccione un perfil",
        label="Perfil",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    codTra = forms.ModelChoiceField(
        queryset=Trabajadores.objects.all(),
        empty_label="Seleccione un trabajador",
        label="Trabajador",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

# forms.py

class FormAsignarFuncion(forms.ModelForm):
    class Meta:
        model = Bodeguero  # Puedes usar cualquier modelo ya que solo estamos inicializando el formulario
        fields = ['codBod', 'codTra','tipo_funcion']

    tipo_funcion = forms.ChoiceField(choices=[('bodeguero', 'Bodeguero'), ('artesano', 'Artesano'), ('recolector', 'Recolector'), ('clasificador', 'Clasificador')],
                                    widget=forms.Select(attrs={'class': 'form-control'}),
                                    label='Tipo de Función')

    codBod = forms.ModelChoiceField(
        queryset=Bodega.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Elegir Bodega',
        empty_label=('Seleccionar Bodega'))

    codTra = forms.ModelChoiceField(
        queryset=Trabajadores.objects.all(),
        empty_label="Seleccione un trabajador a modificar",
        label="Trabajador a Modificar",
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class FiltrosMovimientosForm(forms.Form):
    codigo_movimiento_far = forms.ModelChoiceField(
        queryset=TipoMovFardo.objects.all(),
        empty_label="Seleccione un tipo de movimiento para RegBodegaFar",
        label="Tipo de Movimiento para RegBodegaFar",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    codigo_movimiento_muestra = forms.ModelChoiceField(
        queryset=TipoMovimientoM.objects.all(),
        empty_label="Seleccione un tipo de movimiento para RegBodegaMuestra",
        label="Tipo de Movimiento para RegBodegaMuestra",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    cod_bodeguero_far = forms.ModelChoiceField(
        queryset=Bodeguero.objects.all(),
        empty_label="Seleccione un bodeguero ",
        label="Bodeguero Fardos",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    cod_bodeguero_muestra = forms.ModelChoiceField(
        queryset=Bodeguero.objects.all(),
        empty_label="Seleccione un bodeguero ",
        label="Bodeguero Muestras",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

