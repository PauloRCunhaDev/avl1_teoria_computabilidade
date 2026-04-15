
#!/usr/bin/env python3
"""
Máquina de Traços para comparar programas de fatorial.

Nesta versão, o exemplo de não-equivalência é feito entre:
- um programa monolítico do fatorial
- um programa recursivo direto do fatorial

Ambos computam a mesma função n!, mas geram traços diferentes.

Convenção da fita:
- F = operação principal do cálculo
- G = operação auxiliar / avanço de controle

Os testes não são escritos na fita, seguindo o estilo da lauda.
"""

from dataclasses import dataclass
from typing import List, Tuple, Dict, Any

Symbol = str
Label = str
Config = Tuple[Label, str]


def fita_str(fita: List[Symbol]) -> str:
    return "".join(fita) if fita else "ε"


@dataclass
class TraceResult:
    nome: str
    n: int
    valor: Any
    trace: str
    sequencia: List[Config]

    def sequencia_formatada(self) -> str:
        return "".join(f"({rotulo},{conteudo})" for rotulo, conteudo in self.sequencia)


def trace_monolitico(n: int) -> TraceResult:
    """
    Programa monolítico conceitual do fatorial.

    Rótulos:
    1: se n < 0 vá_para 7 senão vá_para 2
    2: se contador == 0 vá_para 6 senão vá_para 3
    3: faça F vá_para 4
    4: faça G vá_para 2
    6: parada
    7: erro

    Para n = 3, o traço é:
    FGFGFG
    """
    if n < 0:
        return TraceResult("monolítico", n, None, "ε", [("1", "ε"), ("7", "ε")])

    fita: List[Symbol] = []
    seq: List[Config] = [("1", fita_str(fita))]

    resultado = 1
    contador = n
    label = "1"

    while label != "6":
        if label == "1":
            label = "2"
            seq.append((label, fita_str(fita)))

        elif label == "2":
            label = "6" if contador == 0 else "3"
            seq.append((label, fita_str(fita)))

        elif label == "3":
            resultado *= contador
            fita.append("F")
            label = "4"
            seq.append((label, fita_str(fita)))

        elif label == "4":
            contador -= 1
            fita.append("G")
            label = "2"
            seq.append((label, fita_str(fita)))

        else:
            raise RuntimeError(f"Rótulo inválido no monolítico: {label}")

    return TraceResult("monolítico", n, resultado, "".join(fita) if fita else "ε", seq)


def trace_iterativo(n: int) -> TraceResult:
    """
    Programa iterativo conceitual do fatorial.

    Rótulos:
    1: se n < 0 vá_para 7 senão vá_para 2
    2: se i > n vá_para 6 senão vá_para 3
    3: faça F vá_para 4
    4: faça G vá_para 2
    6: parada
    7: erro

    Para n = 3, o traço é:
    FGFGFG
    """
    if n < 0:
        return TraceResult("iterativo", n, None, "ε", [("1", "ε"), ("7", "ε")])

    fita: List[Symbol] = []
    seq: List[Config] = [("1", fita_str(fita))]

    resultado = 1
    i = 1
    label = "1"

    while label != "6":
        if label == "1":
            label = "2"
            seq.append((label, fita_str(fita)))

        elif label == "2":
            label = "6" if i > n else "3"
            seq.append((label, fita_str(fita)))

        elif label == "3":
            resultado *= i
            fita.append("F")
            label = "4"
            seq.append((label, fita_str(fita)))

        elif label == "4":
            i += 1
            fita.append("G")
            label = "2"
            seq.append((label, fita_str(fita)))

        else:
            raise RuntimeError(f"Rótulo inválido no iterativo: {label}")

    return TraceResult("iterativo", n, resultado, "".join(fita) if fita else "ε", seq)


def _trace_recursivo_direto_ativacao(k: int, fita: List[Symbol]) -> Tuple[int, List[Config]]:
    """
    Recursivo direto do fatorial:

    R1 def (se k == 0 então R4 senão R2)
    R2 def (faça G; R1(k-1))
    R3 def (faça F; R5)
    R4 def ✓
    R5 def ✓

    Na descida escreve G.
    Na volta escreve F.

    Para n = 3, o traço é:
    GGGFFF
    """
    seq: List[Config] = [("R1", fita_str(fita))]

    if k == 0:
        seq.append(("R4", fita_str(fita)))
        return 1, seq

    seq.append(("R2", fita_str(fita)))
    fita.append("G")
    seq.append(("R1", fita_str(fita)))

    subvalor, subseq = _trace_recursivo_direto_ativacao(k - 1, fita)
    # Evita repetir o primeiro estado já registrado logo acima
    seq.extend(subseq[1:])

    seq.append(("R3", fita_str(fita)))
    fita.append("F")
    seq.append(("R5", fita_str(fita)))

    return k * subvalor, seq


def trace_recursivo_direto(n: int) -> TraceResult:
    if n < 0:
        return TraceResult("recursivo_direto", n, None, "ε", [("R1", "ε"), ("R6", "ε")])

    fita: List[Symbol] = []
    valor, seq = _trace_recursivo_direto_ativacao(n, fita)
    return TraceResult("recursivo_direto", n, valor, "".join(fita) if fita else "ε", seq)


def comparar(a: TraceResult, b: TraceResult) -> Dict[str, Any]:
    return {
        "programa_a": a.nome,
        "programa_b": b.nome,
        "valor_a": a.valor,
        "valor_b": b.valor,
        "traco_a": a.trace,
        "traco_b": b.trace,
        "mesmo_valor": a.valor == b.valor,
        "mesmo_traco": a.trace == b.trace,
        "equivalentes_nesta_MT": (a.valor == b.valor) and (a.trace == b.trace),
    }


def bloco_programa(r: TraceResult) -> List[str]:
    return [
        f"\nPrograma {r.nome}",
        f"Valor computado: {r.valor}",
        f"Traço: {r.trace}",
        "Sequência de fita:",
        r.sequencia_formatada(),
    ]


def bloco_comparacao(comp: Dict[str, Any], titulo: str) -> List[str]:
    return [
        "\n" + "-" * 72,
        titulo,
        "-" * 72,
        f"{comp['programa_a']} x {comp['programa_b']}",
        f"valores: {comp['valor_a']} x {comp['valor_b']}",
        f"traços : {comp['traco_a']} x {comp['traco_b']}",
        f"mesmo_valor = {comp['mesmo_valor']}",
        f"mesmo_traco = {comp['mesmo_traco']}",
        f"equivalentes_nesta_MT = {comp['equivalentes_nesta_MT']}",
    ]


def demonstracao(n: int) -> str:
    mon = trace_monolitico(n)
    it = trace_iterativo(n)
    rec = trace_recursivo_direto(n)

    comp_eq = comparar(mon, it)
    comp_neq = comparar(mon, rec)

    linhas = []
    linhas.append("=" * 72)
    linhas.append(f"DEMONSTRAÇÃO DA MÁQUINA DE TRAÇOS PARA f(n) = n!, com n = {n}")
    linhas.append("=" * 72)

    for r in (mon, it, rec):
        linhas.extend(bloco_programa(r))

    linhas.extend(bloco_comparacao(comp_eq, "EXEMPLO DE EQUIVALÊNCIA"))
    linhas.extend(bloco_comparacao(comp_neq, "EXEMPLO DE NÃO-EQUIVALÊNCIA"))

    linhas.append("\nResumo:")
    linhas.append("- Equivalência: monolítico x iterativo")
    linhas.append("- Não-equivalência: monolítico x recursivo_direto")
    linhas.append("- Ambos no caso de não-equivalência computam a mesma função n!,")
    linhas.append("  mas os traços diferem.")

    return "\n".join(linhas)


if __name__ == "__main__":
    for n in (0, 1, 3, 5):
        print(demonstracao(n))
        print()