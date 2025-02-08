import sistema_banco as cu
while True: 
        
    entrada = (input("""
----------------------INTERFAZ---------------------
          escriba '1' para consultar usuarios
        escriba '2' para realizar una transferencia
               escriba '3' para salir
entrada: """))
    try:
        opcion = int(entrada)
        if opcion == 1:
            cu.consulta()
        elif opcion == 2:
            cu.transaccion()
        elif opcion == 3:
            break

    except Exception as e:
        print(f"error inesperado: {e}")