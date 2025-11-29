from db_connection import get_connection

def ausencias():
    conn = get_connection()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM vista_ausencias ORDER BY empleado_id, fecha;
        """)
        rows = cur.fetchall()

        print(f"\n🟠 AUSENCIAS ENCONTRADAS: {len(rows)} registros\n")

        if len(rows) == 0:
            print("❗ No hay ausencias registradas.")
        else:
            for r in rows:
                print(r)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    ausencias()
