import socket
import threading

has_error = False
symbol_table = {}
channels = {}

# Functions for the execution of each intruction
def run_stmt(stmt):     
    #time.sleep(1)
    if stmt[0] == 'SEQ':
        # For each instruction in the SEQ block, execute
        for s in stmt[1]:
            run_stmt(s)
    
    elif stmt[0] == 'PAR':
        threads = []
        # For each instruction in the PAR block, create a thread and execute.
        for s in stmt[1]:
            thread = threading.Thread(target=run_stmt, args=(s,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
            
    elif stmt[0] == 'IF':
        if execute_bool(stmt[1]):
            for s in stmt[2]:
                run_stmt(s)
    
    elif stmt[0] == 'WHILE':
        while execute_bool(stmt[1]):
            for s in stmt[2]:
                run_stmt(s)
    
    elif stmt[0] == 'LOG':
        if isinstance(stmt[1], tuple):
            for v in stmt[1]:
                display_log(v)
        else:
            display_log(stmt[1])
    
    # Fibonacci
    elif stmt[0] == 'FIBONACCI':
        if isinstance(stmt[1], tuple):
            fibonacci(run_stmt(stmt[1]))
        else:
            fibonacci(stmt[1])

    # Factorial            
    elif stmt[0] == 'FACTORIAL':
        if isinstance(stmt[1], tuple):
            factorial(run_stmt(stmt[1])) 
        else:
            factorial(stmt[1])

    # Attrubution case.
    elif stmt[0] == '=':
        var_name = stmt[1]
        value = stmt[2]

        # Atribution with input
        if value == "INPUT":
            value = run_stmt((value, var_name))     
        
        # Simple attributions
        else:
            value = evaluate_expr(value)
            symbol_table[var_name] = value
    
    # Channel declaration, only saves the channel in the channels tables.
    elif stmt[0] == "C_CHANNEL":
        channels[stmt[1]] = (stmt[2], stmt[3])

    # When the instruction is using a communication channel
    elif not isinstance(stmt[0], tuple) and stmt[0] in channels:
 
        if stmt[1] == 'SEND':
            channel_name = stmt[0]
            channel = channels.get(channel_name)
            if channel:
                if (len(stmt) == 6):
                    _, _, operation, value1, value2, result = stmt
                    send_data(channel[1], 9999, f"{symbol_table[operation]},{symbol_table[value1]},{symbol_table[value2]},{result}")
                elif (len(stmt) == 3):
                    send_data(channel[1], 9998, f"{symbol_table[stmt[2]]}")


        elif stmt[1] == "RECEIVE":
            channel_name = stmt[0]
            channel = channels.get(channel_name)
            if channel:
                if (len(stmt) == 6):
                    stringRec = receive_data(channel[1], 9999)
                    operation, value1, value2, result = stringRec.split(",")
                    symbol_table[stmt[2]] = operation
                    symbol_table[stmt[3]] = int(value1)
                    symbol_table[stmt[4]] = int(value2)
                    symbol_table[stmt[5]] = result
                elif (len(stmt) == 3):
                    stringRec = receive_data(channel[1], 9998)
                    symbol_table[stmt[2]] = stringRec

    # Loops untill it executes all the blocks. Permits the execution of SEQ and PAR blocks in the same code.
    elif isinstance(stmt, tuple):
        for s in stmt:
            run_stmt(s)

# Executes all types of output 
def display_log(v):
    var_name = v
    var_value = symbol_table.get(var_name, None)
    # If it is in the symbol's table
    if var_value is not None:
        formatted_output = var_value
        print(formatted_output, end='')
    else:
        formatted_output = var_name.replace("\\n", "\n")
        print(formatted_output, end='')

# Executes boolean expression
def execute_bool(expr):
    if isinstance(expr, tuple):

        op, left, right = expr

        if left in symbol_table:
            left = symbol_table.get(left, 0)  # Gets the variable's value if it exists
        if right in symbol_table:
            right = symbol_table.get(right, 0)  # Gets the variable's value if it exists
            
        if op == '<':
            return evaluate_expr(left) < evaluate_expr(right)
        elif op == '>':
            return evaluate_expr(left) > evaluate_expr(right)
        elif op == '<=':
            return evaluate_expr(left) <= evaluate_expr(right)
        elif op == '>=':
            return evaluate_expr(left) >= evaluate_expr(right)
        elif op == '==':
            return evaluate_expr(left) == evaluate_expr(right)
        elif op == '!=':
            return evaluate_expr(left) != evaluate_expr(right)
    return False

# Evaluate arithmetic expressions
def evaluate_expr(expr):
    if isinstance(expr, int) or expr in {'-', '+', '*', '/'}:
        return expr
    elif isinstance(expr, tuple):
        op, left, right = expr
        if op == '+':
            return evaluate_expr(left) + evaluate_expr(right)
        elif op == '-':
            return evaluate_expr(left) - evaluate_expr(right)
        elif op == '*':
            return evaluate_expr(left) * evaluate_expr(right)
        elif op == '/':
            return evaluate_expr(left) / evaluate_expr(right)
        elif any(op == x for x in ['<', '>', '<=', '>=', '==', '!=']):
            return execute_bool(expr)
    elif isinstance(expr, str):
        return symbol_table.get(expr, expr)  # Returns the variable's value from the symbols table

# Print fibonacci series storing the last number
def fibonacci(n):
    count = 0
    num1 = 0
    num2 =  1
    next_number = num2
    while count <= n:
        print(next_number, end=" ")
        count += 1
        num1, num2 = num2, next_number
        next_number = num1 + num2
    print()
    
# Calculate factorial of n
def factorial(n):
    value = n
    for i in range(n-1, 0, -1):
        value *= n
    print(value)

# Client connection
def send_data(host, port, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to a host
        sock.connect((host, port))
        # Sends data
        sock.sendall(data.encode())
    finally:
        # Close socket
        sock.close()


# Create a TCP host ready for recieving connections
def receive_data(host, port):
    # Start the TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Define IP and Port
        server_socket.bind((host, port))
        # Listen for connections
        server_socket.listen(5)
        
        while True:
            # Accept connections
            client_socket, address = server_socket.accept()
            
            # Recieve data
            data = client_socket.recv(1024)
            if not data:
                break
            
            # Returns the recieved string
            return data.decode()
            # Close the client connection
            client_socket.close()
    finally:
        # Close server connectionr
        server_socket.close()
