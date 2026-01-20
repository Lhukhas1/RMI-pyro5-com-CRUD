import Banco
import Pyro5.server
import Pyro5.core
import Pyro5.api
import disciplina

@Pyro5.server.expose
class CRUD:
    def __init__(self):
        self.banco = Banco.Banco()
        print("Sistema CRUD iniciado!")
    
    def adicionar(self, disc):
        resultado = self.banco.adicionar(
            disc.codigo,
            disc.nomeDisciplina,
            disc.nomeProfessor,
            disc.quantidadeAlunos,
            disc.cargaHoraria,
            disc.mediaTurma
        )
        return resultado
    
    def buscar(self, codigo):
        dados = self.banco.buscar(codigo)
        if dados:
            disc = disciplina.Disciplina(
                dados[0],  # codigo
                dados[1],  # nomeDisciplina
                dados[2],  # nomeProfessor
                dados[3],  # quantidadeAlunos
                dados[4],  # cargaHoraria
                dados[5]   # mediaTurma
            )
            return disc
        return None
    
    def listarTodas(self):
        dados = self.banco.listarTodas()
        disciplinas = []
        for registro in dados:
            disc = disciplina.Disciplina(
                registro[0],  # codigo
                registro[1],  # nomeDisciplina
                registro[2],  # nomeProfessor
                registro[3],  # quantidadeAlunos
                registro[4],  # cargaHoraria
                registro[5]   # mediaTurma
            )
            disciplinas.append(disc)
        return disciplinas
    
    def atualizar(self, codigoAntigo, disc):
        resultado = self.banco.update(
            codigoAntigo,
            disc.codigo,
            disc.nomeDisciplina,
            disc.nomeProfessor,
            disc.quantidadeAlunos,
            disc.cargaHoraria,
            disc.mediaTurma
        )
        return resultado
    
    def remover(self, codigo):
        resultado = self.banco.remover(codigo)
        return resultado


def main():
    print("Iniciando servidor...")
    
    daemon = Pyro5.server.Daemon()
    
    crud = CRUD()
    
    endereco = daemon.register(crud)
    print(f'URI do objeto: {endereco}')
    
    Pyro5.api.register_dict_to_class(
        "disciplina.Disciplina",
        disciplina.converterDicionario
    )
    
    Pyro5.api.register_class_to_dict(
        disciplina.Disciplina,
        disciplina.converterDisciplinaDicionario
    )
    
    try:
        ns = Pyro5.core.locate_ns()
        ns.register("lucas.gabriel", endereco)
        print("Aguardando requisiçoes...")
    except Exception as e:
        print(f"Erro ao registrar no nameserver: {e}")
        return
    
    daemon.requestLoop()


if __name__ == '__main__':
    main()