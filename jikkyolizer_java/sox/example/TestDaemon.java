package example;

import org.apache.commons.daemon.Daemon;
import org.apache.commons.daemon.DaemonContext;
import org.apache.commons.daemon.DaemonInitException;
/*
import java.io.IOException;
import java.util.List;
import org.jivesoftware.smack.SmackException;
import org.jivesoftware.smack.XMPPException;

import jp.ac.keio.sfc.ht.sox.protocol.*;
import jp.ac.keio.sfc.ht.sox.soxlib.*;
import jp.ac.keio.sfc.ht.sox.soxlib.event.SoxEvent;
import jp.ac.keio.sfc.ht.sox.soxlib.event.SoxEventListener;
*/

import example.MySubscribe;

public class TestDaemon implements Daemon {

  private Thread thread; 
  private boolean stopped = false;

  @Override
  public void start() throws Exception {
	new MySubscribe();
	thread.start();
  }

  @Override
  public void stop() throws Exception {
    stopped = true;
    try {
      thread.join();
    } catch (InterruptedException e) {
      System.err.println(e.getMessage());
      throw e;
    }
  }

  @Override
  public void destroy() {
    thread = null;
  }

  @Override
  public void init(DaemonContext daemonContext) throws DaemonInitException, InterruptedException, Exception {
    thread = new Thread() {
      private long i = 0;
	  /*
      @Override
      public void run() {
        while(!stopped) {
          System.out.println(i++);
          try {
            sleep(1000);
          } catch (InterruptedException e) {
            System.err.println(e.getMessage());
          }
        }
      }
	  */
	  /*
	public void handlePublishedSoxEvent(SoxEvent e) {
		try{
		System.out.println(":::::Received Data:::::" + "\n");
		System.out.println("Message from: "+e.getOriginServer());
		List<TransducerValue> values = e.getTransducerValues();
		for (TransducerValue value : values) {
			System.out.println("TransducerValue[id:" + value.getId()
			+ ", rawValue:" + value.getRawValue() + ", typedValue:"
			+ value.getTypedValue() + ", timestamp:"
			+ value.getTimestamp() + "]" + "\n");
		}
		} catch(IOException e2){
			e2.printStackTrace();
		}
	}
	*/
    };
  }
/*
 public MySubscribe() throws Exception {
	try{
		SoxConnection con = new SoxConnection("sox.ht.sfc.keio.ac.jp",true);
		List<String> nodeList = con.getAllSensorList();
		int upper_limit = 0;
		for(String node:nodeList){
			SoxDevice exampleDevice = new SoxDevice(con, node);
			Device deviceInfo = exampleDevice.getDevice();
			System.out.println("[Device Meta Info] ID:" + deviceInfo.getId()
			+ ", Name:" + deviceInfo.getName() + " Type:"
			+ deviceInfo.getDeviceType().toString() + "\n");
			List<Transducer> transducerList = deviceInfo.getTransducers();
			for (Transducer t : transducerList) {
				System.out.println("[Transducer] Name:" + t.getName() + ", ID:"
				+ t.getId() + ", unit:" + t.getUnits() + ", minValue:"
				+ t.getMinValue() + ", maxValue:" + t.getMaxValue() + "\n");
			}
			exampleDevice.subscribe();
			exampleDevice.addSoxEventListener(this);
			upper_limit++ ;
			if (upper_limit > 10){
				break;
			}
		}
	} catch (SmackException e) {
		e.printStackTrace();
	} catch (IOException e) {
		e.printStackTrace();
	} catch (XMPPException e) {
		e.printStackTrace();
	}
 }
 */
}
