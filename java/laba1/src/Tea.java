public class Tea extends Food implements Nutritious {
    private String type;

    public Tea(String type) {
        super("Чай");
        this.type = type;
    }

    @Override
    public void consume() {
        System.out.println(this + " выпит");
    }

    @Override
    public String toString() {
        return super.toString() + " типа '" + type.toUpperCase() + "'";
    }

    @Override
    public boolean equals(Object obj) {
        if (!super.equals(obj)) return false;
        if (!(obj instanceof Tea)) return false;
        return type.equals(((Tea) obj).type);
    }

    @Override
    public float calculateCalories() {
        switch (type.toLowerCase()) {
            case "чёрный": return 5f;
            case "зелёный": return 2f;
            case "травяной": return 3f;
            default: return 4f;
        }
    }
}
