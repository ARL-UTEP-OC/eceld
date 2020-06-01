import java.io.*;
import java.util.*;
import java.text.*;

public class AuditdToJSON{
    static long numItems = 0;
 public static void main(String args[]) {
  try {
   if (args.length != 2)
   {
    System.out.println("Usage: java KeysToJSON <filename> <output-directory>");
    System.exit(-1);
   }
   System.out.println("Parsing auditd data");
   String answer = "[\n";
   String filename = args[0];
   String outputPath = args[1];

   //sample: {\"content\" :\"<2 p/s\", \"className\" :\"traffic\", \"title\" : \"eth:ipv6:udp:dhcpv6\" \n', \"start\" : \"Wed Oct 08 10:56:33 EDT 2014\"},

   FileReader fr = new FileReader(filename);
   //System.out.println("RUNNING with " + filename);
   BufferedReader br = new BufferedReader(fr);
   String line;
   String parsedLine[];

   String timestamp;
   String uid;
   String sid;
   String tty;
   String command;
   String loggerType;
   String temp;
   long lineNum = 0;

//check if we have another line to read
   line = br.readLine();
   while (line != null) {
	//  System.out.println("Processing line: " + line);
	 parsedLine = line.split(" ");


	  line = br.readLine();
  }
//   System.out.println(answer + "\n]");
  System.out.println("\tFinished processing auditd data");
  br.close();
  answer += "\n]\n";
        FileOutput.WriteToFile(outputPath + "/auditdData.JSON", answer);
        // System.out.println(answer);
  }
  catch (FileNotFoundException e) {
   System.out.println("\tNo auditd file exists.");
  }
  catch (Exception e) {
   e.printStackTrace();
  }
 }
 /**
 * Code adapted from Jettison JSONObject open source software:
 * http://grepcode.com/file/repo1.maven.org/maven2/org.codehaus.jettison/jettison/1.3.3/org/codehaus/jettison/json/JSONObject.java#JSONObject
 */
 public static String quote(String string) {
         if (string == null || string.length() == 0) {
             return "";
         }

         char         c = 0;
         int          i;
         int          len = string.length();
         StringBuilder sb = new StringBuilder(len + 4);
         String       t;

         //sb.append('"');
         for (i = 0; i < len; i += 1) {
             c = string.charAt(i);
             switch (c) {
             case '\\':
             case '"':
                 sb.append('\\');
                 sb.append(c);
                 break;
             case '/':
 //                if (b == '<') {
                     sb.append('\\');
 //                }
                 sb.append(c);
                 break;
             case '\b':
                 sb.append("\\b");
                 break;
             case '\t':
                 sb.append("\\t");
                 break;
             case '\n':
                 sb.append("\\n");
                 break;
             case '\f':
                 sb.append("\\f");
                 break;
             case '\r':
                sb.append("\\r");
                break;
             default:
                 if (c < ' ') {
                     t = "000" + Integer.toHexString(c);
                     sb.append("\\u" + t.substring(t.length() - 4));
                 } else {
                     sb.append(c);
                 }
             }
         }
         //sb.append('"');
         return sb.toString();
     }

     public static String removeOffsetTime(String timestamp)
     {
        String answer;
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssZ");
        try
        {
            Date myFormattedDate = sdf.parse(timestamp);
            SimpleDateFormat toFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
            toFormat.setTimeZone(TimeZone.getTimeZone("UTC"));
            //System.out.println("TIME" + toFormat.format(myFormattedDate));
            return toFormat.format(myFormattedDate);
        }catch(ParseException e)
        {
            System.out.println("Error while parsing time in raw auditd file: " + e);
            return "";
        }
     }
}