```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title Cronograma de Implementación - GUEPARDEX

    section Planificación
    Actividad_1_Analisis        :a1, 2023-11-01, 5d
    Actividad_2_Diseno          :a2, after a1, 7d

    section Ejecución
    Actividad_3_Desarrollo      :crit, a3, after a2, 10d
    Actividad_4_Pruebas         :a4, after a3, 5d

    section Cierre
    Actividad_5_Capacitacion    :a5, after a4, 3d
    Entrega_Final               :milestone, after a5, 1d

