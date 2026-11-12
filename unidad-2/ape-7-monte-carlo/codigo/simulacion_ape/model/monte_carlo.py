"""Los dos modelos Monte Carlo: el círculo inscrito (π) y la suma de dos dados.

Cada función recibe un generador con `next_uniform()` y cuenta aciertos. El estimador
es siempre el mismo: aciertos / N, multiplicado por una constante del modelo.
"""

DICE_TARGET = 7


def inside_circle(u: float, v: float) -> bool:
    """Lleva (u, v) del cuadrado [0,1)² al cuadrado [-1,1)² y revisa si cae en el círculo de radio 1."""
    x = 2.0 * u - 1.0
    y = 2.0 * v - 1.0
    return x * x + y * y <= 1.0


def count_pi_hits(generator, n: int) -> int:
    """Puntos que caen dentro del círculo inscrito (Nc). Cada punto gasta dos uniformes."""
    hits = 0
    for _ in range(n):
        u = generator.next_uniform()
        v = generator.next_uniform()
        if inside_circle(u, v):
            hits += 1
    return hits


def die_face(u: float) -> int:
    """Transformada inversa de la uniforme discreta: D = ⌊6u⌋ + 1, con valores de 1 a 6."""
    return int(6.0 * u) + 1


def count_dice_hits(generator, n: int) -> int:
    """Lanzamientos de dos dados cuya suma es 7. Cada lanzamiento gasta dos uniformes."""
    hits = 0
    for _ in range(n):
        first = die_face(generator.next_uniform())
        second = die_face(generator.next_uniform())
        if first + second == DICE_TARGET:
            hits += 1
    return hits


def dice_sum_counts(generator, n: int) -> dict[int, int]:
    """Cuántas veces salió cada suma (2 a 12) en n lanzamientos."""
    counts = {total: 0 for total in range(2, 13)}
    for _ in range(n):
        counts[die_face(generator.next_uniform()) + die_face(generator.next_uniform())] += 1
    return counts


def dice_sum_probability(total: int) -> float:
    """Probabilidad exacta de cada suma: (6 − |s − 7|) / 36."""
    return (6 - abs(total - 7)) / 36


def sample_points(generator, n: int) -> list[tuple[float, float, bool]]:
    """Primeros n puntos (x, y, dentro) del experimento de π, para dibujarlos."""
    points = []
    for _ in range(n):
        u = generator.next_uniform()
        v = generator.next_uniform()
        points.append((2.0 * u - 1.0, 2.0 * v - 1.0, inside_circle(u, v)))
    return points
