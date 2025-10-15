import java.util.*;

public class Breakfast {
    public static void main(String[] args) {
        Food[] breakfast = new Food[20];
        int itemsCount = 0;
        boolean calcCalories = false;
        boolean sort = false;

        if (args.length == 0) {
            Scanner scanner = new Scanner(System.in);
            System.out.println("Введите продукты (например: IceCream/карамель, IceCream/шоколад,  -sort -calories).");
            System.out.println("Введите 'end' для завершения ввода.");

            while (itemsCount < breakfast.length) {
                System.out.print("> ");
                String line = scanner.nextLine().trim();
                if (line.equalsIgnoreCase("end")) break;
                if (line.isEmpty()) continue;

                if (line.equals("-calories")) calcCalories = true;
                else if (line.equals("-sort")) sort = true;
                else {
                    Food item = parseFood(line.split("/"));
                    if (item != null) breakfast[itemsCount++] = item;
                }
            }
            scanner.close();
        } else {
            for (String arg : args) {
                if (arg.equals("-calories")) calcCalories = true;
                else if (arg.equals("-sort")) sort = true;
                else {
                    Food item = parseFood(arg.split("/"));
                    if (item != null) breakfast[itemsCount++] = item;
                }
            }
        }

        if (sort) {
            Arrays.sort(breakfast, 0, itemsCount, new FoodComparator());
            System.out.println("\nЗавтрак отсортирован по названию и калорийности.");
        }

        for (int i = 0; i < itemsCount; i++) {
            breakfast[i].consume();
        }

        if (calcCalories) {
            float total = 0;
            for (int i = 0; i < itemsCount; i++) {
                if (breakfast[i] instanceof Nutritious) {
                    total += ((Nutritious) breakfast[i]).calculateCalories();
                }
            }
            System.out.printf("\nОбщая калорийность завтрака: %.2f ккал%n", total);
        }

        System.out.println("Всего хорошего!");
    }

    private static Food parseFood(String[] parts) {
        switch (parts[0].toLowerCase()) {
            case "icecream":
                return new IceCream(parts.length > 1 ? parts[1] : "карамель");
            default:
                System.out.println("Неизвестный продукт: " + parts[0]);
                return null;
        }
    }

}
