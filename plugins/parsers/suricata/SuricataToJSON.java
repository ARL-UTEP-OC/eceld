import java.io.*;
import java.util.*;
import java.text.*;
import java.util.HashMap;
import java.util.Arrays;

public class SuricataToJSON{
	static long numItems = 0;

	public static void main(String args[]){
		try {
			if(args.length != 2){
				System.out.println("Usage: java suricataToJSON <filename> <ouput-directory>");
				System.exit(-1);
			}

			// sample: "suricata_id" : 6, "suricata_rule_id" : "[1:2:1]", "content" : "PING detected ", "className" : "suricataAlert", "start" : "2020-11-20T05:08:49"

			// File processing variables
			String filename = args[0];
			String outputPath = args[1];
			FileReader fr = new FileReader(filename);
			BufferedReader br = new BufferedReader(fr);
			String line;
			String answer = "[\n";

			String[] alertsKeyVals = null;
			String[] suriKeyVals = null;

		    // Fields
			String rule = "";
			String alertText = "";
			long id = 0;
			String timestamp = "";
			String[] ruleContent = null;

			System.out.println("\tParsing Suricata alerts");

		    // Read input from file
			line = br.readLine();
			while(line != null){

				alertsKeyVals = line.replaceAll("\\s+", " ").split(" ");
				List<Integer> matchingIndices = new ArrayList<>();
				String needle = "[**]";
				for(int i=0; i < alertsKeyVals.length; i++){
					String element = alertsKeyVals[i];

					if (needle.equals(element)){
						matchingIndices.add(i);
					}
				}

				for(int i=0; i < alertsKeyVals.length; i++){
					timestamp = alertsKeyVals[0];
					ruleContent = subArray(alertsKeyVals, matchingIndices.get(0), matchingIndices.get(1));
					rule = ruleContent[1];
				}
				for(int x = 2; x < ruleContent.length - 1; x++)
					alertText += ruleContent[x] + " ";

				answer += formatOutLine(id++, rule, alertText, timestamp);

				alertText = "";
				line = br.readLine();
			}

			System.out.println("\tFinished processing suricata alerts data (" + Long.toString(id) + " items)");
			br.close();
			answer += "\n]\n";
			FileOutput.WriteToFile(outputPath + "/suricata.JSON", answer);
		}

		catch (FileNotFoundException e) {
			System.out.println("\tNo suricata file exists.");
		}
		catch (Exception e) {
			e.printStackTrace();
		}

	}

	public static String formatOutLine(long id, String rule, String alertText, String timestamp){
		String answer = "";
		if (id > 0) {
			answer += ",";
			answer += "\n";
		}

		answer += "\t{\"suricata_id\" : "+ Long.toString(id)+", ";
		answer += "\"suricata_rule_id\" : \"";
		answer += quote(rule);
		answer += "\", ";
		answer += "\"content\" : \"";
		answer += quote(alertText);
		answer += "\", ";

		answer += "\"className\" : \"suricataAlert";
		answer += "\", ";

		answer += "\"start\" : \"";
		answer += formatTimestamp(timestamp);
		answer += "\"";
		answer += "}";

		return answer;

	}

	public static String formatTimestamp(String timestamp)
     {
        String answer;
        String time = timestamp.replace("-", " ").split("\\.")[0];
        SimpleDateFormat fromFormat = new SimpleDateFormat("MM/dd/yyyy HH:mm:ss");
        SimpleDateFormat toFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
        toFormat.setTimeZone(TimeZone.getTimeZone("UTC"));
        try
        {
            return toFormat.format(fromFormat.parse(time));
        }catch(ParseException e)
        {
            System.out.println("Error while parsing time in raw suricata file: " + e);
            return "";
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

	public static<T> T[] subArray(T[] array, int beg, int end) {
		return Arrays.copyOfRange(array, beg, end + 1);
	}


}
