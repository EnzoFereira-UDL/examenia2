from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QPropertyAnimation

class Load_ventana_cuestionario(QtWidgets.QDialog):
    # -------------------------------------------------------------------------
    # CORRECCIÓN: Ajustamos los parámetros para aceptar 'modelo_cuestionario'
    # -------------------------------------------------------------------------
    def __init__(self, parent=None, modelo_cuestionario=None):
        super(Load_ventana_cuestionario, self).__init__(parent)
        
        # Cargar la interfaz .ui directamente
        # Asegúrate de que esta ruta sea correcta relativa al main.py
        try:
            uic.loadUi("interfaces/ventana_cuestionario.ui", self)
        except FileNotFoundError:
            print("ERROR: No se encontró 'interfaces/ventana_cuestionario.ui'")
        
        # Asignamos el modelo recibido a la variable que usas en el resto de la clase
        self.modelo = modelo_cuestionario
        
        self.pdf_path = None
        self.estado_cuestionario = "inicio" # inicio | preguntas_listas


        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.boton_cerrar.clicked.connect(lambda: self.close())
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        self.boton_menu.clicked.connect(self.mover_menu)

        # --- Conexiones (Asegúrate que estos botones existen en tu .ui) ---
        # Es buena práctica usar try/except aquí por si cambiaste nombres en Qt Designer
        try:
            self.boton_pdf.clicked.connect(self.seleccionar_pdf)
            self.boton_enviar.clicked.connect(self.gestionar_flujo)
            
            # Estado inicial UI
            self.output_response.setPlaceholderText("Aquí aparecerán las preguntas...")
            self.respuestas.setPlaceholderText("Selecciona un PDF primero")
            self.respuestas.setEnabled(False)
        except AttributeError as e:
            print(f"Error de UI: {e}. Verifica los nombres de los objetos en Qt Designer.")

    def seleccionar_pdf(self):
        opciones = QtWidgets.QFileDialog.Options()
        archivo, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Seleccionar PDF", "", "Archivos PDF (*.pdf);;Todos los archivos (*)", options=opciones
        )
        
        if archivo:
            self.pdf_path = archivo
            nombre_archivo = archivo.split("/")[-1]
            self.boton_pdf.setText(f"PDF: {nombre_archivo}")
            self.output_response.setText(f"PDF Cargado: {nombre_archivo}\nPresiona 'Generar Cuestionario' para comenzar.")
            
            # Reiniciar estado
            self.estado_cuestionario = "inicio"
            self.boton_enviar.setText("Generar Cuestionario")
            self.respuestas.clear()
            self.respuestas.setEnabled(False)

    def gestionar_flujo(self):
        if self.estado_cuestionario == "inicio":
            self.generar_preguntas()
        else:
            self.calificar_respuestas()

    def generar_preguntas(self):
        if not self.pdf_path:
            self.output_response.setText("Por favor selecciona un PDF primero.")
            return

        self.output_response.setText("Leyendo PDF y generando preguntas con IA... (Esto puede tardar unos segundos)")
        self.boton_enviar.setEnabled(False)
        QtWidgets.QApplication.processEvents() # Forzar actualización de UI

        # Validación de seguridad por si el modelo no llegó
        if not self.modelo:
            self.output_response.setText("Error CRÍTICO: El modelo de IA no se cargó correctamente.")
            self.boton_enviar.setEnabled(True)
            return

        # Llamada al modelo
        exito, resultado = self.modelo.procesar_pdf_y_generar_preguntas(self.pdf_path)

        self.boton_enviar.setEnabled(True)

        if exito:
            self.output_response.setText(resultado)
            self.output_response.append("\n\nEscribe tus respuestas abajo separadas por comas (Ej: A, B, C, D, A)")
            
            # Cambiar estado a modo respuesta
            self.estado_cuestionario = "preguntas_listas"
            self.boton_enviar.setText("Calificar Respuestas")
            self.respuestas.setEnabled(True)
            self.respuestas.setFocus()
        else:
            self.output_response.setText(f"Error: {resultado}")

    def calificar_respuestas(self):
        texto_usuario = self.respuestas.text().strip()
        
        if not texto_usuario:
            self.output_response.append("\nPor favor escribe tus respuestas.")
            return

        # Llamada al modelo para evaluar
        resultado_evaluacion = self.modelo.evaluar_respuestas(texto_usuario)
        
        # Mostrar resultado
        self.output_response.append("\n" + "="*30 + "\n")
        self.output_response.append(resultado_evaluacion)
        
        # Finalizar ciclo
        self.boton_enviar.setText("Intentar de nuevo (Reseleccionar PDF)")
        self.estado_cuestionario = "finalizado"
        
        # Desconectar para evitar bucles raros y conectar el reset
        try: 
            self.boton_enviar.clicked.disconnect()
        except: 
            pass
        self.boton_enviar.clicked.connect(self.reset_interfaz)

    def reset_interfaz(self):
        self.output_response.clear()
        self.respuestas.clear()
        self.respuestas.setEnabled(False)
        self.boton_enviar.setText("Generar Cuestionario")
        self.estado_cuestionario = "inicio"
        self.pdf_path = None
        self.boton_pdf.setText("Seleccionar PDF") # Resetear texto del botón PDF
        
        # Reconectar lógica normal
        try:
            self.boton_enviar.clicked.disconnect()
        except:
            pass
        self.boton_enviar.clicked.connect(self.gestionar_flujo)
        self.output_response.setText("Listo para empezar de nuevo. Selecciona PDF o Generar.")

    # --- Lógica de ventana (Mover, etc) ---
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
        
    def mover_ventana(self, event):
        if self.isMaximized() == False:     
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        # (Tu lógica de maximizar/minimizar al arrastrar arriba)
        # (NOTA: Esta lógica a veces es conflictiva, pero la dejo)
        # if event.globalPos().y() <=20:
        #     self.showMaximized()
        # else:
        #     self.showNormal()
    
    # --- Tu código original para MOVER MENÚ ---
    # (¡Un poco simplificado para que use los anchos correctos!)
    def mover_menu(self):
        width = self.frame_lateral.width()
        
        if width == 0:
            # Si está oculto (ancho 0), lo extendemos a 200
            extender = 200
            self.boton_menu.setText("Menú")
        else:
            # Si está visible (ancho 200), lo ocultamos (ancho 0)
            extender = 0
            self.boton_menu.setText("") # (Tu lógica de borrar texto)
            
        # Animación para el frame lateral
        self.animacion = QtCore.QPropertyAnimation(self.frame_lateral, b'minimumWidth')
        self.animacion.setDuration(300)
        self.animacion.setStartValue(width)
        self.animacion.setEndValue(extender)
        self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animacion.start()
        
        # Animación para el botón (si también quieres animarlo)
        # (Nota: Animar el botón puede ser raro, quizás quieras quitar esto)
        self.animacionb = QPropertyAnimation(self.boton_menu, b'minimumWidth')
        self.animacionb.setDuration(300)
        self.animacionb.setStartValue(width) # (Debería ser el ancho del botón, no del frame)
        self.animacionb.setEndValue(extender)
        self.animacionb.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animacionb.start()