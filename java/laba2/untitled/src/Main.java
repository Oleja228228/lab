
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

@SuppressWarnings("serial")
class MainFrame extends JFrame {

    private static final int WIDTH = 500;
    private static final int HEIGHT = 350;

    private JTextField textFieldX;
    private JTextField textFieldY;
    private JTextField textFieldZ;
    private JTextField textFieldResult;

    private ButtonGroup radioFormulaGroup = new ButtonGroup();
    private ButtonGroup radioMemoryGroup = new ButtonGroup();

    private int formulaId = 1;
    private int activeMem = 1;

    private Double mem1 = 0.0;
    private Double mem2 = 0.0;
    private Double mem3 = 0.0;

    public MainFrame() {
        super("Вычисление формул — Вариант B4");
        setSize(WIDTH, HEIGHT);
        Toolkit kit = Toolkit.getDefaultToolkit();
        setLocation((kit.getScreenSize().width - WIDTH) / 2,
                (kit.getScreenSize().height - HEIGHT) / 2);

        // Радиокнопки выбора формулы
        Box boxFormula = Box.createHorizontalBox();
        boxFormula.add(Box.createHorizontalGlue());
        addRadioButton("Формула 1", 1, boxFormula, radioFormulaGroup);
        addRadioButton("Формула 2", 2, boxFormula, radioFormulaGroup);
        boxFormula.add(Box.createHorizontalGlue());
        boxFormula.setBorder(BorderFactory.createTitledBorder("Выбор формулы"));

        // Поля ввода X, Y, Z
        Box boxVariables = Box.createHorizontalBox();
        boxVariables.add(new JLabel("X:"));
        textFieldX = new JTextField("0.0", 8);
        boxVariables.add(textFieldX);
        boxVariables.add(Box.createHorizontalStrut(10));
        boxVariables.add(new JLabel("Y:"));
        textFieldY = new JTextField("0.0", 8);
        boxVariables.add(textFieldY);
        boxVariables.add(Box.createHorizontalStrut(10));
        boxVariables.add(new JLabel("Z:"));
        textFieldZ = new JTextField("0.0", 8);
        boxVariables.add(textFieldZ);
        boxVariables.setBorder(BorderFactory.createTitledBorder("Переменные"));

        // Поле вывода результата
        Box boxResult = Box.createHorizontalBox();
        textFieldResult = new JTextField("0.0", 12);
        textFieldResult.setEditable(false);
        boxResult.add(new JLabel("Результат:"));
        boxResult.add(Box.createHorizontalStrut(10));
        boxResult.add(textFieldResult);
        boxResult.setBorder(BorderFactory.createTitledBorder("Результат"));

        // Кнопки MC и M+
        JButton buttonMC = new JButton("MC");
        JButton buttonMPlus = new JButton("M+");
        JButton buttonCalc = new JButton("Вычислить");
        JButton buttonReset = new JButton("Очистить поля");

        Box boxButtons = Box.createHorizontalBox();
        boxButtons.add(buttonCalc);
        boxButtons.add(Box.createHorizontalStrut(10));
        boxButtons.add(buttonReset);
        boxButtons.add(Box.createHorizontalStrut(10));
        boxButtons.add(buttonMC);
        boxButtons.add(Box.createHorizontalStrut(10));
        boxButtons.add(buttonMPlus);
        boxButtons.setBorder(BorderFactory.createTitledBorder("Действия"));

        // Радиокнопки выбора памяти
        Box boxMemory = Box.createHorizontalBox();
        addRadioButton("Переменная 1", 1, boxMemory, radioMemoryGroup);
        addRadioButton("Переменная 2", 2, boxMemory, radioMemoryGroup);
        addRadioButton("Переменная 3", 3, boxMemory, radioMemoryGroup);
        boxMemory.setBorder(BorderFactory.createTitledBorder("Выбор памяти"));

        // Основное расположение
        Box contentBox = Box.createVerticalBox();
        contentBox.add(boxFormula);
        contentBox.add(boxVariables);
        contentBox.add(boxResult);
        contentBox.add(boxMemory);
        contentBox.add(boxButtons);

        getContentPane().add(contentBox, BorderLayout.CENTER);

        // Действие "Вычислить"
        buttonCalc.addActionListener(e -> {
            try {
                double x = Double.parseDouble(textFieldX.getText());
                double y = Double.parseDouble(textFieldY.getText());
                double z = Double.parseDouble(textFieldZ.getText());
                double result = (formulaId == 1) ? formula1(x, y, z) : formula2(x, y, z);
                textFieldResult.setText(String.format("%.5f", result));
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Ошибка ввода чисел!", "Ошибка", JOptionPane.ERROR_MESSAGE);
            }
        });

        // Очистить поля
        buttonReset.addActionListener(e -> {
            textFieldX.setText("0.0");
            textFieldY.setText("0.0");
            textFieldZ.setText("0.0");
            textFieldResult.setText("0.0");
        });

        // Работа с памятью
        buttonMC.addActionListener(e -> {
            setMem(0.0);
            textFieldResult.setText("0.0");
        });

        buttonMPlus.addActionListener(e -> {
            try {
                double value = Double.parseDouble(textFieldResult.getText());
                addToMem(value);
                textFieldResult.setText(getMem().toString());
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Ошибка работы с памятью!");
            }
        });
    }

    private void addRadioButton(String name, int id, Box box, ButtonGroup group) {
        JRadioButton button = new JRadioButton(name, id == 1);
        button.addActionListener(e -> {
            if (group == radioFormulaGroup)
                formulaId = id;
            else
                activeMem = id;
        });
        group.add(button);
        box.add(button);
    }

    // Формулы
    private double formula1(double x, double y, double z) {
        return Math.sin(4 * x + 2 * Math.cos(y) * Math.cos(y)) + Math.log(Math.abs(Math.sin(y)));
    }

    private double formula2(double x, double y, double z) {
        return Math.log10(Math.abs(y * x * x * z)) + Math.tan(y / (x + 2));
    }

    // Работа с памятью
    private Double getMem() {
        return (activeMem == 1) ? mem1 : (activeMem == 2 ? mem2 : mem3);
    }

    private void setMem(Double val) {
        if (activeMem == 1) mem1 = val;
        else if (activeMem == 2) mem2 = val;
        else mem3 = val;
    }

    private void addToMem(Double val) {
        setMem(getMem() + val);
    }

    public static void main(String[] args) {
        MainFrame frame = new MainFrame();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
}
