from db_connection import get_connection

def generar_reporte(inicio, fin):
    conn = get_connection()
    if conn is None:
        print("No se pudo conectar a la base de datos")
        return

    try:
        cur = conn.cursor()

        query = """
        SELECT 
            e.empleado_id,
            e.nombre || ' ' || e.apellido AS empleado,
            m.fecha_hora::date AS dia,
            MIN(CASE WHEN m.tipo='E' THEN m.fecha_hora END) AS entrada,
            MAX(CASE WHEN m.tipo='S' THEN m.fecha_hora END) AS salida
        FROM empleados e
        LEFT JOIN marcaciones m ON e.empleado_id = m.empleado_id
           AND m.fecha_hora BETWEEN %s AND %s
        GROUP BY e.empleado_id, empleado, m.fecha_hora::date
        ORDER BY e.empleado_id, dia;
        """

        cur.execute(query, (inicio, fin))
        resultados = cur.fetchall()

        print("\n📌 REPORTE DE ASISTENCIA")
        print(f"Periodo: {inicio} → {fin}")
        print("-------------------------------------------")

        for fila in resultados:
            print(fila)

        cur.close()
        conn.close()

    except Exception as e:
        print("❌ Error generando el reporte:", e)

# EJECUCIÓN
generar_reporte("2025-01-01", "2025-01-31")
