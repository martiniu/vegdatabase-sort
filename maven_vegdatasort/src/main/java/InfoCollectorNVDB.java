import no.vegvesen.nvdbapi.client.clients.ClientFactory;
import no.vegvesen.nvdbapi.client.clients.RoadObjectClient;
import no.vegvesen.nvdbapi.client.model.datakatalog.AttributeType;
import no.vegvesen.nvdbapi.client.model.datakatalog.FeatureType;

import java.io.*;

public class InfoCollectorNVDB {

    private static ClientFactory clientFactory;
    private static RoadObjectClient roadObjectClient;

    static void startClient() throws Exception {
        clientFactory = new ClientFactory("https://www.vegvesen.no/nvdb/api/v2", "nvdb-api-client", "ACME");
        roadObjectClient = clientFactory.createRoadObjectClient();
    }

    static void stopClient() throws Exception{
        clientFactory.close();
    }

    /**
     * This method writes all roadobject types to a file and all their attribute types.
     * ===[FeatureTypeID]:FeatureTypeName===
     * [AttributeTypeID]:AttributeTypeName
     * Description: ...
     */
    static void writeRoadObjectsFull(){
        try {
            Writer writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("GitHub/vegdatabase-sort/objectwiki.txt"), "utf-8"));

            for (FeatureType featureType : roadObjectClient.getDatakatalog().getFeatureTypes()){

                writer.write("\n===[" + featureType.getId() + "]:" + featureType.getName() + "===\n");

                for (AttributeType attributeType : featureType.getAttributeTypes()){

                    writer.write("[" + attributeType.getId() + "]:"
                            + attributeType.getName()
                            +  " - " + attributeType.getType().getName() + "\n");

                }
            }
            writer.write("END");
            writer.close();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e){
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
