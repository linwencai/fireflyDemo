//firefly java client

import java.io.BufferedReader;  
import java.io.DataOutputStream;  
import java.io.IOException;
import java.io.InputStream;  
import java.io.InputStreamReader;  
import java.io.OutputStream;  
import java.net.InetAddress;  
import java.net.Socket;  
import java.util.Arrays;

public class Client implements Runnable {  
    //启动main时传进来两个参数：ip和端口号  
    public static void main(String [] args)   
    {  
    try  
    {  
        //Socket s=new Socket(InetAddress.getByName("192.168.0.213"),8001);  
//        if(args.length < 2)  
//        {  
//            System.out.println("Usage:java TcpClient ServerIP ServerPort");  
//            return;  
//        }  
//        //建立Socket  
//        Socket s=new Socket(InetAddress.getByName(args[0]),Integer.parseInt(args[1]));  
    	Socket s=new Socket(InetAddress.getByName("127.0.0.1"), 1000);  
        InputStream ips=s.getInputStream();  
        OutputStream ops=s.getOutputStream();  
        
        BufferedReader brKey = new BufferedReader(new InputStreamReader(System.in));//键盘输入  
//        DataOutputStream dos = new DataOutputStream(ops);  
//        BufferedReader brNet = new BufferedReader(new InputStreamReader(ips));  
        
        new Thread(new Client(ips)).start();  
        
        while(true)  
        {  
            String strWord = brKey.readLine();// + System.getProperty("line.separator");
            
            byte serverVersion[] = intToByte(0);
            byte len[] = intToByte(strWord.getBytes().length+4);
            byte commandId[] = intToByte(1);
            
            byte head1[] = {0,0,0,0,0};
            byte head2[] = byteMerger(head1, serverVersion);
            byte head3[] = byteMerger(head2, len);
            byte head[] = byteMerger(head3, commandId);
            byte sendData[] = byteMerger(head, strWord.getBytes());
            System.out.println("Send:" + Arrays.toString(sendData));
            //dos.write(sendData);
            ops.write(sendData);
            //dos.writeBytes(head + strWord);  
            if(strWord.equalsIgnoreCase("quit"))  
                break;  
            else 
                //System.out.println(brNet.readLine());
            	;
        }  
//        dos.close();  
//        brNet.close();  
        brKey.close();  
        s.close();  
    }catch(Exception e){e.printStackTrace();}  
    }  
    
    public static byte[] byteMerger(byte[] byte_1, byte[] byte_2){  
        byte[] byte_3 = new byte[byte_1.length+byte_2.length];  
        System.arraycopy(byte_1, 0, byte_3, 0, byte_1.length);  
        System.arraycopy(byte_2, 0, byte_3, byte_1.length, byte_2.length);  
        return byte_3;  
    }  
    
    public static byte[] subBytes(byte[] src, int begin, int count) {
        byte[] bs = new byte[count];
        for (int i=begin; i<begin+count; i++) bs[i-begin] = src[i];
        return bs;
    }
    
    public static byte[] intToByte(int number) {  
        byte[] abyte = new byte[4];  
        // "&" 与（AND），对两个整型操作数中对应位执行布尔代数，两个位都为1时输出1，否则0。  
        abyte[0] = (byte) (0xff & number);  
        // ">>"右移位，若为正数则高位补0，若为负数则高位补1  
        abyte[1] = (byte) ((0xff00 & number) >> 8);  
        abyte[2] = (byte) ((0xff0000 & number) >> 16);  
        abyte[3] = (byte) ((0xff000000 & number) >> 24);  
        return abyte;  
    }  
    
    public static int bytesToInt(byte[] bytes) {  
        int number = bytes[0] & 0xFF;  
        // "|="按位或赋值。  
        number |= ((bytes[1] << 8) & 0xFF00);  
        number |= ((bytes[2] << 16) & 0xFF0000);  
        number |= ((bytes[3] << 24) & 0xFF000000);  
        return number;  
    }
    
//    public   static   byte [] intToByte( int  n) { 
//    	   byte [] b =  new   byte [ 4 ]; 
//    	   b[3 ] = ( byte ) (n &  0xff ); 
//    	   b[2 ] = ( byte ) (n >>  8  &  0xff ); 
//    	   b[1 ] = ( byte ) (n >>  16  &  0xff ); 
//    	   b[0 ] = ( byte ) (n >>  24  &  0xff ); 
//    	   return  b; 
//    	}   
//    public static int bytesToInt(byte[] bytes) {  
//      int number = bytes[3] & 0xFF;  
//      // "|="按位或赋值。  
//      number |= ((bytes[2] << 8) & 0xFF00);  
//      number |= ((bytes[1] << 16) & 0xFF0000);  
//      number |= ((bytes[0] << 24) & 0xFF000000);  
//      return number;  
//    }
    
    BufferedReader brNet;  
    InputStream ips;
    public Client(InputStream ips) {  
        super(); 
        this.ips = ips; 
//        this.brNet = brNet;  
    }  
    
    @Override  
    public void run() {  
	    try {  
//	    	String cbuf = "";
//	    	int len;
//	    	while(true){
//	    		cbuf = "";
//	    		len = 0;
//	    		while (len != 0 && len > cbuf.length()+10){
//	    			len ++;
//	    			cbuf += (char) this.brNet.read();
//	    		}
//	    		
//	    		System.out.println("rec:"+cbuf);
	    	
		        //System.out.println("rec:" + this.brNet.readLine());
		        //Thread.sleep(1000);
//	    	}
	    	byte[] head = {0,0,0,0,0,0,0,0,0};
	    	byte[] tmp;
	    	int len;
	    	int key;
	    	while(true){
	    		byte[] b = new byte[1024];
	    	    int n = this.ips.read(b);
	    	    byte[] data = new byte[n];
	    	    System.arraycopy(b, 0, data, 0, n);
	    	    //System.out.println("Rec:" + n + Arrays.toString(data));
	    	    for (int i=0; i<n;){
	    	    	tmp = subBytes(data, i, head.length);
	    	    	if (Arrays.equals(tmp, head)){
	    	    		i += head.length;
	    	    		
	    	    		tmp = subBytes(data, i, 4);
	    	    		len = bytesToInt(tmp);
	    	    		i += 4;
	    	    		
	    	    		tmp = subBytes(data, i, 4);
	    	    		key = bytesToInt(tmp);
	    	    		i += 4;
	    	    		
//	    	    		byte[] message = new byte[len];
//	    	    		message = subBytes(data, i, len-4);
	    	    		String message= new String(subBytes(data, i, len-4),"UTF-8");
	    	    		//System.out.println("message:"+key+Arrays.toString(message)+message);
	    	    		System.out.println("key:"+key+" message:"+message);
	    	    		i += len-4;
	    	    	}
	    	    	else
	    	    		i++;
	    	    }
	    	}
	    }
	    catch (Exception e) {
	        e.printStackTrace();
	    }
    }

}  
    