#!/usr/bin/env python3
"""
Máquina de Traços para comparar programas de fatorial.

Versão corrigida:
- A saída principal da máquina de traços é o TRAÇO.
- Testes NÃO escrevem na fita.
- Parada NÃO escreve na fita.
- O identificador H foi removido.
- O campo `valor` é mantido apenas como conferência de que o programa calcula n!.
- O recursivo abaixo é o recursivo obtido por tradução estrutural do monolítico.

Convenção didática adotada:
- F = operação principal do passo de cálculo
- G = operação auxiliar de avanço de controle
- A fita registra apenas operações, nunca testes nem parada.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

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
    observacao: str = ""

    def sequencia_formatada(self) -> str:
        return "".join(f"({rotulo},{conteudo})" for rotulo, conteudo in self.sequencia)


def entrada_invalida(nome: str, n: int, rotulo_inicial: str) -> TraceResult:
    return TraceResult(
        nome=nome,
        n=n,
        valor=None,
        trace="ε",
        sequencia=[(rotulo_inicial, "ε"), ("ERRO", "ε")],
        observacao="Fatorial definido apenas para n >= 0.",
    )


def trace_monolitico(n: int) -> TraceResult:
    """
    Programa monolítico do fatorial.

    Rótulos:
    1: se contador == 0 vá_para 4 senão vá_para 2
    2: faça F vá_para 3
    3: faça G vá_para 1
    4: parada

    Observação:
    - F e G são identificadores abstratos de operação na máquina de traços.
    - A parada não escreve nada na fita.
    """
    if n < 0:
        return entrada_invalida("monolítico", n, "1")

    fita: List[Symbol] = []
    seq: List[Config] = [("1", fita_str(fita))]

    resultado = 1
    contador = n
    label = "1"

    while label != "4":
        if label == "1":
            label = "4" if contador == 0 else "2"
            seq.append((label, fita_str(fita)))

        elif label == "2":
            resultado *= contador
            fita.append("F")
            label = "3"
            seq.append((label, fita_str(fita)))

        elif label == "3":
            contador -= 1
            fita.append("G")
            label = "1"
            seq.append((label, fita_str(fita)))

        else:
            raise RuntimeError(f"Rótulo inválido no monolítico: {label}")

    return TraceResult(
        nome="monolítico",
        n=n,
        valor=resultado,
        trace="".join(fita),
        sequencia=seq,
        observacao="A saída principal da máquina de traços é o traço.",
    )


def trace_iterativo(n: int) -> TraceResult:
    """
    Programa iterativo do fatorial.

    Rótulos:
    1: se i > n vá_para 4 senão vá_para 2
    2: faça F vá_para 3
    3: faça G vá_para 1
    4: parada
    """
    if n < 0:
        return entrada_invalida("iterativo", n, "1")

    fita: List[Symbol] = []
    seq: List[Config] = [("1", fita_str(fita))]

    resultado = 1
    i = 1
    label = "1"

    while label != "4":
        if label == "1":
            label = "4" if i > n else "2"
            seq.append((label, fita_str(fita)))

        elif label == "2":
            resultado *= i
            fita.append("F")
            label = "3"
            seq.append((label, fita_str(fita)))

        elif label == "3":
            i += 1
            fita.append("G")
            label = "1"
            seq.append((label, fita_str(fita)))

        else:
            raise RuntimeError(f"Rótulo inválido no iterativo: {label}")

    return TraceResult(
        nome="iterativo",
        n=n,
        valor=resultado,
        trace="".join(fita),
        sequencia=seq,
        observacao="Nesta modelagem, o traço coincide com o do monolítico.",
    )


def trace_recursivo(n: int) -> TraceResult:
    """
    Programa recursivo obtido por tradução estrutural do monolítico.

    R1 def (se contador == 0 então R4 senão R2)
    R2 def (faça F; R3)
    R3 def (faça G; R1)
    R4 def ✓

    Esse é o recursivo alinhado com o slide de equivalência:
    ele preserva o mesmo padrão de operações do monolítico.
    """
    if n < 0:
        return entrada_invalida("recursivo", n, "R1")

    fita: List[Symbol] = []
    seq: List[Config] = [("R1", fita_str(fita))]

    def R1(contador: int, resultado: int) -> int:
        if contador == 0:
            seq.append(("R4", fita_str(fita)))
            return resultado

        seq.append(("R2", fita_str(fita)))
        return R2(contador, resultado)

    def R2(contador: int, resultado: int) -> int:
        resultado *= contador
        fita.append("F")
        seq.append(("R3", fita_str(fita)))
        return R3(contador, resultado)

    def R3(contador: int, resultado: int) -> int:
        contador -= 1
        fita.append("G")
        seq.append(("R1", fita_str(fita)))
        return R1(contador, resultado)

    valor = R1(n, 1)

    return TraceResult(
        nome="recursivo",
        n=n,
        valor=valor,
        trace="".join(fita),
        sequencia=seq,
        observacao="Recursivo por tradução estrutural do monolítico.",
    )


def comparar_em_uma_entrada(a: TraceResult, b: TraceResult) -> Dict[str, Any]:
    """
    Compara os resultados apenas para uma entrada n específica.

    Observação:
    - Isso não prova equivalência forte.
    - Apenas mostra se, nesta entrada testada, os programas
      calcularam o mesmo valor e produziram o mesmo traço.
    """
    return {
        "programa_a": a.nome,
        "programa_b": b.nome,
        "mesmo_valor_nesta_entrada": a.valor == b.valor,
        "mesmo_traco_nesta_entrada": a.trace == b.trace,
    }


def demonstracao(n: int) -> str:
    mon = trace_monolitico(n)
    it = trace_iterativo(n)
    rec = trace_recursivo(n)

    comparacoes = [
        comparar_em_uma_entrada(mon, it),
        comparar_em_uma_entrada(mon, rec),
        comparar_em_uma_entrada(it, rec),
    ]

    linhas: List[str] = []
    linhas.append("=" * 78)
    linhas.append(f"MÁQUINA DE TRAÇOS PARA f(n) = n!, com n = {n}")
    linhas.append("=" * 78)
    linhas.append("Observação: a saída principal é o TRAÇO; o valor é só conferência.")

    for r in (mon, it, rec):
        linhas.append(f"\nPrograma {r.nome}")
        linhas.append(f"Valor calculado: {r.valor}")
        linhas.append(f"Traço: {r.trace}")
        linhas.append(f"Sequência: {r.sequencia_formatada()}")
        if r.observacao:
            linhas.append(f"Obs.: {r.observacao}")

    linhas.append("\n" + "-" * 78)
    linhas.append("COMPARAÇÕES NESTA ENTRADA")
    linhas.append("-" * 78)

    for c in comparacoes:
        linhas.append(
            f"{c['programa_a']} x {c['programa_b']}: "
            f"mesmo_valor={c['mesmo_valor_nesta_entrada']}, "
            f"mesmo_traco={c['mesmo_traco_nesta_entrada']}"
        )

    linhas.append("\nLeitura esperada nesta modelagem:")
    linhas.append("- monolítico x iterativo: mesmo traço")
    linhas.append("- monolítico x recursivo: mesmo traço")
    linhas.append("- iterativo x recursivo: mesmo traço")

    return "\n".join(linhas)


if __name__ == "__main__":
    for n in (0, 1, 3, 5):
        print(demonstracao(n))
        print()