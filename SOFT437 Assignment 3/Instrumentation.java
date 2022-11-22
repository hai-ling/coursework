// "static void main" must be defined in a public class.
import java.io.*;
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.text.DecimalFormat;
class Instrumentation {
    private static Instrumentation instance = null;
    private String padding = "|   ";
    private boolean onoff = false;
    private Stack<List<Object>> stack = new Stack<List<Object>>();
    private List<String> logs = new ArrayList<>();
    private Instrumentation(){}
    private DecimalFormat format = new DecimalFormat("0.00");
    
    public static Instrumentation Instance(){
        // To ensure only one instance is created
        if (instance == null) {
            instance = new Instrumentation();
        }
        return instance;
    }
    public void activate(boolean x){
        onoff = x;
    }
    
    public void startTiming(String s) {
        if (!onoff){
            return;
        }
        List<Object> pair = new ArrayList<Object>(List.of(s, System.nanoTime()));
        stack.push(pair);
        String log = String.format("STARTTIMING: %s", s);
        logs.add(padding.repeat(stack.size()-1) + log);
    }
    public void stopTiming(String s) {
        if (!onoff){
            return;
        }
        List<Object> pair = stack.pop();
        double elapsedNano = (double)(System.nanoTime()-(long)pair.get(1));
        String elapsedMillis = format.format(elapsedNano/1000000);
        String log = String.format("STOPTIMING: %s %sms", s, elapsedMillis);
        logs.add(padding.repeat(stack.size()) + log);
    }
    
    public void comment(String s){
        if (!onoff){
            return;
        }
        logs.add(padding.repeat(stack.size()) + s);
    }
    
    public void printLog(){
        String result = String.join("\n", logs);
        System.out.println(result);
    }

    public void dump(String filename){
        if (filename == null){
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("ddyyMMhhmmss");
            LocalDateTime localDateTime = LocalDateTime.now();
            filename = "instrumentation"+formatter.format(localDateTime)+".log";
        }


        try {
            String result = String.join("\n", logs);
            FileWriter fw = new FileWriter(new File(filename));
            fw.write(result);
            fw.close();
        }
        catch(Exception e) {
          }

    }
}