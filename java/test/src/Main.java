import java.util.Scanner;
import java.util.ArrayList;
import java.util.Collections;

public class Main {

    static class Student implements Comparable<Student> {
        private String name;
        private int age;
        private double grade;
        private static int countStudents = 0;

        public Student(String name, int age, double grade) {
            this.name = name;
            this.age = age;
            this.grade = grade;
            countStudents++;
        }

        public void printInfo() {
            System.out.println("Name: " + name + ", Age: " + age + ", Grade: " + grade);
        }

        public double getGrade() {
            return grade;
        }

        public boolean isAdult() {
            return age >= 18;
        }

        public static int getCountStudents() {
            return countStudents;
        }

        // Реализация Comparable для сортировки по убыванию оценки
        @Override
        public int compareTo(Student other) {
            return Double.compare(other.grade, this.grade); // убывание
        }
    }

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        ArrayList<Student> students = new ArrayList<>();
        String answer;

        // Ввод студентов
        do {
            System.out.print("Write your name: ");
            String name = in.nextLine();

            System.out.print("Write your age: ");
            int age = in.nextInt();
            in.nextLine(); // очищаем буфер

            System.out.print("Write your grade: ");
            double grade = in.nextDouble();
            in.nextLine(); // очищаем буфер

            students.add(new Student(name, age, grade));

            System.out.print("Add another student? (yes/no): ");
            answer = in.nextLine();
        } while(answer.equalsIgnoreCase("yes"));

        // Сортировка студентов по убыванию оценки
        Collections.sort(students);

        // Вывод студентов после сортировки
        System.out.println("\n--- Students sorted by grade (highest first) ---");
        for(Student s : students) {
            s.printInfo();
        }

        // Студент с наивысшей оценкой
        if(!students.isEmpty()) {
            System.out.println("\nStudent with highest grade:");
            students.get(0).printInfo();
        }
    }
}
