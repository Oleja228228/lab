

public class Main {

    public static class Book{
        private String title;
        private String author;
        private boolean isAvailable;

        public Book(String title, String author){
            this.title = title;
            this.author = author;
            isAvailable = true;
        }

        public void takeBook(){
            if(isAvailable){
                System.out.println("You are take book: " + title + " " + author);
                isAvailable = false;
            }else{
                System.out.println("This book is not available");
            }
        }

        public void pullBook(){

        }

    }


    public static void main(String[] args){

    }
}