import java.util.*;

/*
    Class that finds different topological indexes
    basic topology -> frequency of valency pair
    ABC index -> sum over all edges(sqrt((du + dv - 2) / (du * dv))) where du and dv represent the degree of the vertices u, v of edge
*/

public class Topology {

    public static void traverseAndUpdateBasicTopology(Element currentElement, Set<Element> visited, HashMap<List<Integer>, Integer> frequencies) {

        visited.add(currentElement); // add the current carbon to visited hash map

        // a queue to store the carbons that must be visited next
        Queue<Element> toVisitCarbons = new LinkedList<>();

        Element[] connections = currentElement.getConnections(); // get all connections of current carbon

        // iterate through connections
        for (Element ithConnection : connections) {
            if (ithConnection != null) {
                // if the connection is a carbon, we append it to the queue to visit it later
                if (Objects.equals(ithConnection.getSymbol(), "C")) {
                    toVisitCarbons.offer(ithConnection);
                }

                // create a list of max size 2
                List<Integer> elementValencies = new ArrayList<>(2);

                /*
                 * NOTE
                 * valency pairs go both way, for example let us consider a bond C-H
                 * valency of carbon is 4 and valency of hydrogen is 1
                 * so two pairs can be produced from this bond alone which are as follows:
                 * pair1 = (4, 1) [valency of carbon, valency of hydrogen]
                 * pair2 = (1, 4) [valency of hydrogen, valency of carbon]
                 * thus, order of the valency matters
                 * however a pair of (1, 4) made from connection between chlorine and carbon and
                 * a pair of (1, 4) made from connection between hydrogen and carbon are equivalent
                 *
                 * the above stated rules apply for all bonds
                 */

                // place the carbon's valency and connection's valency and increment its frequency in the hashmap
                elementValencies.add(currentElement.getValency());
                elementValencies.add(ithConnection.getValency());
                Helper.incrementFrequency(frequencies, elementValencies);

                // place the valencies in reverse and increment its frequency in the hashmap
                elementValencies.set(0, ithConnection.getValency());
                elementValencies.set(1, currentElement.getValency());
                Helper.incrementFrequency(frequencies, elementValencies);
            }
        }

        // now we visit all carbons that is connected to the current carbon
        // if and only if the carbon is not already visited
        while(!toVisitCarbons.isEmpty()) {
            Element nextCarbon = toVisitCarbons.poll();
            if(!visited.contains(nextCarbon)) {
                traverseAndUpdateBasicTopology(nextCarbon, visited, frequencies);
            }
        }

    }


    /*
     * function to calculate the ABC (Atom-Bond Connectivity) index for the given compound.
     */
    public static double calculateABCIndex(Element[] compound) {

        // since abc index is a sum, we start the sum value at 0 for the result to not be biased (0 + number = number)
        double abcIndex = 0.0;

        // we iterate through each carbon of the compound
        for (Element element : compound) {
            Element[] connections = element.getConnections(); // get all the connections of the ith carbon
            int d_v = element.getNumConnections(); // get the degree of the ith carbon (number of connections of the ith carbon)

            // iterate through all connections of the ith carbon
            for (Element connectedElement : connections) {
                if (connectedElement == null) continue; // some connections can be just null, so skip it if it is

                // since we don't want to consider a C-C edge twice, we skip an edge if connection's element is lower than the current carbon,
                // since it is given that the left carbon has a lower ID than the right carbon
                if (connectedElement.getId() < element.getId()) continue;

                // get number of connections (degree) of the connection itself
                int d_w = connectedElement.getNumConnections();

                // if anyone is 0, we don't want to calculate the ABC index for that edge since it would cause a division by 0 error
                if (d_v == 0 || d_w == 0) {
                    System.out.println("Skipping edge with zero valency: " + d_v + ", " + d_w);
                    continue;
                }

                // calculate numerator
                double numerator = d_v + d_w - 2.0;
                // ABC index can't be negative, so if it goes below 0 we skip
                if (numerator < 0) {
                    System.out.println("Skipping edge due to negative numerator: " + d_v + ", " + d_w);
                    continue;
                }

                // find the ABC index for the current edge (term)
                double term = Math.sqrt(numerator / (d_v * d_w));

                // add the term to final result
                abcIndex += term;

            }
        }

        return abcIndex;

    }

}
