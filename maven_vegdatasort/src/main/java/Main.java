public class Main {
    public static void main(String[] args) {
        try {
            InfoCollectorNVDB.startClient();
            InfoCollectorNVDB.writeRoadObjectsFull();
            InfoCollectorNVDB.stopClient();
        } catch (Exception e) {
            e.getStackTrace();
        }
    }
}
