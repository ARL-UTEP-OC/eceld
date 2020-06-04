import java.io.*;
import java.util.*;
import java.text.*;
import java.util.HashMap;

public class AuditdToJSON{
    static long numItems = 0;
 public static void main(String args[]) {
  try {
   if (args.length != 2)
   {
    System.out.println("Usage: java KeysToJSON <filename> <output-directory>");
    System.exit(-1);
   }
   //sample: {"auditd_id" : 0, "content" : "\"find\" \"\/\" \"-name\" \"3120322033\"", "className" : "auditd", "start" : "2020-06-03T17:49:39"},
   // File processing variables
   String filename = args[0];
   String outputPath = args[1];
   FileReader fr = new FileReader(filename);
   BufferedReader br = new BufferedReader(fr);
   String line;
   String answer = "[\n";

   // Field Parser variables
   HashMap<String, String> holderSyscall = new HashMap<String, String>();
   HashMap<String, String> holderExecve = new HashMap<String, String>();
   String[] syscallKeyVals = null;
   String[] execveKeyVals = null;

   // Fields
   String comm = "";
   String tty = "";
   long id = 0;
   String euid = "";
   String timestamp = "";
   SimpleDateFormat toFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
   toFormat.setTimeZone(TimeZone.getTimeZone("UTC"));

   // Arguments
   int argcount = 0;
   String baseCount = "a";
   int countInt = 1;
   String currCountName = "";
   String argVal = "";

   System.out.println("Parsing auditd data");
   // Read input from file
   line = br.readLine();
   while (line != null) {
    //  System.out.println("Processing line: " + line);
    // Get Key Val pairs for line
    syscallKeyVals = line.split(" ");
    for(String keyVal:syscallKeyVals)
    {
      String[] parts = keyVal.split("=");
      if (parts.length == 2)
      {
        holderSyscall.put(parts[0],parts[1]);
      }
    }
    //we only want those lines that start with SYSCALL and have our key
    if (holderSyscall.get("type").equals("SYSCALL") && holderSyscall.get("key").equals("\"eceld\"") && !holderSyscall.get("tty").equals("(none)"))
    {
        comm = holderSyscall.get("comm");
        // if command is not in quotes, then we have to convert from hex to ascii
        if (comm != null && !comm.startsWith("\""))
        {
            comm = hexToAscii(comm);
        }
        // Remove quotes from command:
        comm = comm.substring(1,comm.length()-1);
        timestamp = holderSyscall.get("msg");
        euid = holderSyscall.get("euid");
        tty = holderSyscall.get("tty");
        //get next line, if it exists
        line = br.readLine();
        if (line == null)
            continue;
        // Get Key Val pairs for second line
        execveKeyVals = line.split(" ");
        for(String keyVal:execveKeyVals)
        {
          String[] parts = keyVal.split("=");
          if (parts.length == 2)
          {
            holderExecve.put(parts[0],parts[1]);
          }
        }
        // If the second line is of type EXECVE then we process it; otherwise ignore and start over
        if (!holderExecve.get("type").equals("EXECVE"))
            continue;
        argcount = Integer.parseInt(holderExecve.get("argc"));
        baseCount = "a";
        countInt = 1;
        currCountName = "";
        argVal = "";
        for (countInt=1; countInt < argcount; countInt++)
        {
            currCountName = baseCount + Integer.toString(countInt);
            argVal = holderExecve.get(currCountName);
            //if arg value is not in quotes, then convert it from hex to ascii
            if (argVal != null && !argVal.startsWith("\""))
            {
                argVal = hexToAscii(argVal);
            }
            // remove double quotes
            argVal = argVal.substring(1, argVal.length()-1);
            comm += " " + argVal;
        }
        answer += formatOutLine(id++, comm, timestamp, toFormat);
    }
	line = br.readLine();
  }

  System.out.println("\tFinished processing auditd data (" + Long.toString(id) + " items)");
  br.close();
  answer += "\n]\n";
        FileOutput.WriteToFile(outputPath + "/auditdData.JSON", answer);
  }
  catch (FileNotFoundException e) {
   System.out.println("\tNo auditd file exists.");
  }
  catch (Exception e) {
   e.printStackTrace();
  }
 }

public static String formatOutLine(long id, String comm, String timestamp, SimpleDateFormat dateFormat)
{
    String answer = "";
    String timestampEpoch = "";
    if (id > 0)
    {
      answer += ",";
      answer += "\n";
    }  
    answer += "\t{\"auditd_id\" : "+ Long.toString(id)+", ";
    answer += "\"content\" : \"";
    answer += quote(comm);
    answer += "\", ";

    answer += "\"className\" : \"auditd";
    answer += "\", ";

    answer += "\"start\" : \"";
    timestampEpoch = timestamp.split("[(:]")[1];
    answer += dateFormat.format(new Date(((long)Double.parseDouble(timestampEpoch)*1000)));
    answer += "\"";
    answer += "}";
    return answer;
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

    public static String hexToAscii(String hexStr) 
    {
        StringBuilder output = new StringBuilder("");
            
        for (int i = 0; i < hexStr.length(); i += 2) 
        {
            String str = hexStr.substring(i, i + 2);
            output.append((char) Integer.parseInt(str, 16));
        }
    return "\"" +output.toString() + "\"";
    }
}