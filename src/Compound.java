import java.util.*;

/*
 * The following class will represent the organic compound whose IUPAC name is input.
 * We consider the skeleton (biggest carbon chain) of the organic compound to be an array of elements
 * In the following comments, the biggest carbon chain would be referred to as 'skeleton'.
 */

public class Compound {

    String compoundIUPACName; // IUPAC name of the compound
    Element[] compound; // element array that represents the skeleton of the compound

    Compound(String compoundIUPACName) {
        this.compoundIUPACName = compoundIUPACName.toLowerCase();
        getOrganicCompound();
    }

    void getOrganicCompound() {

        System.out.println("The Given IUPAC Name is: "+ compoundIUPACName);

        // we get the name of the alkane to specify the skeleton size
        String prefix = Helper.getAlkaneName(compoundIUPACName);
        switch (prefix) {
            case "methane":
                constructSkeleton(1);
                break;
            case "ethane":
                constructSkeleton(2);
                break;
            case "propane":
                constructSkeleton(3);
                break;
            case "butane":
                constructSkeleton(4);
                break;
            case "pentane":
                constructSkeleton(5);
                break;
            case "hexane":
                constructSkeleton(6);
                break;
            case "heptane":
                constructSkeleton(7);
                break;
            case "octane":
                constructSkeleton(8);
                break;
            case "nonane":
                constructSkeleton(9);
                break;
            case "decane":
                constructSkeleton(10);
                break;
        }

        // function call to insert substituents onto the skeleton after construction of the skeleton
        insertSubstituents();

    }

    // function to construct the skeleton
    void constructSkeleton(int skeletonSize) {

        // allocate space for the skeleton, which is an array of elements
        compound = new Element[skeletonSize];

        /*
         * NOTES
         * 1. since we only construct the skeleton in this function,
         *    we by default connect all carbons in the chain to hydrogen
         * 2. Each carbon can have maximum of 4 connections,
         *    hence arrays of elements that represent connections will have size of 4
         */

        // we firstly give the 4 connections of the first carbon

        // we first give the first 3 connections for the first carbon in the chain
        Element[] startChainConnections = new Element[4];
        for(int i = 0; i < 3; i++) {
            startChainConnections[i] = new Element("H", 1);
        }

        // we initialize the first element of the chain with a carbon whose valency is 4
        if(compound[0] == null) {
            compound[0] = new Element("C", 4);
        }

        // if the given skeleton size is 1, then that would mean there would only be 1 carbon in the chain
        if(skeletonSize == 1) {
            // therefore even the 4th connection of the first carbon would also the hydrogen by default
            startChainConnections[3] = new Element("H", 1);
            compound[0].setConnections(startChainConnections); // set the connections of the only carbon
            // since all connections of the only carbon are filled, we exit from this function
            return;
        }
        // if the given skeleton size is not 1, then that would mean there would be more than 1 carbon in the chain
        else {
            // therefore the 4th connection of the first carbon would be the 2nd carbon in the chain
            if(compound[1] == null) {
                compound[1] = new Element("C", 4); // initialize second carbon
            }
            startChainConnections[3] = compound[1]; // set the 4th connection of first carbon as 2nd carbon
            compound[0].setConnections(startChainConnections); // set the connections of the first carbon
        }

        // we secondly give the 4 connections of the last carbon
        Element[] endChainConnections = new Element[4];
        // since the first connection of the last carbon would be the 2nd last carbon,
        // we initialize the second last carbon
        if(compound[compound.length - 2] == null)
            compound[compound.length - 2] = new Element("C", 4);
        endChainConnections[0] = compound[compound.length - 2]; // first connection is set as the 2nd last carbon

        // we give the rest of the 3 connections of the last carbon as hydrogen
        for(int i = 1; i < 4; i++) {
            endChainConnections[i] = new Element("H", 1);
        }

        // we initialize the last carbon
        if(compound[compound.length - 1] == null)
            compound[compound.length - 1] = new Element("C", 4);
        compound[compound.length - 1].setConnections(endChainConnections); // and set its connections

        // if the skeleton size is less than or equal to 2, then
        // the code written before this point would have successfully initialized all connections for
        // all carbon in the skeleton
        // thus we only continue if skeleton size is greater than 2
        if(skeletonSize > 2) {
            // we thirdly give the connections for the rest of the carbons that lie in the middle of the chain
            for (int i = 1; i < compound.length - 1; i++) {
                // if the ith carbon has not been initialized, we initialize it
                if (compound[i] == null) {
                    compound[i] = new Element("C", 4);
                }
                // same goes for (i + 1)th carbon
                if (compound[i + 1] == null && i + 1 < compound.length) {
                    compound[i + 1] = new Element("C", 4);
                }

                // allocate space for the connections of the carbon that lies in the middle
                Element[] midChainConnections = new Element[4];
                midChainConnections[0] = compound[i - 1]; // first connection would be the carbon that lies to the left
                midChainConnections[3] = compound[i + 1]; // fourth connection would be the carbon that lies to the right
                // second and third connections would just be hydrogen by default
                midChainConnections[1] = new Element("H", 1);
                midChainConnections[2] = new Element("H", 1);

                // set connection for the ith carbon
                compound[i].setConnections(midChainConnections);
            }
        }

    }

    /*
     * function to insert various substituents given in the IUPAC name to the skeleton,
     * which before the call of this function would only contain hydrogen as connections for all carbon
     * in the skeleton
     * */
    public void insertSubstituents() {

        // we start of by extracting the substituent names and positions from the IUPAC name
        // and storing it in a dictionary / map

        /*
         * NOTE: the use of only the LinkedHashMap is not necessary
         *       as any ordered mapping datastructures like a dictionary can be used
         */
        LinkedHashMap<String, List<Integer>> substituents = Helper.preprocessSubstituents(compoundIUPACName);
        System.out.println("The Substituents are : " + substituents);

        // we iterate through each substituent in the map
        for (Map.Entry<String, List<Integer>> entry : substituents.entrySet()) {
            String substituentName = entry.getKey(); // get the name of the substituent

            // get the symbol and valency of the substituents as a pair
            Pair symbolValency = Helper.elementReferenceMap.get(substituentName);

            // collect the positions of the substituent
            // eg: in 1,2-Dichloroethane, [1, 2] are the positions
            List<Integer> positions = entry.getValue();

            // we iterate through each of the positions
            for (Integer position : positions) {
                // we subtract the position number by 1 as positions are 1 indexed in IUPAC names
                Element ithCarbon = compound[position - 1]; // get the carbon at given position

                int numSubstitutionsLeft;

                if(Helper.isElement(substituentName)) {
                    // 'numSubstitutionsLeft' basically refers to "number of hydrogen to replace with substituent"
                    // the value of this is equal to the valency of the substituent as the valency of hydrogen is 1
                    // therefore numSubstitutionsLeft = substituentValency / hydrogenValency
                    // = numSubstitutionsLeft = substituentValency
                    numSubstitutionsLeft = symbolValency.valency;
                }
                else {
                    // if the substituent is a compound rather than an element
                    // number of hydrogen to replace substituent with will be equal to 1
                    // because at most the substituent will have 1 bond left to afford to connect with
                    // carbon chain
                    numSubstitutionsLeft = 1;
                }

                // 'numSpotsLeftForSubstitutions' basically refers to "how many hydrogen atoms exist to replace with substituent?"
                // we need this as we assume only hydrogen can be replaced with substituent (may change in the future)
                int numSpotsLeftForSubstitutions = 0;

                // we now find the number of hydrogen to find numSpotsLeftForSubstitutions
                Element[] ithConnections = ithCarbon.getConnections(); // get the connections of the ith carbon
                // iterate through the connections of the ith carbon
                for (int j = 0; j < ithCarbon.getConnections().length; j++) {
                    // if connection is a hydrogen, increment numSpotsLeftForSubstitutions
                    if (ithConnections[j].getSymbol().equals("H")) {
                        numSpotsLeftForSubstitutions++;
                    }
                }
                // the substitutions shall only take place if the numSpotsLeftForSubstitutions is greater than
                // or equal to number of substituents we must insert
                if (numSpotsLeftForSubstitutions >= numSubstitutionsLeft) {
                    // if the substituent is not an alkyl
                    if(Helper.isElement(substituentName)) {
                        // we first create the element we want to insert as a substituent
                        Element jthConnection = new Element(symbolValency.symbol, symbolValency.valency);

                        // iterate through the connections of ithCarbon
                        for (int j = 0; j < ithCarbon.getConnections().length; j++) {
                            // if connection is a hydrogen, we substitute it with the substituent
                            if (ithConnections[j].getSymbol().equals("H") && numSubstitutionsLeft > 0) {
                                ithConnections[j] = jthConnection;

                                // the substituent is in turn connected to the ith carbon
                                jthConnection.setConnection(ithCarbon);
                                numSubstitutionsLeft--;
                            }
                        }
                    }
                    // else we attempt to insert an alkyl group as the substituent
                    else {
                        CompoundSubstituent compoundSubstituent = new CompoundSubstituent(substituentName, ithCarbon);
                        // iterate through the connections of ithCarbon
                        for (int j = 0; j < ithCarbon.getConnections().length; j++) {
                            // if connection is a hydrogen, we substitute it with the substituent
                            if (ithConnections[j].getSymbol().equals("H") && numSubstitutionsLeft > 0) {
                                ithConnections[j] = compoundSubstituent.compound[0];
                                numSubstitutionsLeft--;
                            }
                        }
                    }
                }

                // otherwise, we throw a runtime error (may change in the future)
                else {
                    throw new RuntimeException("More Substituents than Space to Insert Them!");
                }
            }
        }

    }

    /*
     * function that finds the topological indexes
     * the computation in written form can be viewed in the read me section of the GitHub repository
     */
    public void findBasicTopology() {

        // we use a search algorithm akin to breadth first search (BFS)
        // where we start the search from the first carbon in the skeleton

        // hash set to prevent visiting already visited elements by tracking the visited elements
        Set<Element> visited = new HashSet<>();

        // frequencies of valency pair will be stored in this hash map
        // key is the list of the two valencies of the pair
        // key is the frequency of those valency pairs
        HashMap<List<Integer>, Integer> frequencies = new HashMap<>();

        // traverse the entire compound including substituents to find topological indexes
        Topology.traverseAndUpdateBasicTopology(compound[0], visited, frequencies);

        System.out.println("The Valency Pair Frequencies are : " + frequencies);

    }

    /*
     * function to print out the compound along with main carbons, substituents and all connections
     * we approach this problem using the same traversal method we used to find the topological indexes
     */
    public void printCompound() {

        // traverse the compound form the first main carbon in the skeleton
        // hash set is for keeping track of the visited carbons to not visit them again later
        // depth is defined as "how many carbons away are we from the main skeleton"
        // which is equal to 0 at start of traversal
        traverseAndPrint(compound[0], 0, new HashSet<>());

    }
    private void traverseAndPrint(Element currentElement, int depth, Set<Element> visited) {

        // print tabs to illustrate the depth we have travelled
        Helper.printTabs(depth);

        // print out the current carbon and get ready to print its connections
        System.out.print(currentElement.getSymbol() + "[ ");

        // a queue to store the carbons that must be visited next
        Queue<Element> toVisitCarbons = new LinkedList<>();

        visited.add(currentElement); // add the current carbon to visited hash map

        // iterate through each connection of the current carbon
        for(int i = 0; i < currentElement.getConnections().length; i++) {
            Element ithConnection = currentElement.getConnections()[i];
            if(ithConnection != null) {
                // if the ith connection is a carbon, add it to the queue to visit it later
                if(Objects.equals(ithConnection.getSymbol(), "C")) {
                    toVisitCarbons.offer(ithConnection);
                }

                // print out the ith connection
                System.out.print(ithConnection.getSymbol() + ", ");
            }
        }
        System.out.println("] \n"); // all connections of the current carbon are printed

        // now we visit all carbons that is connected to the current carbon
        // if and only if the carbon is not already visited
        while(!toVisitCarbons.isEmpty()) {
            Element nextCarbon = toVisitCarbons.poll();
            if(!visited.contains(nextCarbon)) {
                // if the next carbon to visit is not part of the main skeleton
                // then it's depth is incremented by 1
                if(!Helper.containsElement(compound, nextCarbon)) {
                    traverseAndPrint(nextCarbon, depth + 1, visited);
                }

                // else the depth does not change
                else {
                    traverseAndPrint(nextCarbon, depth, visited);
                }
            }
        }

    }

    /*
        function that calculates and prints the ABC (Atom Bond Connectivity) index of the current compound
    */
    public void calculateAndPrintABCIndex() {
        double abcIndex = Topology.calculateABCIndex(compound);
        System.out.println("ABC Index: " + abcIndex);
    }

}