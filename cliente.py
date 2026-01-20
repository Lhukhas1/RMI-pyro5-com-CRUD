import Pyro5.client
import Pyro5.api
import sys
import disciplina


class Cliente:
    def __init__(self, nome_servico = "lucas.gabriel"):       
        print("Conectando ao servidor")
        
        input("PARADA 1 - Proxy criado")
        self.crud_proxy = Pyro5.client.Proxy(f'PYRONAME:{nome_servico}')
        
        input("PARADA 2 - bind")
        if not self.crud_proxy._pyroBind():
            print("Erro ao conectar com o servidor!")
            sys.exit(-1)
        

        input("PARADA 3 - conversores registrados")
        Pyro5.api.register_class_to_dict(
            disciplina.Disciplina,
            disciplina.converterDisciplinaDicionario
        )
        
        Pyro5.api.register_dict_to_class(
            "disciplina.Disciplina",
            disciplina.converterDicionario
        )
        
        self.fechar = False
        print("Conectado com sucesso!\n")

    
    def executar(self):
        while not self.fechar:
            try:
                self.menu_crud()
                
                if self.fechar:
                    break
                
                continuar = input("\nNova operação (S/N): ").upper()
                if continuar not in ["SIM", 'S']:
                    break
            
            except KeyboardInterrupt:
                print("\nEncerrando...")
                break
            except Exception as e:
                print(f"Erro: {e}")
                break
    
    def menu_crud(self):
        print("\n\tSistema CRUD - RMI (Pyro5)")
        print("C - Criar (Adicionar disciplina)")
        print("R - Buscar disciplina por código")
        print("L - Listar todas as disciplinas")
        print("U - Atualizar disciplina")
        print("D - Deletar disciplina")
        print("E - Encerrar")
        
        while True:
            opcao = input("Escolha uma opção: ").upper()
            if opcao not in ['C', 'R', 'U', 'D', 'L', 'E']:
                print("Opção inválida!")
            elif opcao == 'E':
                self.fechar = True
                return
            else:
                break
        
        match opcao:
            case 'C':
                self.criar()
            case 'R':
                self.buscar()
            case 'L':
                self.listar()
            case 'U':
                self.atualizar()
            case 'D':
                self.deletar()
        
        # Parada 4: Apos gerar a requisicao
        if(opcao != 'E'):
            input(f"\nPARADA 4 - Requisição {opcao} enviada")
    
    def criar(self):
        print("\n\t--- ADICIONAR DISCIPLINA ---")
        try:
            codigo = input("Código da disciplina: ").upper()
            nomeDisciplina = input("Nome da Disciplina: ")
            nomeProfessor = input("Nome do Professor: ")
            quantidadeAlunos = int(input("Quantidade de alunos: "))
            cargaHoraria = int(input("Carga Horária: "))
            mediaTurma = float(input("Média de notas da turma: "))
            
            # Cria o objeto  da Disciplina
            disc = disciplina.Disciplina(
                codigo,
                nomeDisciplina,
                nomeProfessor,
                quantidadeAlunos,
                cargaHoraria,
                mediaTurma
            )
    
            resultado = self.crud_proxy.adicionar(disc)
            
            if resultado:
                print("Disciplina adicionada!")
            else:
                print("Erro ao adicionar disciplina")
        
        except ValueError:
            print("Erro: valor invalido!")
        except Exception as e:
            print(f"Erro ao adicionar: {e}")
    
    def buscar(self):
        print("\n\t--- BUSCAR DISCIPLINA ---")
        try:
            codigo = input("Código da disciplina: ").upper()
            
            resultado = self.crud_proxy.buscar(codigo)
            
            if resultado:
                print("\nDisciplina encontrada:")
                self.exibir_disciplina(resultado)
            else:
                print("Disciplina não encontrada!")
        
        except Exception as e:
            print(f"Erro ao fazer busca: {e}")
    
    def listar(self):
        print("\n\t--- LISTAR TODAS AS DISCIPLINAS ---")
        try:
            disciplinas = self.crud_proxy.listarTodas()
            
            if disciplinas:
                print(f"\n{len(disciplinas)} disciplina(s) encontrada(s):\n")
                for i, disc in enumerate(disciplinas, 1):
                    print(f"{i}. {'-'*35}")
                    self.exibir_disciplina(disc)
            else:
                print("Nenhuma disciplina cadastrada!")
        
        except Exception as e:
            print(f"Erro ao listar disciplinas: {e}")
    
    def atualizar(self):
        print("\n\t--- ATUALIZAR DISCIPLINA ---")
        try:
            codigoAntigo = input("Código da disciplina a atualizar: ").upper()
            
            print("\nInforme os NOVOS dados:")
            codigo = input("Novo código: ").upper()
            nomeDisciplina = input("Nome da Disciplina: ")
            nomeProfessor = input("Nome do Professor: ")
            quantidadeAlunos = int(input("Quantidade de alunos: "))
            cargaHoraria = int(input("Carga Horária: "))
            mediaTurma = float(input("Média de notas: "))
            
            disc = disciplina.Disciplina(
                codigo,
                nomeDisciplina,
                nomeProfessor,
                quantidadeAlunos,
                cargaHoraria,
                mediaTurma
            )
            
            resultado = self.crud_proxy.atualizar(codigoAntigo, disc)
            
            if resultado:
                print("Disciplina atualizada!")
            else:
                print("Disciplina não encontrada!")
        
        except ValueError:
            print("Erro: valor invalido!")
        except Exception as e:
            print(f"Erro ao atualizar: {e}")

    def deletar(self):
        print("\n\t--- DELETAR DISCIPLINA ---")
        try:
            codigo = input("Código da disciplina: ").upper()
            
            confirmacao = input(f"Tem certeza que deseja deletar '{codigo}'? (S/N): ").upper()
            if confirmacao not in ['S', 'SIM']:
                print("Operação cancelada.")
                return

            resultado = self.crud_proxy.remover(codigo)
            
            if resultado:
                print("Disciplina removida!")
            else:
                print("Disciplina não encontrada!")
        
        except Exception as e:
            print(f"Erro ao deletar: {e}")

    def exibir_disciplina(self, disc):
        print(f"   Código: {disc.codigo}")
        print(f"   Disciplina: {disc.nomeDisciplina}")
        print(f"   Professor: {disc.nomeProfessor}")
        print(f"   Alunos: {disc.quantidadeAlunos}")
        print(f"   Carga Horária: {disc.cargaHoraria}h")
        print(f"   Média da Turma: {disc.mediaTurma:.2f}")


def main():  
    print("Abrindo cliente...\n")
    
    cliente = Cliente(nome_servico = "lucas.gabriel")
    cliente.executar()
    
    print("\nEncerrando cliente")


if __name__ == "__main__":
    main()