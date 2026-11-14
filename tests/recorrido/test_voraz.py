"""Pruebas del vecino más cercano dirigido (R4-10, DA-13)."""
from quindio.recorrido.exactos import held_karp
from quindio.recorrido.voraz import vecino_mas_cercano


def test_R4_10_voraz_visita_todo_y_vuelve():
    m = [
        [0, 2, 9],
        [1, 0, 2],
        [9, 1, 0],
    ]
    tour, total, info = vecino_mas_cercano(m)
    assert tour[0] == tour[-1] == 0
    assert sorted(tour[:-1]) == [0, 1, 2]
    assert total == sum(m[a][b] for a, b in zip(tour, tour[1:]))  # noqa: RUF007 - mismo estilo que el medido
    assert info == {"metodo": "vecino_mas_cercano"}


def test_R4_10_desempate_menor_indice():
    m = [
        [0, 5, 5],
        [5, 0, 1],
        [5, 1, 0],
    ]
    tour, _, _ = vecino_mas_cercano(m)
    assert tour == [0, 1, 2, 0]


def test_R4_10_no_siempre_optimo():
    # El voraz toma lo barato (0->1->2->3) y paga el regreso caro (3->0 = 10).
    # El óptimo va primero a 3 y vuelve barato: 4+1+1+4 = 10 < 13.
    m = [
        [0, 1, 4, 4],
        [4, 0, 1, 4],
        [4, 4, 0, 1],
        [10, 1, 4, 0],
    ]
    tour_v, total_v, _ = vecino_mas_cercano(m)
    _, total_h, _ = held_karp(m)
    assert (tour_v, total_v) == ([0, 1, 2, 3, 0], 13)
    assert total_h == 10  # (sirve de insumo para el ejemplo R4.5)
