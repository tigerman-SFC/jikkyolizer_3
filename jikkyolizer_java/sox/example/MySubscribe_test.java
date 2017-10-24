/*
 * Copyright (C) 2014 Takuro Yonezawa
 * Keio University, Japan
 */

package example;

import java.io.File;
import java.io.FileWriter;
import java.io.BufferedWriter;

import java.io.IOException;
import java.util.List;

import org.jivesoftware.smack.SmackException;
import org.jivesoftware.smack.XMPPException;

import jp.ac.keio.sfc.ht.sox.protocol.*;
import jp.ac.keio.sfc.ht.sox.soxlib.*;
import jp.ac.keio.sfc.ht.sox.soxlib.event.SoxEvent;
import jp.ac.keio.sfc.ht.sox.soxlib.event.SoxEventListener;

import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.lang.Runtime;
import java.lang.Process;
import java.lang.InterruptedException;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.lang.ProcessBuilder;

public class MySubscribe_test implements SoxEventListener {
	
	File file = new File("/home/jikkyolizer_java/log/MySubscribe.log");
	FileWriter filewriter = new FileWriter(file);
	BufferedWriter outBuffer = new BufferedWriter(filewriter);

	Runtime runtime = Runtime.getRuntime();
	Process p; 
	int ret;
	//ProcessBuilder pb;

	public static void main(String[] args) throws Exception {
		new MySubscribe_test();
	}
	public static String dummy_escape(String not_escaped) {
		String escape_candidate[] = {"\"", "'", "=", ">", "<", " "};
		String escape_processed[] = {"”", "’", "＝", "＞", "＜", "　"};
		Pattern escape_pattern;
		Matcher matched;
		for(int i=0; i<5; i++){
			escape_pattern = Pattern.compile(escape_candidate[i]);
			matched = escape_pattern.matcher(not_escaped);
			not_escaped = matched.replaceAll(escape_processed[i]);
		}
		return not_escaped;
	}

	public MySubscribe_test() throws Exception {

		try{

		Process l_p;
		//anonymous login
		SoxConnection con = new SoxConnection("sox.ht.sfc.keio.ac.jp",true); 
		
		//login with JID and password
		// SoxConnection con = new SoxConnection("sox.ht.sfc.keio.ac.jp",
		// "guest","miroguest", true); 
		List<String> nodeList = con.getAllSensorList();
		int upper_limit = 0;
		for(String node:nodeList){
			SoxDevice exampleDevice = new SoxDevice(con, node);


		/** Create new device object from virtualized device **/
		//you can specify another SOX server where the node exists
		// SoxDevice exampleDevice = new SoxDevice(con,
		// "testNode","takusox.ht.sfc.keio.ac.jp");

		/** Getting Device Meta Data **/
		Device deviceInfo = exampleDevice.getDevice();

		//System.out.println("[Device Meta Info] ID:" + deviceInfo.getId()
		outBuffer.write("[Device Meta Info] ID:" + deviceInfo.getId()
				+ ", Name:" + deviceInfo.getName() + " Type:"
				+ deviceInfo.getDeviceType().toString() + "\n");
		List<Transducer> transducerList = deviceInfo.getTransducers();
		for (Transducer t : transducerList) {
			outBuffer.write("[Transducer] Name:" + t.getName() + ", ID:"
					+ t.getId() + ", unit:" + t.getUnits() + ", minValue:"
					+ t.getMinValue() + ", maxValue:" + t.getMaxValue() + "\n");
			String device_id, transducer_id;
			device_id = dummy_escape(deviceInfo.getId());
			transducer_id = dummy_escape(t.getId());
			String for_register_transducer = "'group_id=" + deviceInfo.getId() + ",item_id=" + t.getId() + "'";

			String register_transducer[] = {"/var/local/jikkyolizer/bin/python3", "/home/jikkyolizer_input/jikkyolizer_device2.py", for_register_transducer, "1>>/home/jikkyolizer_input/log/processing_input.log"};
			outBuffer.write(for_register_transducer+ "\n");
			outBuffer.write("1\n");
			l_p = new ProcessBuilder(register_transducer).start();
			l_p.waitFor();
			outBuffer.write("2\n");
		}
		
		
		Data data = exampleDevice.getLastPublishData();
		List<TransducerValue> values = data.getTransducerValue();
		outBuffer.write("--last published data starts--" + "\n");
		for (TransducerValue value : values) {
			outBuffer.write("TransducerValue[id:" + value.getId()
					+ ", rawValue:" + value.getRawValue() + ", typedValue:"
					+ value.getTypedValue() + ", timestamp:"
					+ value.getTimestamp() + "]" + "\n");
		}
		outBuffer.write("--last published data ends --" + "\n");
		
		exampleDevice.subscribe();
		exampleDevice.addSoxEventListener(this);

		/*
		 * If you close the program: 
		 * exampleDevice.unsubscribe();
		 * exampleDevice.removeSoxEventListener(); 
		 * con.disconnect();
		 */
		outBuffer.flush();
		upper_limit++ ;
			if (upper_limit > 5){ 
				//filewriter.close();
				break; 
			}
		}

		} catch (SmackException e) {
			// TODO Auto-generated catch block
		    e.printStackTrace();
		} catch (IOException e) {
		    // TODO Auto-generated catch block
		    e.printStackTrace();
		} catch (XMPPException e) {
		    // TODO Auto-generated catch block
			e.printStackTrace();
		} catch (NullPointerException e){
			e.printStackTrace();
		} catch (Exception e){
			e.printStackTrace();	
		}
	}

	public void handlePublishedSoxEvent(SoxEvent e) {
		// TODO Auto-generated method stub	
		try{

		outBuffer.write(":::::Received Data:::::" + "\n");
		outBuffer.write("Message from: "+e.getOriginServer());
		List<TransducerValue> values = e.getTransducerValues();
		String to_python_arg = "";
		Pattern pat;
		Matcher mat;
		String id_arg, value_arg, timing_arg;
		id_arg="";
		value_arg="";
		outBuffer.write("\n" +":::::Node ID:::::" + e.getNodeID() + "\n");
		String group_id = e.getNodeID();
		for (TransducerValue value : values) {
			outBuffer.write("TransducerValue[id:" + value.getId()
					+ ", rawValue:" + value.getRawValue() + ", typedValue:"
					+ value.getTypedValue() + ", timestamp:"
					+ value.getTimestamp() + "]" + "\n");
			
			if (value.getId().length() > 255 ){ id_arg = value.getId().substring(0,255); } else { id_arg = value.getId(); }
			if (value.getRawValue().length() > 255 ){ value_arg = value.getRawValue().substring(0,255); } else { value_arg = value.getRawValue(); }

			id_arg = dummy_escape(id_arg);
			value_arg = dummy_escape(value_arg);
			timing_arg = value.getTimestamp();
			to_python_arg = "'group_id" + group_id + " item_id=" + id_arg + " raw_value=" + value_arg + " timing=" + timing_arg + "'";

			p = new ProcessBuilder("/var/local/jikkyolizer/bin/python3", "/home/jikkyolizer_input/jikkyolizer_input2.py", to_python_arg, "1>>/home/jikkyolizer_input/log/processing_input.log").start();
			ret = p.waitFor();



		outBuffer.write("/var/local/jikkyolizer/bin/python3 /home/jikkyolizer_input/jikkyolizer_input.py " + to_python_arg + " 1>>/home/jikkyolizer_input/log/processing_input.log");
		}
		outBuffer.flush();
		} catch(IOException e2){
			e2.printStackTrace();
		} catch(InterruptedException ie){
		}
	}
}
