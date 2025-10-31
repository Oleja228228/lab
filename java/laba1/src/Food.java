public abstract class Food implements Consumable{
    protected String name;

    public Food(String name){
        this.name = name;
    }

    public String getName(){
        return name;
    }

    public void setName(String name){
        this.name = name;
    }

    @Override
    public String toString(){
        return name;
    }

    @Override
    public boolean equals(Object obj){
        if(!(obj instanceof Food)) return false;

        Food other = (Food) obj;

        if ( this.name == null || other.name == null) return false;

        return this.name.equals(other.name);
    }
}
