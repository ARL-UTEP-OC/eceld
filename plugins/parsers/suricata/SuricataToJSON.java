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

			//sample: {"suricata_id : 0", "rule_id: 600", "alert_text": "ICMP Packet Found", "className: " "suricataAlert", "start": 10/17/2020T23:53:27.395703 }

			// File processing variables
			String filename = args[0];
			String outputPath = args[1];
			FileReader fr = new FileReader(filename);
			BufferedReader br = new BufferedReader(fr);
			String line;
			String answer = "[\n";

		// Field Parser Variables

			HashMap<String, String> holderSuriAlerts = new HashMap<String, String>();
			HashMap<String, String> holderSuriAlerts2 = new HashMap<String, String>();

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

			// System.out.println("Processing line: " + line);
				alertsKeyVals = line.replaceAll("\\s+", " ").split(" ");
				List<Integer> matchingIndices = new ArrayList<>();
				String needle = "[**]";
				for(int i=0; i < alertsKeyVals.length; i++){
					String element = alertsKeyVals[i];

					if (needle.equals(element)){
						matchingIndices.add(i);
					}
				}

				// System.out.println(matchingIndices);
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
//         System.out.println(timestamp);
        String time = timestamp.replace("-", " ").split("\\.")[0];
//         System.out.println(time);
        SimpleDateFormat sdf = new SimpleDateFormat("MM/dd/yyyy HH:mm:ss");
        try
        {
            Date date = sdf.parse(time);
            System.out.println(date);
            sdf.applyPattern("yyyy-MM-dd'T'HH:mm:ss");
            return sdf.format(date);
        }catch(ParseException e)
        {
            System.out.println("Error while parsing time in raw suricata file: " + e);
            return "";
        }
     }

//     public static String removeOffsetTime(String timestamp)
//      {
//         String answer;
//         SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
//         try
//         {
//             Date myFormattedDate = sdf.parse(timestamp);
//             SimpleDateFormat toFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
//             toFormat.setTimeZone(TimeZone.getTimeZone("UTC"));
//             return toFormat.format(myFormattedDate);
//         }catch(ParseException e)
//         {
//             System.out.println("Error while parsing time in raw auditd file: " + e);
//             return "";
//         }
//      }

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
