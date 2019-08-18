import no.vegvesen.nvdbapi.client.clients.ClientFactory;
import no.vegvesen.nvdbapi.client.clients.RoadObjectClient;
import no.vegvesen.nvdbapi.client.model.datakatalog.DataType;
import no.vegvesen.nvdbapi.client.model.roadobjects.RoadObject;

public class Sorter {
    public static void main(String[] args) {
        Sorter.openDatabase();
    }

    public static void openDatabase() {
        // First, create factory
        ClientFactory factory = new ClientFactory("https://www.vegvesen.no/nvdb/api/v2", "nvdbapi-client", "ACME");
        // Then, create your client. Typically, there's one per root endpoint
        RoadObjectClient client = factory.createRoadObjectClient();

        for (DataType dt : client.getDatakatalog().getDataTypes()) {
            System.out.println("[" +dt.getId() + "]: " + dt.getName() + " \nDesc: " + dt.getDescription());
        }
        // Example single object download
        // RoadObject ro = client.getRoadObject(534, 1);

        // Remember to close your factory when you're done using it

        try {
            factory.close();
        }
        catch (Exception e){
            e.getCause();
        }
    }
}
