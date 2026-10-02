"""Presentation of results: tables, plots, and console output."""

from .analysis import Summary


def format_summary(summary: Summary) -> str:
    return (
        f"Samples: {summary.samples}\n"
        f"Mean: {summary.mean:.4f}\n"
        f"Std dev: {summary.std_dev:.4f}"
    )
