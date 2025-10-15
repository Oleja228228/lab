import java.util.Comparator;

public class FoodComparator implements Comparator<Food> {
    @Override
    public int compare(Food f1, Food f2) {
        if (f1 == null || f2 == null) return 0;
        // сортировка по длине названия в ОБРАТНОМ порядке
        return Integer.compare(f2.getName().length(), f1.getName().length());
    }
}
