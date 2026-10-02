"""Vista de consola: formato y salida de los resultados."""

from ..model.analysis import Summary


def format_summary(summary: Summary) -> str:
    return (
        f"Samples: {summary.samples}\n"
        f"Mean: {summary.mean:.4f}\n"
        f"Std dev: {summary.std_dev:.4f}"
    )


def show_summary(summary: Summary) -> None:
    print(format_summary(summary))
