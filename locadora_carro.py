import grpc
from concurrent import futures
import viagem_pb2
import viagem_pb2_grpc
class LocadoraCarro(viagem_pb2_grpc.CarroServicer):

    def reserva_carro(self, request, context):
        return viagem_pb2.CarroResposta(sucesso=False, mensagem="Carro reservada com sucesso")

    def rollback_carro(self, request, context):
        print(f"Cancelando reserva do carro do pacote ID:{request.id}")
        return viagem_pb2.RollbackCarroResposta(mensagem="A reserva do carro foi estornado")

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    viagem_pb2_grpc.add_CarroServicer_to_server(LocadoraCarro(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("server AgenciaViagemServicer iniciado")
    server.wait_for_termination()

if __name__ == '__main__':
    server()