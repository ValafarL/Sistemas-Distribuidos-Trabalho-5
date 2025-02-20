import grpc
from concurrent import futures
import viagem_pb2
import viagem_pb2_grpc
class CompanhiaAerea(viagem_pb2_grpc.CompanhiaAereaServicer):

    def reserva_passagem(self, request, context):
        if(request.tipo_viagem == "somente ida"):
            print(f'Reserva, ida para {request.destino} efetivada')
        else:
            print(f'Reserva, ida - {request.destino} e volta - {request.origem} efetivada')
        return viagem_pb2.PassagemResposta(sucesso=True, mensagem="Passagem reservada com sucesso")

    def rollback_reserva(self, request, context):
        print(f"Cancelando passagem do pacote ID:{request.id}")
        return viagem_pb2.RollbackPassagemResposta(mensagem="Sua passagem foi estornada")

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    viagem_pb2_grpc.add_CompanhiaAereaServicer_to_server(CompanhiaAerea(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("server AgenciaViagemServicer iniciado")
    server.wait_for_termination()

if __name__ == '__main__':
    server()