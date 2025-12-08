```mermaid
flowchart LR
    %% Nodos (Actividades)
    A([Inicio]) --> B[[Actividad 1]]
    B --> C[[Actividad 2]]
    C --> D[[Actividad 3]]
    C --> E[[Actividad 4]]
    D --> F[[Actividad 5]]
    E --> F
    F --> G([Fin del Proyecto])

    %% Estilos para resaltar la ruta crítica (opcional)
    style A fill:#c700c7,stroke:#222,stroke-width:2px
    style G fill:#c700c7,stroke:#222,stroke-width:2px
    style D fill:#b30000,stroke:#660000,stroke-width:2px
    style F fill:#b30000,stroke:#660000,stroke-width:2px


