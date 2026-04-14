#!/usr/bin/env python3
"""
Máquina de Traços para comparar programas de fatorial.

Base conceitual usada:
- Máquina de Traços: produz um rastro/histórico da ocorrência das operações.
- Para monolíticos/iterativos, a comparação forte pode ser feita a partir da
  ordem das operações observáveis.
- Para recursivo, aqui exibimos um contraexemplo por traço: mesma função
  computada, mas comportamento observável diferente nesta MT.

Convenção desta implementação:
- A fita guarda apenas identificadores de operação.
- Os testes guiam o fluxo, mas não são escritos na fita, como no exemplo da lauda.
- A saída "sequência de fita" segue o formato (rótulo, fita).

Alfabeto de operações desta MT:
I = inicialização
M = multiplicação do acumulador
U = atualização da variável de controle
F = finalização com sucesso
E = erro de entrada
C = chamada recursiva
B = caso-base recursivo
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
    Programa monolítico conceitual equivalente ao cálculo iterativo do fatorial.

    Rótulos:
    1: faça I vá_para 2
    2: se n < 0 vá_para 7 senão vá_para 3
    3: se contador == 0 vá_para 6 senão vá_para 4
    4: faça M vá_para 5
    5: faça U vá_para 3
    6: faça F vá_para 8
    7: faça E vá_para 8
    8: parada
    """
    fita: List[Symbol] = []
    seq: List[Config] = [("1", fita_str(fita))]

    resultado = 1
    contador = n
    label = "1"

    while label != "8":
        if label == "1":
            fita.append("I")
            label = "2"
            seq.append((label, fita_str(fita)))

        elif label == "2":
            label = "7" if n < 0 else "3"
            seq.append((label, fita_str(fita)))

        elif label == "3":
            label = "6" if contador == 0 else "4"
            seq.append((label, fita_str(fita)))

        elif label == "4":
            resultado *= contador
            fita.append("M")
            label = "5"
            seq.append((label, fita_str(fita)))

        elif label == "5":
            contador -= 1
            fita.append("U")
            label = "3"
            seq.append((label, fita_str(fita)))

        elif label == "6":
            fita.append("F")
            label = "8"
            seq.append((label, fita_str(fita)))

        elif label == "7":
            fita.append("E")
            resultado = None
            label = "8"
            seq.append((label, fita_str(fita)))

        else:
            raise RuntimeError(f"Rótulo inválido no monolítico: {label}")

    return TraceResult(
        nome="monolítico",
        n=n,
        valor=resultado,
        trace="".join(fita),
        sequencia=seq,
    )


def trace_iterativo(n: int) -> TraceResult:
    """
    Programa iterativo com a mesma função computada e a mesma abstração observável.

    Rótulos:
    1: faça I vá_para 2
    2: se n < 0 vá_para 7 senão vá_para 3
    3: se i > n vá_para 6 senão vá_para 4
    4: faça M vá_para 5
    5: faça U vá_para 3
    6: faça F vá_para 8
    7: faça E vá_para 8
    8: parada
    """
    fita: List[Symbol] = []
    seq: List[Config] = [("1", fita_str(fita))]

    resultado = 1
    i = 1
    label = "1"

    while label != "8":
        if label == "1":
            fita.append("I")
            label = "2"
            seq.append((label, fita_str(fita)))

        elif label == "2":
            label = "7" if n < 0 else "3"
            seq.append((label, fita_str(fita)))

        elif label == "3":
            label = "6" if i > n else "4"
            seq.append((label, fita_str(fita)))

        elif label == "4":
            resultado *= i
            fita.append("M")
            label = "5"
            seq.append((label, fita_str(fita)))

        elif label == "5":
            i += 1
            fita.append("U")
            label = "3"
            seq.append((label, fita_str(fita)))

        elif label == "6":
            fita.append("F")
            label = "8"
            seq.append((label, fita_str(fita)))

        elif label == "7":
            fita.append("E")
            resultado = None
            label = "8"
            seq.append((label, fita_str(fita)))

        else:
            raise RuntimeError(f"Rótulo inválido no iterativo: {label}")

    return TraceResult(
        nome="iterativo",
        n=n,
        valor=resultado,
        trace="".join(fita),
        sequencia=seq,
    )


def _trace_recursivo_ativacao(k: int, fita: List[Symbol]) -> Tuple[int, List[Config]]:
    """
    Sub-rotinas recursivas conceituais:
    R1 def (se k == 0 então R4 senão R2)
    R2 def (faça C; R1(k-1))
    R3 def (faça M; R5)
    R4 def (faça B; R5)
    R5 def ✓
    """
    seq: List[Config] = [("R1", fita_str(fita))]

    if k == 0:
        seq.append(("R4", fita_str(fita)))
        fita.append("B")
        seq.append(("R5", fita_str(fita)))
        return 1, seq

    seq.append(("R2", fita_str(fita)))
    fita.append("C")
    subvalor, subseq = _trace_recursivo_ativacao(k - 1, fita)
    seq.extend(subseq)

    seq.append(("R3", fita_str(fita)))
    fita.append("M")
    seq.append(("R5", fita_str(fita)))
    return k * subvalor, seq


def trace_recursivo(n: int) -> TraceResult:
    fita: List[Symbol] = []

    if n < 0:
        seq = [("R1", "ε"), ("R6", "ε")]
        fita.append("E")
        seq.append(("R5", fita_str(fita)))
        return TraceResult(
            nome="recursivo",
            n=n,
            valor=None,
            trace="".join(fita),
            sequencia=seq,
        )

    valor, seq = _trace_recursivo_ativacao(n, fita)
    return TraceResult(
        nome="recursivo",
        n=n,
        valor=valor,
        trace="".join(fita),
        sequencia=seq,
    )


def comparar(a: TraceResult, b: TraceResult) -> Dict[str, Any]:
    return {
        "programa_a": a.nome,
        "programa_b": b.nome,
        "mesmo_valor": a.valor == b.valor,
        "mesmo_traco": a.trace == b.trace,
        "equivalentes_nesta_MT": (a.valor == b.valor) and (a.trace == b.trace),
    }


def demonstracao(n: int) -> str:
    mon = trace_monolitico(n)
    it = trace_iterativo(n)
    rec = trace_recursivo(n)

    comp_mi = comparar(mon, it)
    comp_ir = comparar(it, rec)
    comp_mr = comparar(mon, rec)

    linhas = []
    linhas.append("=" * 72)
    linhas.append(f"DEMONSTRAÇÃO DA MÁQUINA DE TRAÇOS PARA f(n) = n!, com n = {n}")
    linhas.append("=" * 72)
    for r in (mon, it, rec):
        linhas.append(f"\nPrograma {r.nome}")
        linhas.append(f"Valor computado: {r.valor}")
        linhas.append(f"Traço: {r.trace}")
        linhas.append("Sequência de fita:")
        linhas.append(r.sequencia_formatada())

    linhas.append("\n" + "-" * 72)
    linhas.append("COMPARAÇÕES")
    linhas.append("-" * 72)
    for comp in (comp_mi, comp_ir, comp_mr):
        linhas.append(
            f"{comp['programa_a']} x {comp['programa_b']}: "
            f"mesmo_valor={comp['mesmo_valor']}, "
            f"mesmo_traco={comp['mesmo_traco']}, "
            f"equivalentes_nesta_MT={comp['equivalentes_nesta_MT']}"
        )

    linhas.append("\nLeitura esperada:")
    linhas.append("- monolítico x iterativo: equivalentes nesta MT")
    linhas.append("- iterativo x recursivo: não equivalentes nesta MT")
    linhas.append("- monolítico x recursivo: não equivalentes nesta MT")
    return "\n".join(linhas)


if __name__ == "__main__":
    # Exemplos rápidos para a apresentação
    for n in (0, 1, 3, 5):
        print(demonstracao(n))
        print()
