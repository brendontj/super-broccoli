import socket
from common.util import *

def main():
    sock = listen(host='localhost', port=10000)
    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()

        try:
            print('connection from' + str(client_address))

            # Define Diffie-Hellman parameters
            print('Defining Diffie-Hellman parameters with client')
            client_prime_module = connection.recv(128).decode(encoding='UTF-8')
            client_prime_module_number = int(client_prime_module)
            print('received {} as prime module generated by client'.format(client_prime_module))

            prime_generated_number = generate_random_prime()
            print('sending prime generated by server to the client')
            connection.sendall(str.encode(str(prime_generated_number)))

            server_private_key = generate_random_prime() #Client private key
            print('Server Private Key {}'.format(str(server_private_key))) # Move to logging

            client_result = connection.recv(128).decode(encoding='UTF-8')
            client_result_number = int(client_result)
            print('Client received result {}'.format(client_result))

            server_result = power(prime_generated_number, server_private_key, client_prime_module_number)
            print('Server Result {}'.format(str(server_result))) # Move to logging
            connection.sendall(str.encode(str(server_result)))

            shared_private_key = power(client_result_number, server_private_key, client_prime_module_number)
            print('Shared Private Key {}'.format(str(shared_private_key))) # Move to logging

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(128)
                print('received {} message from the client'.format(data))
                if data:
                    print('sending ack by server to the client')
                    connection.sendall(str.encode('ack: ' + str(data.decode(encoding='UTF-8'))))
                else:
                    print('no more data from', client_address)
                    break
                
        finally:
            close_connection(connection)


def listen(host, port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    print('starting up on {} port {}'.format(host, port))
    server_address = (host, port)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)
    return sock

def close_connection(conn):
    # Clean up the connection
    conn.close()    


if __name__ == "__main__":
    main()