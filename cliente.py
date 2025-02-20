import grpc
from concurrent import futures
import viagem_pb2
import viagem_pb2_grpc

def pacote():
    channel = grpc.insecure_channel('localhost:50050')
    stub = viagem_pb2_grpc.AgenciaStub(channel)
    
    pacote = viagem_pb2.PacotePedido(
    tipo_viagem="ida e volta",
    data_ida="2025-06-10",
    data_volta="2025-06-20",
    origem="São Paulo",
    destino="Paris",
    pessoas=2
    )
    resposta_stream = stub.pacote_viagem(pacote)

    print("Resposta do servidor:")
    for resposta in resposta_stream:
        print(resposta.mensagem)
        
if __name__ == "__main__":
    pacote()