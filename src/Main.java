public class Main {
    public static void main(String[] args) {
        // 8 copinhos de 2 sabores e 4 copinhos de 3 sabores
        Graph g = Graph.createGraphFromFile("test_cases/casocohen.txt");
        System.out.println("Quantidade de combinações para 2 sabores: " + g.twoFlavorsIceCream() + "\n\n");
        System.out.println("Quantidade de combinações para 3 sabores: " + g.threeFlavorsIceCream());
    }
}