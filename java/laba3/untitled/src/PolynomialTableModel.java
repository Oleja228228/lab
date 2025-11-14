import javax.swing.table.AbstractTableModel;
import java.util.ArrayList;

public class PolynomialTableModel extends AbstractTableModel {
    private Double[] coefficients;
    private ArrayList<Object[]> data = new ArrayList<>();

    public PolynomialTableModel(Double[] coefficients) {
        this.coefficients = coefficients;
    }

    public void calculate(double from, double to, double step) {
        data.clear();
        for (double x = from; x <= to + 1e-9; x += step) {
            double y = 0.0;
            for (int i = 0; i < coefficients.length; i++) {
                y += coefficients[i] * Math.pow(x, coefficients.length - i - 1);
            }

            double fraction = Math.abs(y) - Math.floor(Math.abs(y));
            // Показываем дробную часть до тысячных в таблице
            double fractionRounded = Math.floor(fraction * 1000.0 + 1e-9) / 1000.0;
            boolean oddFraction = isAnyFractionDigitOdd(fraction, 3); // проверяем первые 3 цифры

            data.add(new Object[]{x, y, fractionRounded, oddFraction});
        }
        fireTableDataChanged();
    }

    /**
     * Возвращает true, если хотя бы одна из первых `digits` цифр дробной части нечётная.
     * Например, fraction=0.25, digits=3 -> проверит 2,5,0 -> 5 нечётная -> true.
     */
    private boolean isAnyFractionDigitOdd(double fraction, int digits) {
        // Надёжно получаем целую последовательность цифр без артефактов округления
        double eps = 1e-9;
        for (int i = 1; i <= digits; i++) {
            int d = (int) Math.floor(fraction * Math.pow(10, i) + eps) % 10;
            if (d % 2 == 1) return true;
        }
        return false;
    }

    @Override
    public int getRowCount() {
        return data.size();
    }

    @Override
    public int getColumnCount() {
        return 4; // X, P(X), дробная часть (до 3 знаков), булево
    }

    @Override
    public String getColumnName(int col) {
        return switch (col) {
            case 0 -> "X";
            case 1 -> "P(X)";
            case 2 -> "Дробная часть";
            case 3 -> "Дробная часть нечётная?";
            default -> "";
        };
    }

    @Override
    public Class<?> getColumnClass(int col) {
        return switch (col) {
            case 0, 1, 2 -> Double.class;
            case 3 -> Boolean.class;
            default -> Object.class;
        };
    }

    @Override
    public Object getValueAt(int row, int col) {
        return data.get(row)[col];
    }
}
