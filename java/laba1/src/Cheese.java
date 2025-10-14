public class Cheese extends Food implements Nutritious {
    public Cheese() {
        super("Сыр");
    }

    @Override
    public void consume() {
        System.out.println(this + " съеден");
    }

    @Override
    public float calculateCalories() {
        return 350f; // условно
    }
}
