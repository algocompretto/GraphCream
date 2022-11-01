public class Main {
    public static void main(String[] args) {
        Graph g = Graph.createGraphFromFile("test_cases/casocohen.txt");
        System.out.println("Quantidade de combinações para 2 sabores: " + g.twoFlavorsIceCream());
        System.out.println("Quantidade de combinações para 3 sabores: " + g.threeFlavorsIceCream());
    }
}