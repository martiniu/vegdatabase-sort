import no.vegvesen.nvdbapi.client.clients.ClientFactory;
import no.vegvesen.nvdbapi.client.clients.RoadObjectClient;
import no.vegvesen.nvdbapi.client.model.roadobjects.RoadObject;

public class Sorter {
    public void openDatabase() throws Exception {
        // First, create factory
        ClientFactory factory = new ClientFactory("https://www.vegvesen.no/nvdb/api/v2", "nvdbapi-client", "ACME");
    // Then, create your client. Typically, there's one per root endpoint
        RoadObjectClient client = factory.createRoadObjectClient();

    // Example single object download
        RoadObject ro = client.getRoadObject(534, 1);

    // Remember to close your factory when you're done using it
        factory.close();
    }
}
