import no.vegvesen.nvdbapi.client.clients.ClientFactory;
import no.vegvesen.nvdbapi.client.clients.RoadObjectClient;
import no.vegvesen.nvdbapi.client.model.datakatalog.AttributeType;
import no.vegvesen.nvdbapi.client.model.datakatalog.FeatureType;
import no.vegvesen.nvdbapi.client.model.roadobjects.RoadObject;

import java.io.*;

public class Sorter {
    private static ClientFactory clientFactory;
    private static RoadObjectClient roadObjectClient;

    static void startClient() throws Exception {
        clientFactory = new ClientFactory("https://www.vegvesen.no/nvdb/api/v2", "nvdb-api-client", "ACME");
        roadObjectClient = clientFactory.createRoadObjectClient();
    }

    static void stopClient() throws Exception{
        clientFactory.close();
    }

    String getSearchInfo(){
        //Bredde av felt under x verdi

        //Hvilket felt man ønsker målt

        //Bredde av dekkbredde

        //

        return "";
    }


    static void findRoadObject(int roadTypeId, long attributeTypeId){
        RoadObject roadObject = roadObjectClient.getRoadObject(roadTypeId, attributeTypeId);
        System.out.println(roadObject.getId());
    }

    /**
     * This method writes all roadobject types to a file and all their property types.
     * ===[FeatureTypeID]:FeatureTypeName===
     * [AttributeTypeID]:AttributeTypeName
     * Description: ...
     */
    static void writeRoadObjectsFull(){
        try {
            Writer writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("egenskaper2.txt"), "utf-8"));

            for (FeatureType featureType : roadObjectClient.getDatakatalog().getFeatureTypes()){
                writer.write("\n===[" + featureType.getId() + "]:" + featureType.getName() + "===\n");
                for (AttributeType attributeType : featureType.getAttributeTypes()){
                    writer.write("[" + attributeType.getId() + "]:" + attributeType.getName() + "\nDescription: "
                            + attributeType.getDescription() + "\nTypeDesc:" + attributeType.getType().getDescription()
                            + "\n" + attributeType.isEnum());
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

//    static void printRoadObjects(){
//        for (FeatureType featureType : roadObjectClient.getDatakatalog().getFeatureTypes()){
//            System.out.println("[" + featureType.getId() + "]" + featureType.getName() + "\nDesc: " + featureType.getDescription());
//        }
//    }
//
//    static void printRoadObjectsFull(){
//        for (FeatureType featureType : roadObjectClient.getDatakatalog().getFeatureTypes()){
//            System.out.println("[" + featureType.getId() + "]" + featureType.getName() + "\n\n");
//            for (AttributeType attributeType : featureType.getAttributeTypes()){
//                System.out.println("[" + attributeType.getId() + "]:" + attributeType.getName() + "\nDescription: " + attributeType.getDescription() + "\n");
//            }
//        }
//    }
//
}
