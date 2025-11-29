from db_connection import get_connection

def reporte_completo():
    conn = get_connection()
    if not conn:
        return

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM vista_reporte_completo
            ORDER BY empleado_id, fecha;
        """)
        rows = cur.fetchall()

        print(f"\n🟣 REPORTE COMPLETO: {len(rows)} registros\n")

        if len(rows) == 0:
            print("❗ No hay datos en el reporte.")
        else:
            for r in rows:
                print(r)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    reporte_completo()
