import grpc
from concurrent import futures
import viagem_pb2
import viagem_pb2_grpc
class RedeHoteleira(viagem_pb2_grpc.HotelServicer):

    def reserva_hotel(self, request, context):
        print(f'Hotel reservado para {request.pessoas} pessoas')
        return viagem_pb2.HotelResposta(sucesso=True, mensagem=f'Hotel reservado para {request.pessoas} pessoas')

    def rollback_hotel(self, request, context):
        print(f"Cancelando hotel do pacote ID:{request.id}")
        return viagem_pb2.RollbackHotelResposta(mensagem="A reserva do hotel foi estornada")

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    viagem_pb2_grpc.add_HotelServicer_to_server(RedeHoteleira(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("server AgenciaViagemServicer iniciado")
    server.wait_for_termination()

if __name__ == '__main__':
    server()