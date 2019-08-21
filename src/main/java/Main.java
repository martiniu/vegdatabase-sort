public class Main {
    public static void main(String[] args) {
        try {
            Sorter.startClient();
            //Sorter.findRoadObject(583, 86512964);
            Sorter.writeRoadObjectsFull();

            Sorter.stopClient();
        } catch (Exception e) {
            e.getStackTrace();
        }
    }
}
