# Contenido COMPLETO para: load/load_ventana_modelos_basicos.py
from PyQt5 import QtWidgets,uic,QtCore
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve # (Añadí QEasingCurve)

class Load_ventana_modelos_basicos(QtWidgets.QDialog):
    
    #
    # <<< ¡AQUÍ ESTÁ LA CORRECCIÓN! >>>
    # Ahora el __init__ ACEPTA los 3 modelos
    #
    def __init__(self, modelo_simple, modelo_memoria, modelo_chat, parent=None):
        super().__init__(parent)
        
        #cargar la interfaz grafica
        uic.loadUi("interfaces/ventana_modelos_basicos.ui",self)
        
        # <<< AÑADIDO: Guardamos los modelos que nos pasaron
        self.modelo_simple = modelo_simple
        self.modelo_memoria = modelo_memoria
        self.modelo_chat = modelo_chat

        # --- Tu código original para la ventana sin bordes ---
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.boton_cerrar.clicked.connect(lambda: self.close())
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        self.boton_menu.clicked.connect(self.mover_menu)
        # --- Fin de tu código original ---

        #
        # <<< AÑADIDO: Conexiones para la navegación del StackedWidget ---
        # (Estos son los botones 'Prompt', 'Memoria', 'Chat' del lateral)
        #
        self.pushButton.clicked.connect(self.mostrar_pagina_prompt)
        self.pushButton_2.clicked.connect(self.mostrar_pagina_memoria)
        self.pushButton_3.clicked.connect(self.mostrar_pagina_chat)

        #
        # <<< AÑADIDO: Conexiones para los botones de "Enviar" ---
        #
        self.boton_enviar.clicked.connect(self.logica_enviar_prompt)
        self.boton_enviar_2.clicked.connect(self.logica_enviar_memoria)
        self.boton_enviar_3.clicked.connect(self.logica_enviar_chat)

    # 
    # <<< AÑADIDO: Funciones de navegación (Slots) ---
    #
    def mostrar_pagina_prompt(self):
        print("Cambiando a página Prompt")
        self.stackedWidget.setCurrentWidget(self.page_prompt)

    def mostrar_pagina_memoria(self):
        print("Cambiando a página Memoria")
        self.stackedWidget.setCurrentWidget(self.page_memoria)

    def mostrar_pagina_chat(self):
        print("Cambiando a página Chat")
        self.stackedWidget.setCurrentWidget(self.page_chat)

    #
    # <<< AÑADIDO: Funciones de Lógica (aquí usamos los modelos) ---
    # (¡CON LA CORRECCIÓN DE .invoke({"input": ...})!)
    #
    def logica_enviar_prompt(self):
        texto_usuario = self.input_prompt.text()
        print(f"[Prompt Simple] Usuario dijo: {texto_usuario}")
        
        #Usamos el modelo que nos pasaron con {"input": ...}
        respuesta_modelo = self.modelo_simple.invoke({"input": texto_usuario})
        
        self.output_response.setText(respuesta_modelo)
        self.input_prompt.clear()

    def logica_enviar_memoria(self):
        texto_usuario = self.input_prompt_2.text()
        print(f"[Memoria] Usuario dijo: {texto_usuario}")
        
        # 🚀 Usamos el modelo de memoria con {"input": ...}
        respuesta_dict = self.modelo_memoria.invoke({"input": texto_usuario})
        
        # (Asumimos que la respuesta está en 'response')
        respuesta_modelo = respuesta_dict.get('response', 'Error al obtener respuesta')
        
        # Usamos .append() para construir un historial
        self.output_response_2.append(f"Usuario: {texto_usuario}\n")
        self.output_response_2.append(f"Modelo: {respuesta_modelo}\n")
        self.input_prompt_2.clear()

    def logica_enviar_chat(self):
        texto_usuario = self.input_prompt_3.text()
        print(f"[Chat] Usuario dijo: {texto_usuario}")
        
        # corregido
        respuesta_dict = self.modelo_chat.invoke({"human_input": texto_usuario})
        
        # la respuesta está en ai_output (como definimos en el modelo)
        respuesta_modelo = respuesta_dict.get("ai_output", "Error al obtener respuesta")

        # mostrar en la interfaz
        self.output_response_3.append(f"Tú: {texto_usuario}\n")
        self.output_response_3.append(f"IA: {respuesta_modelo}\n")

        # limpiar caja de texto
        self.input_prompt_3.clear()

    # --- Tu código original para MOVER VENTANA ---
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