class Disciplina:
    def __init__(self, codigo, nomeDisciplina, nomeProfessor, quantidadeAlunos, cargaHoraria, mediaTurma):
        self.codigo = codigo
        self.nomeDisciplina = nomeDisciplina
        self.nomeProfessor = nomeProfessor
        self.quantidadeAlunos = quantidadeAlunos
        self.cargaHoraria = cargaHoraria
        self.mediaTurma = mediaTurma
    
    def __str__(self):
        return f"Disciplina(codigo={self.codigo}, nome={self.nomeDisciplina}, professor={self.nomeProfessor})"


def converterDisciplinaDicionario(disc: Disciplina):
    dicionario = {
        "__class__": "disciplina.Disciplina",
        "codigo": disc.codigo,
        "nomeDisciplina": disc.nomeDisciplina,
        "nomeProfessor": disc.nomeProfessor,
        "quantidadeAlunos": disc.quantidadeAlunos,
        "cargaHoraria": disc.cargaHoraria,
        "mediaTurma": disc.mediaTurma
    }
    return dicionario


def converterDicionario(classname, dicionario: dict):
    disc = Disciplina(
        dicionario["codigo"],
        dicionario["nomeDisciplina"],
        dicionario["nomeProfessor"],
        dicionario["quantidadeAlunos"],
        dicionario["cargaHoraria"],
        dicionario["mediaTurma"]
    )
    return disc