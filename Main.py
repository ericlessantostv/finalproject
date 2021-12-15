import arcade
import Client
import Server


def main():
    client_address = Server.find_server_address()
    server_address = input("what is the IP address of the server:")
    client = Client(server_address, client_address)
    client.setup()
    arcade.run()


if __name__ == '__main__':
    main()
