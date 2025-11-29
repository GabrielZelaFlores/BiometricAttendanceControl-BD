from db_connection import get_connection

def calcular_tardanzas():
    conn = get_connection()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM vista_tardanzas ORDER BY empleado_id, fecha;
        """)
        rows = cur.fetchall()

        print(f"\n🔵 TARDANZAS ENCONTRADAS: {len(rows)} registros\n")

        if len(rows) == 0:
            print("❗ No hay tardanzas registradas.")
        else:
            for r in rows:
                print(r)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    calcular_tardanzas()
