# forms.py
from django import forms
from .models import Reserva, Chofer

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            'fecha', 'horario', 'chofer', 'calificacion', 'resena', 'respuesta'
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.Select(choices=[(f"{hour}:00", f"{hour}:00") for hour in range(7, 20)]),  # Horas de 7:00 a 19:00
        }

    # Asegúrate de usar 'chofer' como campo de tipo ModelChoiceField para seleccionar choferes
    chofer = forms.ModelChoiceField(
        queryset=Chofer.objects.all(),
        empty_label="Seleccione un Chofer",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        # Recoger el horario seleccionado del formulario si está disponible
        horario_seleccionado = kwargs.get('initial', {}).get('horario', None)
        
        # Llamamos al método __init__ de la clase base
        super().__init__(*args, **kwargs)

        # Si hay un horario seleccionado, filtramos los choferes por el horario
        if horario_seleccionado:
            self.fields['chofer'].queryset = Chofer.objects.filter(
                horario1__lte=horario_seleccionado,
                horario2__gte=horario_seleccionado
            )
