import sistema_banco as cu
while True: 
        
    user_input = (input("""
----------------------INTERFACE---------------------
          Type '1' to search a user
        Type '2' to make a transsaction
               Type '3' to exit
input: """))
    try:
        option = int(user_input)
        if option == 1:
            cu.consulta()
        elif option == 2:
            cu.transaccion()
        elif option == 3:
            break

    except Exception as e:
        print(f"unespected error: {e}")
