from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from plyer import notification
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
import time
from kivy.core.window import Window

# Configurar tamaño de ventana
Window.size = (400, 600)

class ConfiguracionPopup(Popup):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.title = "Configuración de Alarma"
        self.size_hint = (0.8, 0.8)
        self.parent_widget = parent
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Selector de tono de alarma
        layout.add_widget(Label(text="Seleccionar tono de alarma:"))
        self.tono_spinner = Spinner(
            text='Tono 1',
            values=('Tono 1', 'Tono 2', 'Tono 3'),
            size_hint=(1, 0.3)
        )
        layout.add_widget(self.tono_spinner)

        # Mensaje personalizado al terminar
        layout.add_widget(Label(text="Mensaje personalizado:"))
        self.mensaje_personalizado = TextInput(hint_text="Ingresa un mensaje", multiline=False)
        layout.add_widget(self.mensaje_personalizado)

        # Slider para volumen
        layout.add_widget(Label(text="Volumen de la alarma:"))
        self.volumen_slider = Slider(min=0, max=1, value=0.5)
        layout.add_widget(self.volumen_slider)

        # Botón para cerrar y guardar configuración
        guardar_btn = Button(text="Guardar Configuración", size_hint=(1, 0.3))
        guardar_btn.bind(on_press=self.guardar_configuracion)
        layout.add_widget(guardar_btn)

        self.add_widget(layout)

    def guardar_configuracion(self, instance):
        self.parent_widget.configuracion['tono'] = self.tono_spinner.text
        self.parent_widget.configuracion['mensaje'] = self.mensaje_personalizado.text or "¡Tiempo terminado!"
        self.parent_widget.configuracion['volumen'] = self.volumen_slider.value
        self.dismiss()

class AlarmaTareas(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Layout para sobreponer el contenido sobre la imagen
        self.contenedor = BoxLayout(orientation='vertical', spacing=20, padding=[10], size_hint=(1, 0.9))
        self.add_widget(self.contenedor)

        # Estilo de la etiqueta del reloj
        self.reloj_cteisa = Label(text="00:00:00", font_size=64, color=(1, 0.8, 0, 1), bold=True)
        self.contenedor.add_widget(self.reloj_cteisa)

        # Entrada de texto para tiempo de la tarea (en minutos)
        self.entrada_tiempo = TextInput(hint_text="Ingresa tiempo en minutos", font_size=10, multiline=False,
                                        input_filter='float', size_hint=(1, 0.2))
        self.contenedor.add_widget(self.entrada_tiempo)

        # Botón de iniciar
        self.boton_iniciar = Button(text="Iniciar Alarma", background_color=(0.2, 0.6, 1, 1), font_size=20, size_hint=(1, 0.2))
        self.boton_iniciar.bind(on_press=self.iniciar_alarma)
        self.contenedor.add_widget(self.boton_iniciar)

        # Botón de detener
        self.boton_detener = Button(text="Detener Alarma", background_color=(1, 0.2, 0.2, 1), font_size=20, size_hint=(1, 0.2))
        self.boton_detener.bind(on_press=self.detener_alarma)
        self.contenedor.add_widget(self.boton_detener)

        # Botón de configuración
        self.boton_configuracion = Button(text="Configuración", background_color=(0.2, 0.8, 0.2, 1), font_size=20, size_hint=(1, 0.2))
        self.boton_configuracion.bind(on_press=self.mostrar_configuracion)
        self.contenedor.add_widget(self.boton_configuracion)

        # Variables de control
        self.tiempo_final = None
        self.corriendo = False

        # Diccionario para almacenar las configuraciones
        self.configuracion = {
            'tono': 'Tono 1',
            'mensaje': '¡Tiempo terminado!',
            'volumen': 0.5
        }

        Clock.schedule_interval(self.actualizar, 1)

    def iniciar_alarma(self, instance):
        if not self.corriendo:
            try:
                minutos = float(self.entrada_tiempo.text)  # Obtener el tiempo en minutos
                self.tiempo_final = time.time() + (minutos * 60)  # Convertir minutos a segundos
                self.corriendo = True
                notification.notify(title="Alarma de Tareas", message="Alarma iniciada")
            except ValueError:
                self.reloj_cteisa.text = "Ingrese un tiempo"
    
    def detener_alarma(self, instance):
        if self.corriendo:
            self.corriendo = False
            self.reloj_cteisa.text = "00:00:00"
            notification.notify(title="Alarma de Tareas", message="Alarma detenida")
    
    def actualizar(self, dt):
        if self.corriendo:
            tiempo_restante = self.tiempo_final - time.time()

            if tiempo_restante > 0:
                minutos, segundos = divmod(tiempo_restante, 60)
                self.reloj_cteisa.text = f"{int(minutos):02}:{int(segundos):02}"
            else:
                self.reloj_cteisa.text = "00:00:00"
                notification.notify(title="Alarma de Tareas", message=self.configuracion['mensaje'])
                self.corriendo = False

    def mostrar_configuracion(self, instance):
        popup = ConfiguracionPopup(self)
        popup.open()

class MiApp(App):
    def build(self):
        return AlarmaTareas()

if __name__ == "__main__":
    MiApp().run()
