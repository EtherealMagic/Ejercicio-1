import bank_system as cu

while True: 
        
    user_input = (input("""
----------------------INTERFACE---------------------
          Type '1' to search a user
        Type '2' to make a transaction
               Type '3' to exit
input: """))
    try:
        option = int(user_input)
        if option == 1:
            cu.query()
        elif option == 2:
            cu.transaction()
        elif option == 3:
            break

    except Exception as e:
        print(f"Unexpected error: {e}")
