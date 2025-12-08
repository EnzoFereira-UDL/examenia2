# Contenido COMPLETO para: load/load_ventana_principal.py
from PyQt5 import QtWidgets,uic

# --- Importamos las clases de las VENTANAS ---
from .load_ventana_modelos_basicos import Load_ventana_modelos_basicos
from .load_ventana_modelos_langChain import LoadVentanaLangChain
from .load_ventana_modelos_cuestionario import Load_ventana_cuestionario

# --- Importamos los "MOTORES BÁSICOS" ---
from main import crear_modelo_simple
from main_historial import crear_modelo_historial
from main_memoria import crear_modelo_chat_limitado

#
# --- <<< CAMBIO 1: Importamos SÓLO EL MOTOR 1 de LangChain >>> ---
#
from lc_1_llmchain import crear_chain_llmchain
from lc_2_sequientialchain import crear_chain_sequential # (Asumiendo que el archivo se llama así)
from lc_3_simplesequientialchain import crear_chain_simple
from lc_4_parseo import crear_chain_parseo
from lc_5_varios_pasos import crear_chain_varios_pasos
from lc_6_memoria import crear_chain_memoria
from lc_7_persistencia import crear_chain_persistencia
from lc_8_rag import crear_chain_rag

from cuestionario import crear_chain_rag2


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
        self.lc_chain_2 = crear_chain_sequential()
        self.lc_chain_3 = crear_chain_simple()
        self.lc_chain_4 = crear_chain_parseo()
        self.lc_chain_5 = crear_chain_varios_pasos()
        self.lc_chain_6 = crear_chain_memoria()
        self.lc_chain_7 = crear_chain_persistencia()
        self.lc_chain_8 = crear_chain_rag()


        self.cuestionario = crear_chain_rag2()
        # (Los otros 7 motores aún no existen, no los cargamos)
        
        print("¡Modelos cargados y listos!")


        # Conectamos las acciones del menú
        self.actionBasicos.triggered.connect(self.abrirVentanaBasico)
        self.actionLangChain.triggered.connect(self.abrirVentanaLangchain)
        self.actionCuestionarioIA.triggered.connect(self.abrirVentanaCuestionario)
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
            chain_1=self.lc_chain_1,
            chain_2=self.lc_chain_2,
            chain_3=self.lc_chain_3,
            chain_4=self.lc_chain_4,
            chain_5=self.lc_chain_5,
            chain_6=self.lc_chain_6,
            chain_7=self.lc_chain_7,
            chain_8=self.lc_chain_8
        )
        self.LangChain.exec_()

    def abrirVentanaCuestionario(self):
        # Instanciamos la ventana dedicada pasando el modelo
        self.ventana_cuestionario = Load_ventana_cuestionario(
            modelo_cuestionario=self.cuestionario
        )
        self.ventana_cuestionario.exec_()

    def cerrarVentana(self):
        self.close()