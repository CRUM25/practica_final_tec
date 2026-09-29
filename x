flowchart TD
    subgraph R[1. Recolección]
        R1[Fuentes: Canales Auto / Manuales] --> R2[Validación de Calidad en Origen]
        R2 --> R3[Ingesta Centralizada<br>Cifrado + DLP + ISO 27001/27701]
    end

    subgraph A[2. Almacenamiento]
        A1[Landing Zone: Cloud Bucket] --> A2[Data Lakehouse / Warehouse]
        A2 --> A3[Políticas de Seguridad<br>RBAC + Mínimo Privilegio]
    end

    subgraph U[3. Análisis / Uso - Arquitectura Medallón]
        U1[Bronce: Raw] --> U2[Plata: MDM + Llave Maestra + Limpieza]
        U2 --> U3[Oro: Data Marts por Área + DDM]
    end

    subgraph E[4. Retención / Eliminación]
        E1[Evaluación: Inactividad / Tiempos Legales] --> E2{¿Solicitud de Borrado / Fin de Plazo?}
        E2 -- Sí --> E3[Anonimización Irreversible + Lista de Supresión]
        E2 -- No --> E4[Resguardo en Backup Cifrado]
    end

    R3 --> A1
    A3 --> U1
    U3 --> E1 
