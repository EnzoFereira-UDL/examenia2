# Contenido COMPLETO para: load/load_ventana_principal.py
from PyQt5 import QtWidgets,uic

# --- Importamos las clases de las VENTANAS ---
from .load_ventana_modelos_basicos import Load_ventana_modelos_basicos
from .load_ventana_modelos_langChain import LoadVentanaLangChain

# --- Importamos los "MOTORES BÁSICOS" ---
from main import crear_modelo_simple
from main_historial import crear_modelo_historial
from main_memoria import crear_modelo_chat_limitado

#
# --- <<< CAMBIO 1: Importamos SÓLO EL MOTOR 1 de LangChain >>> ---
#
from lc_1_llmchain import crear_chain_llmchain # (Asumiendo que el archivo se llama así)


class Load_ventana_principal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interfaces/ventana_principal.ui",self)
        self.showMaximized()

        print("Cargando modelos... (Esto puede tardar un momento)")
        
        # --- Cargamos los 3 motores BÁSICOS ---
        self.modelo_simple_cargado = crear_modelo_simple()
        self.modelo_historial_cargado = crear_modelo_historial()
        self.modelo_chat_cargado = crear_modelo_chat_limitado()
        
        #
        # --- <<< CAMBIO 2: Cargamos SÓLO EL MOTOR 1 de LangChain >>> ---
        #
        self.lc_chain_1 = crear_chain_llmchain()
        # (Los otros 7 motores aún no existen, no los cargamos)
        
        print("¡Modelos cargados y listos!")


        # Conectamos las acciones del menú
        self.actionBasicos.triggered.connect(self.abrirVentanaBasico)
        self.actionLangChain.triggered.connect(self.abrirVentanaLangchain)
        self.actionSalir.triggered.connect(self.cerrarVentana)
    
    def abrirVentanaBasico(self):
        # Esto ya está 100% funcional
        self.basicos = Load_ventana_modelos_basicos(
            modelo_simple=self.modelo_simple_cargado,
            modelo_memoria=self.modelo_historial_cargado,
            modelo_chat=self.modelo_chat_cargado
        )
        self.basicos.exec_()
    
    
    def abrirVentanaLangchain(self):
        #
        # --- <<< CAMBIO 3: Pasamos el motor 1 y "None" para los demás >>> ---
        #
        self.LangChain = LoadVentanaLangChain(
            chain_1=self.lc_chain_1, # ¡El único que tenemos!
            chain_2=None,
            chain_3=None,
            chain_4=None,
            chain_5=None,
            chain_6=None,
            chain_7=None,
            chain_8=None
        )
        self.LangChain.exec_()

    def cerrarVentana(self):
        self.close()