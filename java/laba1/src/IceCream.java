public class IceCream extends Food implements Nutritious {
    private String sirup;

    public IceCream(String sirup) {
        super("Мороженое");
        this.sirup = sirup;
    }

    @Override
    public void consume() {
        System.out.println(this + " съедено");
    }

    @Override
    public String toString() {
        return super.toString() + " с сиропом '" + sirup.toUpperCase() + "'";
    }

    @Override
    public boolean equals(Object obj) {
        if (!super.equals(obj)) return false;
        if (!(obj instanceof IceCream)) return false;
        return sirup.equals(((IceCream) obj).sirup);
    }

    @Override
    public float calculateCalories() {
        switch (sirup.toLowerCase()) {
            case "карамель": return 250f;
            case "шоколад": return 270f;
            default: return 200f;
        }
    }
}
