/*
 * The following class represents all substituents which are made of more than one type of atom.
 * the name 'compound' is misleading as this class would also represent substituents such as
 * NH2 which is a molecule.
 * I was not able to find a better name for this class, so we shall ignore that inconsistency.
 */

/*
 * NOTE:
 * The following class's implementation as of (2nd March 2025) which is the latest date of change only considers
 * pure alkyls as the only form of compound substituents
 * thus continue reading with this in mind
 */

public class CompoundSubstituent {

    String substituentName; // subtituent name of the compound
    Element[] compound; // element array that represents the skeleton of the compound
    Element sourceCarbon; // the carbon to which this substituent will be connected to

    CompoundSubstituent(String substituentName, Element sourceCarbon) {
        this.substituentName = substituentName.toLowerCase();
        this.sourceCarbon = sourceCarbon;
        getOrganicCompoundSubstituent();
    }

    void getOrganicCompoundSubstituent() {

        // we get the name of the alkyl to specify the skeleton size
        String prefix = Helper.getAlkylName(substituentName);
        switch (prefix) {
            case "methyl":
                constructSubstituentSkeleton(1);
                break;
            case "ethyl":
                constructSubstituentSkeleton(2);
                break;
            case "propyl":
                constructSubstituentSkeleton(3);
                break;
            case "butyl":
                constructSubstituentSkeleton(4);
                break;
            case "pentyl":
                constructSubstituentSkeleton(5);
                break;
            case "hexyl":
                constructSubstituentSkeleton(6);
                break;
            case "heptyl":
                constructSubstituentSkeleton(7);
                break;
            case "octyl":
                constructSubstituentSkeleton(8);
                break;
            case "nonyl":
                constructSubstituentSkeleton(9);
                break;
            case "decyl":
                constructSubstituentSkeleton(10);
                break;
        }

    }

    // function to construct the skeleton
    void constructSubstituentSkeleton(int skeletonSize) {

        // allocate space for the skeleton, which is an array of elements
        compound = new Element[skeletonSize];

        /*
         * NOTES
         * 1. since we only construct the skeleton in this function,
         *    we by default connect all carbons in the chain to hydrogen,
         *    except the first carbon which has one of its connections connected to the main chain
         * 2. Each carbon can have maximum of 4 connections,
         *    hence arrays of elements that represent connections will have size of 4
         */

        // we firstly give the 4 connections of the first carbon

        // we first give the first 3 connections for the first carbon in the chain
        Element[] startChainConnections = new Element[4];
        // first connection of the first carbon is the carbon on the main chain to which this substituent will be
        // attached to
        startChainConnections[0] = sourceCarbon;
        // rest of the second and third connections are hydrogen
        startChainConnections[1] = new Element("H", 1);
        startChainConnections[2] = new Element("H", 1);

        // we initialize the first element of the chain with a carbon whose valency is 4
        if(compound[0] == null) {
            compound[0] = new Element("C", 4);
        }

        // if the given skeleton size is 1, then that would mean there would only be 1 carbon in the substituent
        if(skeletonSize == 1) {
            // therefore even the 4th connection of the first carbon would also the hydrogen by default
            startChainConnections[3] = new Element("H", 1); // set the connections of the only carbon
            compound[0].setConnections(startChainConnections);
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
        endChainConnections[1] = new Element("H", 1);
        endChainConnections[2] = new Element("H", 1);
        endChainConnections[3] = new Element("H", 1);

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

}