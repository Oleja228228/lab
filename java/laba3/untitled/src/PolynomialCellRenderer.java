import javax.swing.*;
import javax.swing.table.DefaultTableCellRenderer;
import java.awt.*;

/**
 * Рендерер для таблицы многочлена.
 * - Колонка 1 (индекс 0) — X (обычная белая фон)
 * - Колонка 2 (индекс 1) — P(X): зелёный фон если целая часть чётная, розовый если нечётная
 * - Колонка 3 (индекс 2) — Дробная часть нечётная?: подсвечивается жёлтым, если true
 */
public class PolynomialCellRenderer extends DefaultTableCellRenderer {

    private static final Color GREEN_EVEN = new Color(220, 255, 220);
    private static final Color PINK_ODD   = new Color(255, 220, 220);
    private static final Color YELLOW_TRUE = new Color(255, 255, 180);

    @Override
    public Component getTableCellRendererComponent(JTable table, Object value,
                                                   boolean isSelected, boolean hasFocus,
                                                   int row, int column) {
        // Вызов базовой реализации — она установит текст/чекбокс/выделение и т.д.
        Component cell = super.getTableCellRendererComponent(table, value, isSelected, hasFocus, row, column);

        // Чтобы цвет фона был видимым
        if (cell instanceof JComponent) {
            ((JComponent) cell).setOpaque(true);
        }

        // Если строка выделена — сохраняем стандартный фон выделения
        if (isSelected) {
            cell.setBackground(table.getSelectionBackground());
            cell.setForeground(table.getSelectionForeground());
        } else {
            // Если не выделено — выставляем фон в зависимости от колонки и значения
            switch (column) {
                case 1: // колонка P(X)
                    if (value instanceof Double) {
                        double val = (Double) value;
                        int intPart = (int) Math.floor(Math.abs(val));
                        if (intPart % 2 == 0) {
                            cell.setBackground(GREEN_EVEN);
                        } else {
                            cell.setBackground(PINK_ODD);
                        }
                    } else {
                        cell.setBackground(Color.WHITE);
                    }
                    cell.setForeground(Color.BLACK);
                    break;

                case 2: // колонка "Дробная часть нечётная?"
                    // Обычно value будет Boolean (чекбокс). Если true — подсвечиваем.
                    if (value instanceof Boolean && (Boolean) value) {
                        cell.setBackground(YELLOW_TRUE);
                    } else {
                        cell.setBackground(Color.WHITE);
                    }
                    cell.setForeground(Color.BLACK);
                    break;

                default: // остальные колонки
                    cell.setBackground(Color.WHITE);
                    cell.setForeground(Color.BLACK);
                    break;
            }
        }

        // Центрирование текста / содержимого
        setHorizontalAlignment(SwingConstants.CENTER);

        return cell;
    }
}
