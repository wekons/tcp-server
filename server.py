import socket
import threading
import datetime
import os
import sys

class TCPServer:
    def __init__(self, host='0.0.0.0', port=None):
        # Usar puerto de variable de entorno o puerto por defecto
        self.host = host
        self.port = port if port is not None else 25075
        self.running = False
        
    def log_message(self, message):
        """Log con timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
        sys.stdout.flush()  # Forzar output inmediato para logs en la nube
        
    def handle_client(self, client_socket, client_address):
        """Maneja cada cliente conectado"""
        self.log_message(f"🔗 Nueva conexión desde: {client_address}")
        
        try:
            while True:
                # Recibir datos
                data = client_socket.recv(4096)
                
                if not data:
                    self.log_message(f"❌ Cliente {client_address} desconectado")
                    break
                
                # Mostrar datos recibidos
                self.log_message(f"📨 Datos de {client_address}:")
                self.log_message(f"   Bytes: {len(data)}")
                self.log_message(f"   Hex: {data.hex()}")
                
                # Intentar mostrar como texto
                try:
                    texto = data.decode('utf-8', errors='ignore').strip()
                    if texto:
                        self.log_message(f"   Texto: {texto}")
                except:
                    pass
                
                # Mostrar bytes raw para análisis
                self.log_message(f"   Raw: {list(data[:50])}{'...' if len(data) > 50 else ''}")
                
                # Enviar respuesta de confirmación
                respuesta = f"OK:{len(data)}bytes:{datetime.datetime.now().strftime('%H:%M:%S')}"
                client_socket.send(respuesta.encode('utf-8'))
                self.log_message(f"📤 Respuesta enviada a {client_address}: {respuesta}")
                
        except Exception as e:
            self.log_message(f"❌ Error con cliente {client_address}: {e}")
        finally:
            client_socket.close()
            self.log_message(f"🔌 Conexión cerrada: {client_address}")
    
    def start(self):
        """Inicia el servidor TCP"""
        try:
            # Crear socket
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind y listen
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            
            self.running = True
            self.log_message(f"🚀 Servidor TCP iniciado en {self.host}:{self.port}")
            self.log_message(f"📡 Esperando conexiones...")
            
            while self.running:
                try:
                    # Aceptar conexiones
                    client_socket, client_address = server_socket.accept()
                    
                    # Crear hilo para cada cliente
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except KeyboardInterrupt:
                    self.log_message("🛑 Servidor detenido por usuario")
                    break
                except Exception as e:
                    self.log_message(f"❌ Error del servidor: {e}")
                    
        except Exception as e:
            self.log_message(f"❌ Error fatal: {e}")
        finally:
            try:
                server_socket.close()
            except:
                pass
            self.log_message("✅ Servidor cerrado")

def main():
    """Función principal"""
    print("=" * 60)
    print("🌐 SERVIDOR TCP PARA PRUEBAS - CLOUD READY")
    print("=" * 60)
    
    # Mostrar configuración
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 25075))
    
    print(f"Host: {host}")
    print(f"Puerto: {port}")
    print(f"Variables de entorno PORT: {os.environ.get('PORT', 'No definida')}")
    print("=" * 60)
    
    # Crear e iniciar servidor
    server = TCPServer(host, port)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n🛑 Cerrando servidor...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()