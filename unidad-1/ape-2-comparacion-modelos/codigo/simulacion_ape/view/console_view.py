"""Vista de consola: tablas de resultados en texto."""


def show_parameters(label, params):
    print(f"\n{label}")
    print(f"  P0 = {params['P0']:.0f}   r = {params['r']:.4f}   sigma = {params['sigma']:.2f}")


def show_fit_table(table, data):
    names = list(table)
    print(f"\n  {'t':>2}  {'Datos':>8}" + "".join(f"{n:>18}" for n in names))
    for t, observed in enumerate(data):
        row = "".join(f"{table[n]['values'][t]:>18.1f}" for n in names)
        print(f"  {t:>2}  {observed:>8.0f}{row}")
    print(f"  {'RMSE':<12}" + "".join(f"{table[n]['rmse']:>18.1f}" for n in names))


def show_rate_finals(finals):
    print("\nPoblación final (t = 6) según r, modelo determinístico")
    for r, value in finals.items():
        print(f"  r = {r:+.2f}  ->  P(6) = {value:8.1f}")


def show_noise_spread(spreads):
    print("\nModelo estocástico: ancho de la banda 5 %-95 % en t = 6")
    for sigma, width in spreads.items():
        print(f"  sigma = {sigma:>3}  ->  {width:7.1f}")


def show_euler_errors(errors):
    print("\nError de Euler en t = 6 frente a la solución exacta")
    for dt, error in errors.items():
        print(f"  dt = {dt:<5} ->  {error:7.2f}")


def show_figures_saved(directory):
    print(f"\nFiguras guardadas en {directory}/")
