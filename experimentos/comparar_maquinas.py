"""Comparación de tiempos entre la máquina A (Linux) y la máquina B (Windows).

Lee SOLO archivos ya medidos (GLOB-08): las mediciones originales de Linux en
``resultados/linux/`` y las vigentes de Windows en ``resultados/r1`` a ``r4``.
No vuelve a medir. Genera ``resultados/comparacion/``:

- ``tiempos.csv``: una fila por medición presente en ambas máquinas, con las dos
  medianas, la razón Windows/Linux, si la entrada es idéntica (misma huella del
  arnés) y si la medición es comparable.
- ``resumen.md``: razón Windows/Linux por requerimiento (mediana, mínimo y
  máximo sobre las mediciones comparables) y comprobación de que los
  resultados lógicos coinciden (V y E, vértices de la envolvente, mayor k).

Criterio de comparabilidad: el catálogo corregido (A13, F01, F03) cambia la
entrada de algunas mediciones de R2. Esas se excluyen. En R4 se conservan
todas: fuerza bruta recorre siempre las (k)! permutaciones, Held-Karp llena
siempre las k·2^k entradas de su tabla y el voraz hace siempre k² comparaciones,
así que su trabajo depende de k y no de los valores de la matriz.

Uso: python experimentos/comparar_maquinas.py
"""
import csv
import json
import statistics
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
LINUX = RAIZ / "resultados" / "linux"
VIGENTE = RAIZ / "resultados"
SALIDA = RAIZ / "resultados" / "comparacion"
CORREGIDOS = ("A13", "F01", "F03")

ARCHIVOS = (
    ("R1", "r1/t_componente.csv"),
    ("R2", "r2/mediciones.csv"),
    ("R3", "r3/mediciones.csv"),
    ("R4", "r4/curva_exactos.csv"),
    ("R4", "r4/calidad_exactos.csv"),
)


def leer(path):
    csv.field_size_limit(2**31 - 1)
    with open(path, newline="", encoding="utf-8") as fh:
        return {f["id_medicion"]: f for f in csv.DictReader(fh)}


def mediana(fila):
    return float(fila["mediana_ms"]) if fila["mediana_ms"] else None


def comparable(req, id_medicion):
    if req != "R2":
        return True
    partes = id_medicion.split(":")
    return not any(lugar in CORREGIDOS for lugar in partes[1:3 if partes[0] == "par" else 2])


def maquina(filas):
    m = json.loads(next(iter(filas.values()))["maquina"])
    return f"{m['sistema']} {m['version_so']}, Python {m['python']}, {m['ram_mb']} MB"


def comprobar_logica(lin, win):
    """Resultados que no dependen de la máquina: deben coincidir."""
    avisos = []
    for clave in ("V", "E", "V_comp", "E_comp"):
        for mid in lin["R1"]:
            a = json.loads(lin["R1"][mid]["info"])[clave]
            b = json.loads(win["R1"][mid]["info"])[clave]
            if a != b:
                avisos.append(f"R1 {mid}: {clave} {a} != {b}")
    for mid in lin["R3"]:
        a = json.loads(lin["R3"][mid]["info"])["vertices"]
        b = json.loads(win["R3"][mid]["info"])["vertices"]
        if a != b:
            avisos.append(f"R3 {mid}: vértices {a} != {b}")
    for nombre, filas in (("Linux", lin["R4c"]), ("Windows", win["R4c"])):
        for metodo in ("fuerza_bruta", "held_karp"):
            ks = [int(m.split("=")[1].split(":")[0]) for m, f in filas.items()
                  if metodo in m and f["estado"] == "ok"]
            avisos.append(f"info: {nombre} {metodo} mayor k completado = {max(ks)}")
    return avisos


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    filas_salida = []
    lin_todo, win_todo = {}, {}
    for req, rel in ARCHIVOS:
        lin, win = leer(LINUX / rel), leer(VIGENTE / rel)
        clave = "R4c" if "curva" in rel else ("R4q" if "calidad" in rel else req)
        lin_todo[clave], win_todo[clave] = lin, win
        for mid in lin:
            if mid not in win:
                continue
            a, b = mediana(lin[mid]), mediana(win[mid])
            misma = lin[mid]["huella_entrada"] == win[mid]["huella_entrada"]
            filas_salida.append({
                "requerimiento": req, "medicion": mid,
                "linux_ms": f"{a:.3f}" if a is not None else "",
                "windows_ms": f"{b:.3f}" if b is not None else "",
                "razon_windows_linux": f"{b / a:.3f}" if a and b else "",
                "misma_entrada": "si" if misma else "no",
                "comparable": "si" if comparable(req, mid) and a and b else "no",
            })
    with open(SALIDA / "tiempos.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas_salida[0]))
        w.writeheader()
        w.writerows(filas_salida)

    lineas = ["# Comparación de tiempos: máquina B (Windows) frente a máquina A (Linux)", "",
              f"- Máquina A: {maquina(lin_todo['R1'])}",
              f"- Máquina B: {maquina(win_todo['R1'])}", "",
              "Razón = mediana en Windows ÷ mediana en Linux (mayor que 1: Windows más lento).", "",
              "| Requerimiento | Mediciones comparables | Excluidas | Razón mediana | Mínima | Máxima |",
              "|---|---|---|---|---|---|"]
    for req in ("R1", "R2", "R3", "R4"):
        del_req = [f for f in filas_salida if f["requerimiento"] == req]
        ok = [float(f["razon_windows_linux"]) for f in del_req if f["comparable"] == "si"]
        lineas.append(f"| {req} | {len(ok)} | {len(del_req) - len(ok)} | "
                      f"{statistics.median(ok):.2f} | {min(ok):.2f} | {max(ok):.2f} |")
    lineas += ["", "## Resultados lógicos (no dependen de la máquina)", ""]
    avisos = comprobar_logica(lin_todo, win_todo)
    errores = [a for a in avisos if not a.startswith("info:")]
    lineas += [f"- {a.removeprefix('info: ')}" for a in avisos if a.startswith("info:")]
    lineas.append("- V y E de R1 y vértices de R3: " + ("idénticos en ambas máquinas" if not errores
                                                        else "DIFERENCIAS: " + "; ".join(errores)))
    lineas += ["", ("Generado por `experimentos/comparar_maquinas.py` desde "
                    "`resultados/linux/` y `resultados/r1`–`r4`.")]
    (SALIDA / "resumen.md").write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(lineas))
    if errores:
        raise SystemExit("hay diferencias en resultados lógicos")


if __name__ == "__main__":
    main()