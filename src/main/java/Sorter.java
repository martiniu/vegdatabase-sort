import no.vegvesen.nvdbapi.client.clients.ClientFactory;
import no.vegvesen.nvdbapi.client.clients.RoadObjectClient;
import no.vegvesen.nvdbapi.client.model.datakatalog.AttributeType;
import no.vegvesen.nvdbapi.client.model.datakatalog.DataType;
import no.vegvesen.nvdbapi.client.model.datakatalog.FeatureType;
import no.vegvesen.nvdbapi.client.model.roadobjects.Attribute;
import no.vegvesen.nvdbapi.client.model.roadobjects.RoadObject;

import java.io.*;
import java.util.Scanner;

public class Sorter {
    private static ClientFactory clientFactory;
    private static RoadObjectClient roadObjectClient;

    static void useAPI() throws Exception{
        clientFactory = new ClientFactory("https://www.vegvesen.no/nvdb/api/v2", "nvdbapi-client", "ACME");
        roadObjectClient = clientFactory.createRoadObjectClient();

        clientFactory.close();
    }

    static void printVegobjekter(){
        for (FeatureType featureType : roadObjectClient.getDatakatalog().getFeatureTypes()){
            System.out.println("[" + featureType.getId() + "]" + featureType.getName() + "\nDesc: " + featureType.getDescription());
        }
    }

    static void printVegegenskaper(){
        for (FeatureType featureType : roadObjectClient.getDatakatalog().getFeatureTypes()){
            System.out.println("[" + featureType.getId() + "]" + featureType.getName() + "\n\n");
            for (AttributeType attributeType : featureType.getAttributeTypes()){
                System.out.println("[" + attributeType.getId() + "]:" + attributeType.getName() + "\nDescription: " + attributeType.getDescription() + "\n");
            }
        }
    }

    static void skrivVegegenskaper(){
        try {
            Writer writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("egenskaper.txt"), "utf-8"));

            for (FeatureType featureType : roadObjectClient.getDatakatalog().getFeatureTypes()){
                writer.write("\n===[" + featureType.getId() + "]:" + featureType.getName() + "===\n");
                for (AttributeType attributeType : featureType.getAttributeTypes()){
                    writer.write("[" + attributeType.getId() + "]:" + attributeType.getName() + "\nDescription: " + attributeType.getDescription() + "\n");
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
        } catch (Exception e){
            e.printStackTrace();
        }


    }

}
