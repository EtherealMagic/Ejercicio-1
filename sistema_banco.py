import sqlite3 
import pandas as pd

class Consultor:
    def __init__(self, nombre):
        self.nombre = nombre
    
    def consultar_usuario(self):
        return f"SELECT * FROM cuentas WHERE nombre = '{self.nombre}'"
    
class Transaccionista:
    def __init__(self, usuario1, usuario2, valor):
        self.usuario1 = usuario1
        self.usuario2 = usuario2
        self.valor = valor
    
    def hacer_transaccion(self):
        return [
            f"UPDATE cuentas SET saldo = saldo + {self.valor} WHERE nombre = '{self.usuario1}';",
            f"UPDATE cuentas SET saldo = saldo - {self.valor} WHERE nombre = '{self.usuario2}';"
        ]
    
    def comprobar_saldo(self):
        return f"SELECT saldo FROM cuentas WHERE nombre = '{self.usuario2}'"
        

def consulta():
    with sqlite3.connect("C:/Users/tobia/OneDrive/Desktop/Proyectos/Ejercicio_banco/cuentas_bancarias.db") as conectar:
        while True:
            mi_cuenta = Consultor(input("Introduzca su nombre: ").lower())
            consulta = mi_cuenta.consultar_usuario()
            try:
                mostrar_consulta = pd.read_sql_query(consulta, conectar)
                if mostrar_consulta.empty:
                    print("Usuario no encontrado")
                else:
                    print(mostrar_consulta)
                    break
            except Exception as e:
                print(f"Error inesperado: {e}")

def transaccion():
    with sqlite3.connect("C:/Users/tobia/OneDrive/Desktop/Proyectos/Ejercicio_banco/cuentas_bancarias.db") as conectar:
        cursor = conectar.cursor()
        persona1 = input("¿Qué usuario pide plata?: ").lower()
        persona2 = input("¿Qué usuario le da la plata?: ").lower()
        plata = abs(int(input("¿Cuánta plata le pide?: ")))
        
        cursor.execute(f"SELECT COUNT(*) FROM cuentas WHERE nombre = '{persona1}'")
        usuario1_existe = cursor.fetchone()[0] > 0

        cursor.execute(f"SELECT COUNT(*) FROM cuentas WHERE nombre = '{persona2}'")
        usuario2_existe = cursor.fetchone()[0] > 0

        if not usuario1_existe or not usuario2_existe:
            print("Error: Uno o ambos usuarios no existen en la base de datos.")
            return

        formar_transaccion = Transaccionista(persona1, persona2, plata)
        comprobacion = formar_transaccion.comprobar_saldo()
        cursor.execute(comprobacion)
        saldo_actual = cursor.fetchone()

        if saldo_actual and saldo_actual[0] < plata:
            print("Saldo no disponible")
        else:
            try:
                cursor.execute("BEGIN TRANSACTION;")
                for query in formar_transaccion.hacer_transaccion():
                    cursor.execute(query)
                conectar.commit()
                mostrar_consulta = pd.read_sql_query(f"SELECT * FROM cuentas WHERE nombre IN ('{persona1}', '{persona2}')", conectar)
                print(mostrar_consulta)
            except Exception as e:
                conectar.rollback()
                print(f"Error inesperado: {e}")
