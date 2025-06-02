import java.util.Scanner;

class Main{

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        System.out.println("Enter The IUPAC Compound: ");
        String compoundName = sc.nextLine();
        System.out.println();

        Compound compound = new Compound(compoundName);
        compound.printCompound();
        compound.findBasicTopology();
        compound.calculateAndPrintABCIndex();

        sc.close();

    }

}