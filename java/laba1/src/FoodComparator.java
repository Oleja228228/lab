import java.util.Comparator;

public class FoodComparator implements Comparator<Food> {
    @Override
    public int compare(Food f1, Food f2) {
        if (f1 == null || f2 == null) return 0;
        int nameCompare = f1.getName().compareToIgnoreCase(f2.getName());
        if (nameCompare != 0) return nameCompare;

        // Если объекты питательные — сравним по калориям
        if (f1 instanceof Nutritious && f2 instanceof Nutritious) {
            float diff = ((Nutritious) f1).calculateCalories() - ((Nutritious) f2).calculateCalories();
            return diff > 0 ? 1 : (diff < 0 ? -1 : 0);
        }
        return 0;
    }
}
