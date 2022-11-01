import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class Graph {
    private ArrayList<String> nodes;
    private HashMap<String, ArrayList<String>> adjacencyHash = new HashMap<>();

    public Graph(ArrayList<String> nodes){
        this.nodes = nodes;
    }

    private void addEdge(String a, String b){
        try{
            if (!this.adjacencyHash.get(a).isEmpty()) {
                ArrayList<String> edgesUpdated = this.adjacencyHash.get(a);
                edgesUpdated.add(b);
                this.adjacencyHash.put(a, edgesUpdated);
            }
        } catch (NullPointerException ne){
            ArrayList<String> newEdge = new ArrayList<>();
            newEdge.add(b);
            this.adjacencyHash.put(a, newEdge);
        }
    }

    public void printAdjacency(){
        for(var entry: this.adjacencyHash.entrySet()){
            System.out.println(entry.getKey() + ":" + entry.getValue());
        }
    }

    private boolean _isReachable(String origin, String target){
        ArrayList<String> visited = new ArrayList<>();
        ArrayList<String> queue = new ArrayList<>();

        // adds source node to visited and queue
        visited.add(origin); queue.add(target);

        while(!queue.isEmpty()) {
            String border = queue.remove(0);
            // border is equal to the target node - happy case :)
            if (border.equals(target)) return true;

            // adds the adjacent of border to the frontier
            if (this.adjacencyHash.get(border) != null) {
                for (String newBorder : this.adjacencyHash.get(border)) {
                    // explores only nodes not visited
                    if (!visited.contains(newBorder)) {
                        queue.add(newBorder);
                        visited.add(newBorder);
                    }
                }
            }
        }
        return false;
    }

    public int twoFlavorsIceCream(){
        int numberCombinations = 0;

        // iterates through each source and target node to see if it is reachable
        for(var source: this.adjacencyHash.entrySet()){
            for(var sink: this.adjacencyHash.entrySet()){
                if(!source.getKey().equals(sink.getKey())){
                    if(_isReachable(source.getKey(), sink.getKey())){
                        numberCombinations+=1;
                        System.out.println("Nova combinação: "+ source.getKey() + " -> " + sink.getKey());
                    }
                }
            }
        }
        return numberCombinations;
    }

    public int threeFlavorsIceCream(){
        int numberCombinations = 0;

        // iterates through each source and target node to see if it is reachable
        for(var source: this.adjacencyHash.entrySet()){
            for(var sink: this.adjacencyHash.entrySet()){
                if(!source.getKey().equals(sink.getKey())){
                    if(_isReachable(source.getKey(), sink.getKey())){
                        for(var nextFlavor: this.adjacencyHash.entrySet()) {
                            if(!source.getKey().equals(nextFlavor.getKey()) &&
                                    !sink.getKey().equals(nextFlavor.getKey())){
                                if(_isReachable(sink.getKey(), nextFlavor.getKey())){
                                    numberCombinations+=1;
                                    System.out.println("Nova combinação: "+ source.getKey() + " -> " + sink.getKey() + " -> " + nextFlavor.getKey());
                                }
                            }
                        }
                    }
                }
            }
        }
        return numberCombinations;
    }

    public static Graph createGraphFromFile(String file){
        BufferedReader reader;
        ArrayList<String> new_nodes = new ArrayList<>();
        ArrayList<Tuple<String, String>> new_edges = new ArrayList<>();

        try{
            reader = new BufferedReader(new FileReader(file));
            String line = reader.readLine();
            while(line != null){
                List<String> readFlavors = Arrays.asList(line.split(" -> "));
                if(!new_nodes.contains(readFlavors.get(0))){
                    new_nodes.add(readFlavors.get(0));
                }
                if(!new_nodes.contains(readFlavors.get(1))){
                    new_nodes.add(readFlavors.get(1));
                }


                Tuple<String, String> edge_tuple = new Tuple<>(readFlavors.get(0),
                        readFlavors.get(1));
                new_edges.add(edge_tuple);

                // Reads next line
                line = reader.readLine();
            }
            reader.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        // creating the graph with read nodes
        Graph graph = new Graph(new_nodes);

        // creating the edges between the read nodes
        for (Tuple<String, String> edge:
             new_edges) {
            // for each edge, add to graph
            graph.addEdge(edge.x, edge.y);
        }
        return graph;
    }
}
