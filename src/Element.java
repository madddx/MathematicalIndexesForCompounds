/*
* Class that represents any given element.
* Fundamental unit for the Compound class and also the operations being performed in and for it.
*/

public class Element {

    private final String symbol; // chemical symbol of the element
    private final int valency; // valency of the element
    private Element[] connections; // elements to which this element is connected to, represented as an array of elements
    private int bondsLeft; // how many more bonds this element can afford for more connections
    private final int elementID; // id of this element (automatically incremented upon creation)

    private static int idCounter = 0; // static counter to track element IDs

    Element(String symbol, int valency) {

        this.symbol = symbol;
        this.valency = valency;
        this.bondsLeft = valency;
        this.connections = new Element[valency];
        this.elementID = ++idCounter;

    }

    @Override
    public String toString() {

        return "Symbol: " + symbol + "\n" + "Valency: " + valency + "\n";

    }

    public Element[] getConnections() {

        return connections;

    }

    // function to set the connections if a connection array is already given
    public void setConnections(Element[] newConnections) {

        this.connections = newConnections; // set the connections
        int i = 0;
        // decrease the bonds left according to the valency of each connection in the connection array
        while(bondsLeft > 0) {
            bondsLeft = bondsLeft - newConnections[i].valency;
        }

    }

    // function to set connection if an element and index for the connection are given
    public void setConnection(int connectionIndex, Element element) {

        connections[connectionIndex] = element;

    }

    // function to set connection fi an element is given
    // element fills whichever null spot is available in the connection array
    public void setConnection(Element element) {

        for(int i = 0; i < connections.length; i++) {
            if(connections[i] == null) {
                connections[i] = element;
                return;
            }
        }

    }

    public String getSymbol() {

        return symbol;

    }

    public int getId() {

        return elementID;

    }

    public int getValency() {

        return valency;

    }

    public int getNumConnections() {

        int numConnections = 0;
        for (Element connection: connections) {
            if (connection != null) {
                numConnections++;
            }
        }

        return numConnections;

    }

}