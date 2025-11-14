# Contenido COMPLETO para: load/load_ventana_modelos_LangChain.py
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

class LoadVentanaLangChain(QtWidgets.QDialog):
    
    def __init__(self, chain_1, chain_2, chain_3, chain_4, chain_5, chain_6, chain_7, chain_8, parent=None):
        
        super().__init__(parent)
        uic.loadUi("interfaces/ventana_modelos_LangChain.ui", self)
        
        self.chain_1 = chain_1
        self.chain_2 = chain_2
        self.chain_3 = chain_3
        self.chain_4 = chain_4
        self.chain_5 = chain_5
        self.chain_6 = chain_6
        self.chain_7 = chain_7
        self.chain_8 = chain_8
        
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.boton_salir.clicked.connect(self.close)
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        
        # Menú lateral
        self.boton_menu.clicked.connect(self.mover_menu)
        self.ancho_menu_visible = 200 # Ancho
        self.frame_lateral.setMaximumWidth(0) # Inicia oculto

        # Conexión Botónes (Nav)
        self.btn_llm.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_llm))
        self.btn_sequential.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_sequential))
        self.btn_simple.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_simple))
        self.btn_parseo.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_parseo))
        self.btn_variospasos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_variospasos))
        self.btn_memoria.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_memoria))
        self.btn_persistencia.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_persistencia))
        self.btn_memoria2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_memoria2))
        
        # Conexión Botónes (Enviar)
        self.btn_enviar_llm.clicked.connect(self.logica_enviar_lc_1)
        self.btn_enviar_sequential.clicked.connect(self.logica_enviar_lc_2)
        self.btn_enviar_simple.clicked.connect(self.logica_enviar_lc_3)
        self.btn_enviar_parseo.clicked.connect(self.logica_enviar_lc_4)
        self.btn_enviar_variospasos.clicked.connect(self.logica_enviar_lc_5)
        self.btn_enviar_memoria.clicked.connect(self.logica_enviar_lc_6)
        self.btn_enviar_persistencia.clicked.connect(self.logica_enviar_lc_7)
        self.btn_enviar_memoria2.clicked.connect(self.logica_enviar_lc_8)

    # Funcionalidad y llamada a modelos

    def logica_enviar_lc_1(self):
        # El único que funciona por ahora
        if not self.chain_1:
            self.output_llm.setText("Error: El motor 1 no fue cargado.")
            return
            
        texto_usuario = self.input_llm.text()
        if not texto_usuario:
            self.output_llm.setText("Por favor, escribe un tema.")
            return
            
        self.output_llm.setText("Procesando...")
        try:
            # Tu chain_1 espera la variable "tema"
            respuesta = self.chain_1.invoke({"tema": texto_usuario})
            self.output_llm.setText(respuesta.content) 
        except Exception as e:
            self.output_llm.setText(f"Error en LangChain: {e}")

    # --- Lógica para los 7 motores PENDIENTES ---
    # (Solo muestran un error amigable)

    def logica_enviar_lc_2(self):
        if not self.chain_2:
            self.output_sequential.setText("Motor 2 (SequentialChain) aún no ha sido implementado.9\n Proximamente...")
            return
        # Aquí iría la lógica del motor 2...
        
    def logica_enviar_lc_3(self):
        if not self.chain_3:
            self.output_simple.setText("Motor 3 (SimpleSequential) aún no ha sido implementado.9\n Proximamente...")
            return
        
    def logica_enviar_lc_4(self):
        if not self.chain_4:
            self.output_parseo.setText("Motor 4 (Parseo) aún no ha sido implementado.9\n Proximamente...")
            return

    def logica_enviar_lc_5(self):
        if not self.chain_5:
            self.output_variospasos.setText("Motor 5 (Varios Pasos) aún no ha sido implementado.9\n Proximamente...")
            return

    def logica_enviar_lc_6(self):
        if not self.chain_6:
            self.output_memoria.setText("Motor 6 (Memoria) no implementado.")
            return

    def logica_enviar_lc_7(self):
        if not self.chain_7:
            self.output_persistencia.setText("Motor 7 (Persistencia) no implementado.")
            return

    def logica_enviar_lc_8(self):
        if not self.chain_8:
            self.output_memoria2.setText("Motor 8 (RAG) no implementado.")
            return

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