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



public class DaemonSubscribe implements SoxEventListener {
	
	public static void main(String[] args) throws Exception {
		new DaemonSubscribe();
	}

	public DaemonSubscribe() throws Exception {

		try{

		//anonymous login
		SoxConnection con = new SoxConnection("sox.ht.sfc.keio.ac.jp",true); 
		
		//login with JID and password
		// SoxConnection con = new SoxConnection("sox.ht.sfc.keio.ac.jp",
		// "guest","miroguest", true); 
		//File file = new File("/home/jikkyolizer_java/log");
		//FileWriter filewriter = new FileWriter(file);
		List<String> nodeList = con.getAllSensorList();
		int upper_limit = 0;
		for(String node:nodeList){
			SoxDevice exampleDevice = new SoxDevice(con, node);


		/** Create new device object from virtualized device **/
		//SoxDevice exampleDevice = new SoxDevice(con, "24時間降水量-仁世宇");

		//you can specify another SOX server where the node exists
		// SoxDevice exampleDevice = new SoxDevice(con,
		// "testNode","takusox.ht.sfc.keio.ac.jp");

		/** Getting Device Meta Data **/
		Device deviceInfo = exampleDevice.getDevice();

		//System.out.println("[Device Meta Info] ID:" + deviceInfo.getId()
		System.out.println("[Device Meta Info] ID:" + deviceInfo.getId()
				+ ", Name:" + deviceInfo.getName() + " Type:"
				+ deviceInfo.getDeviceType().toString() + "\n");
		List<Transducer> transducerList = deviceInfo.getTransducers();
		for (Transducer t : transducerList) {
			System.out.println("[Transducer] Name:" + t.getName() + ", ID:"
					+ t.getId() + ", unit:" + t.getUnits() + ", minValue:"
					+ t.getMinValue() + ", maxValue:" + t.getMaxValue() + "\n");
		}

		Data data = exampleDevice.getLastPublishData();
		List<TransducerValue> values = data.getTransducerValue();
		System.out.println("--last published data starts--" + "\n");
		for (TransducerValue value : values) {
			System.out.println("TransducerValue[id:" + value.getId()
					+ ", rawValue:" + value.getRawValue() + ", typedValue:"
					+ value.getTypedValue() + ", timestamp:"
					+ value.getTimestamp() + "]" + "\n");
		}
		System.out.println("--last published data ends --" + "\n");
		
		exampleDevice.subscribe();
		exampleDevice.addSoxEventListener(this);

		/*
		 * If you close the program: 
		 * exampleDevice.unsubscribe();
		 * exampleDevice.removeSoxEventListener(); 
		 * con.disconnect();
		 */
		//outBuffer.flush();
		upper_limit++ ;
			if (upper_limit > 100){ 
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
		}
	}

	public void handlePublishedSoxEvent(SoxEvent e) {
		// TODO Auto-generated method stub	
		//try{
	//	File file2 = new File("/home/jikkyolizer_java/log");
	//	FileWriter filewriter2 = new FileWriter(file2);
	//	BufferedWriter outBuffer2 = new BufferedWriter(filewriter2);

		System.out.println(":::::Received Data:::::" + "\n");
		System.out.println("Message from: "+e.getOriginServer());
		List<TransducerValue> values = e.getTransducerValues();
		for (TransducerValue value : values) {
			System.out.println("TransducerValue[id:" + value.getId()
					+ ", rawValue:" + value.getRawValue() + ", typedValue:"
					+ value.getTypedValue() + ", timestamp:"
					+ value.getTimestamp() + "]" + "\n");
		}
		/*
		} catch(IOException e2){
			e2.printStackTrace();
		}*/
	}
}
