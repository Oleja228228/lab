public class Apple extends Food implements Nutritious {
    private String size;

    public Apple(String size) {
        super("Яблоко");
        this.size = size;
    }

    @Override
    public void consume() {
        System.out.println(this + " съедено");
    }

    @Override
    public String toString() {
        return super.toString() + " размера '" + size.toUpperCase() + "'";
    }

    @Override
    public boolean equals(Object obj) {
        if (!super.equals(obj)) return false;
        if (!(obj instanceof Apple)) return false;
        return size.equals(((Apple) obj).size);
    }

    @Override
    public float calculateCalories() {
        switch (size.toLowerCase()) {
            case "малое": return 50f;
            case "среднее": return 80f;
            case "большое": return 110f;
            default: return 75f;
        }
    }
}
