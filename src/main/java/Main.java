public class Main {
    public static void main(String[] args){
        try {
            Sorter.useAPI();
            //Sorter.printVegobjekter();
            //Sorter.printVegegenskaper();
            Sorter.skrivVegegenskaper();
        }
        catch (Exception e){
            e.getCause();
        }
    }
}
