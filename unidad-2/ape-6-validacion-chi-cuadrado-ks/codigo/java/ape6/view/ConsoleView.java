package ape6.view;

import ape6.model.UniformityTests.ChiSquareResult;
import ape6.model.UniformityTests.KsResult;

/** Vista: imprime resultados ya calculados, una línea clave=valor que lee el programa Python. */
public final class ConsoleView {

    private ConsoleView() {
    }

    public static void showStates(long[] states) {
        StringBuilder out = new StringBuilder();
        for (long x : states) {
            out.append(x).append('\n');
        }
        System.out.print(out);
    }

    public static void showResults(ChiSquareResult chi, KsResult ks, double seconds) {
        StringBuilder observed = new StringBuilder();
        for (int i = 0; i < chi.observed().length; i++) {
            observed.append(i == 0 ? "" : ",").append(chi.observed()[i]);
        }
        System.out.println("observadas=" + observed);
        System.out.println("chi2=" + chi.statistic());
        System.out.println("gl=" + chi.df());
        System.out.println("p_chi2=" + chi.pValue());
        System.out.println("d_mas=" + ks.dPlus());
        System.out.println("d_menos=" + ks.dMinus());
        System.out.println("d=" + ks.statistic());
        System.out.println("p_ks=" + ks.pValue());
        System.out.println("tiempo_s=" + seconds);
    }
}
