import grpc
from concurrent import futures
import viagem_pb2
import viagem_pb2_grpc

class AgenciaViagem(viagem_pb2_grpc.AgenciaServicer):

    def __init__(self):
        self.companhia_aerea_channel = grpc.insecure_channel('localhost:50051')
        self.companhia_aerea_stub = viagem_pb2_grpc.CompanhiaAereaStub(self.companhia_aerea_channel)

        self.rede_hoteleira_channel = grpc.insecure_channel('localhost:50052')
        self.hotel_stub = viagem_pb2_grpc.HotelStub(self.rede_hoteleira_channel)

        self.locadora_carro_channel = grpc.insecure_channel('localhost:50053')
        self.locadora_carro_stub = viagem_pb2_grpc.CarroStub(self.locadora_carro_channel)
        
    def pacote_viagem(self, request, context):
        PACOTE_ID = 555
        # PASSAGEM
        pedido = viagem_pb2.PassagemPedido(
        tipo_viagem=request.tipo_viagem,
        data_ida=request.data_ida,
        data_volta=request.data_volta,
        origem=request.origem,
        destino=request.destino,
        pessoas=request.pessoas,
        id= PACOTE_ID
        )
        reposta = self.companhia_aerea_stub.reserva_passagem(pedido)
        print(reposta.sucesso, "passagem")
        if reposta.sucesso == False:
            yield viagem_pb2.PacoteResposta(sucesso=reposta.sucesso, mensagem="falha na reserva de passagem")
            print("falha na reserva de passagem")
            pedido = viagem_pb2.RollbackPassagemPedido(
            id= PACOTE_ID
            )
            reposta = self.companhia_aerea_stub.rollback_reserva(pedido)
            yield viagem_pb2.PacoteResposta(sucesso=reposta.sucesso, mensagem=reposta.mensagem)
            return
            
        yield viagem_pb2.PacoteResposta(sucesso=reposta.sucesso, mensagem=reposta.mensagem)

        # HOTEL 
        reposta = self.hotel_stub.reserva_hotel(pedido)
        print(reposta.sucesso, "hotel")
        if reposta.sucesso == False:
            yield viagem_pb2.PacoteResposta(sucesso=reposta.sucesso, mensagem="falha na reserva do hotel")
            print("falha na reserva do hotel")
            pedido = viagem_pb2.RollbackHotelPedido(
            id= PACOTE_ID
            )
            reposta = self.hotel_stub.rollback_hotel(pedido)
            yield viagem_pb2.PacoteResposta(sucesso=reposta.sucesso, mensagem=reposta.mensagem)
            reposta = self.companhia_aerea_stub.rollback_reserva(pedido)
            yield viagem_pb2.PacoteResposta(sucesso=reposta.sucesso, mensagem=reposta.mensagem)
            return
        
        yield viagem_pb2.PacoteResposta(sucesso=reposta.sucesso, mensagem=reposta.mensagem)
        
        # CARRO
        reposta = self.locadora_carro_stub.reserva_carro(pedido)
        print(reposta.sucesso, "carro")
        if reposta.sucesso == False:
            yield viagem_pb2.PacoteResposta(sucesso=reposta.sucesso, mensagem="falha na reserva do carro")
            print("falha na reserva do carro")
            pedido = viagem_pb2.RollbackCarroPedido(
            id= PACOTE_ID
            )
            reposta = self.locadora_carro_stub.rollback_carro(pedido)
            yield viagem_pb2.PacoteResposta(sucesso=reposta.sucesso, mensagem=reposta.mensagem)
            reposta = self.hotel_stub.rollback_hotel(pedido)
            yield viagem_pb2.PacoteResposta(sucesso=reposta.sucesso, mensagem=reposta.mensagem)
            reposta = self.companhia_aerea_stub.rollback_reserva(pedido)
            yield viagem_pb2.PacoteResposta(sucesso=reposta.sucesso, mensagem=reposta.mensagem) 
            return
        
        yield viagem_pb2.PacoteResposta(sucesso=reposta.sucesso, mensagem=reposta.mensagem)
        yield viagem_pb2.PacoteResposta(sucesso=True, mensagem='Seu pacote de viagem foi efetivado com sucesso')
        return

    
def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    viagem_pb2_grpc.add_AgenciaServicer_to_server(AgenciaViagem(), server)
    server.add_insecure_port('[::]:50050')
    server.start()
    print("server AgenciaViagemServicer iniciado")
    server.wait_for_termination()

if __name__ == '__main__':
    server()