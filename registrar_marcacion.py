from db_connection import get_connection

def registrar_marcacion(empleado_id, tipo, fecha_hora, origen="python"):
    conn = get_connection()
    if conn is None:
        print("No se pudo conectar a la base de datos")
        return
    
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO marcaciones (empleado_id, tipo, fecha_hora, origen)
            VALUES (%s, %s, %s, %s)
        """, (empleado_id, tipo, fecha_hora, origen))

        conn.commit()
        print(f"✔ Marcación '{tipo}' registrada correctamente para empleado {empleado_id}")

        cur.close()
        conn.close()

    except Exception as e:
        print("❌ Error al registrar marcación:", e)

# EJEMPLO DE USO
registrar_marcacion(1, 'E', '2025-01-10 08:00:00')
registrar_marcacion(1, 'S', '2025-01-10 17:30:00')
