""" --------------------------------------------------------------------------------------
   Programa que implementa o client da comunicacao TCP/IP com Diffie-Hellman
   Objetivo: Comunicacao de cliente-servidor fazendo o estabelecimento de Chave Secreta
   com Diffie-Hellman
   Restricoes: o programa necessita que um servidor esteja em execucao para que seja possivel
    a comunicacao.

   Autor: Brendon e Marllon.
   Disciplina: Redes II
   Data da ultima atualizacao: 28/07/2021
----------------------------------------------------------------------------------------"""

import socket
from common.util import *
from des import DesKey


def connect_to_server(host, port) -> socket.SocketIO:
    """ Create and return TCP/IP socket """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (host, port)
    print('[CLIENT LOG] connecting to {} port {}'.format(host,port)) 
    sock.connect(server_address)
    return sock


def send_message(sock, message) -> None:
    """ Send message to server """
    print('[CLIENT LOG] sending message to server: {}'.format(str(message)))
    if type(message) == bytes:
        
        sock.sendall(message)
    else:
        sock.sendall(str.encode(str(message)))


def close_connection(sock) -> None:
    """ Close connection """
    sock.close()


def generate_prime_module() -> int:
    """ Generate a random prime number to be used as module number (p) for Diffie-Hellman """
    p = generate_random_prime()
    print('[CLIENT LOG] generate prime module (p) with the value equal {}'.format(p))
    return p


def generate_random_private_key() -> int:
    """ Generate a random private key """
    private_key = random.randint(1, 10000)
    print('[CLIENT LOG] generate random private key equal: {}'.format(str(private_key)))
    return private_key


def calculate_client_result(base, exp, mod) -> int:
    """ Calculate client result """
    result = power(base, exp, mod)
    print('[CLIENT LOG] calculated public result to send for the server: {}'.format(result))
    return result


def calculate_private_shared_key(server_result, client_private_key, p) -> int:
    """ Calculate shared key """
    shared_key = power(server_result, client_private_key, p)
    print('[CLIENT LOG] calculated shared key equal: {}'.format(shared_key))
    return shared_key


def main():
    sock = connect_to_server('localhost', port=10000)
    print('[CLIENT LOG] connected to server')
    try:
        # Defines Diffie-Hellman shared parameters communicating with connected server
        print('[CLIENT LOG] defining Diffie-Hellman parameters with server')
        
        p = generate_prime_module() # Random prime generated by client to be used as module number (p) for Diffie-Hellman
        send_message(sock, str(p))

        g = int(sock.recv(1024).decode(encoding='UTF-8')) # Randomly generated by server to be used as generator (g) for Diffie-Hellman
        print('[CLIENT LOG] received generator randomly generated by the server with value equal: {}'.format(g))

        private_key = generate_random_private_key()

        result = calculate_client_result(g, private_key, p) 
        send_message(sock, str(result))
        
        server_result = int(sock.recv(1024).decode(encoding='UTF-8')) # Server's result received from the socket
        print('[CLIENT LOG] received server_result with value equal: {}'.format(server_result))

        shared_private_key = calculate_private_shared_key(server_result, private_key, p)

        des_key = DesKey(shared_private_key.to_bytes(8, byteorder='big'))

        while True:
            message = input('Enter message to send: ')
            encrypted_message = des_key.encrypt(str.encode(message), padding=True)
            send_message(sock, encrypted_message)

            data = sock.recv(1024)
            print('[CLIENT LOG] received message: {}'.format(data))
            print('[CLIENT LOG] message decrypted: {}'.format(des_key.decrypt(data, padding=True)))
            
    finally:
        print('[CLIENT LOG] closing socket')
        close_connection(sock)


if __name__ == '__main__':
    print("===========================================================================")
    print("Inicio da execucao: programa que implementa o client da comunicacao TCP/IP.")
    print("Prof. Elias P. Duarte Jr.  -  Disciplina Redes II")
    print("Autores: Brendon e Marllon")
    print("===========================================================================")
    main()