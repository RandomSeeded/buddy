package com.example.cam;

import android.util.Log;

import java.io.BufferedReader;
import java.io.DataOutput;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

/**
 * Created by nate on 2/6/16.
 */
public class Streamer {
    Socket socket;
    private static int port = 1337;
    private BufferedReader in;
    private PrintWriter out;
    private DataOutputStream dos;

    public Streamer(String address)  {
        try {
            socket = new Socket(address, port);
            dos = new DataOutputStream(socket.getOutputStream());
        }
        catch (IOException exception) {
            Log.d("Streamer", "IO Exception in streamer", exception);
        }
    }

    public void SendImage(int width, int height, byte[] send) {
        try {
            if (dos != null) {
                //Log.e("Streamer","Num Pixels: "+(width * height));
                //
                // Log.e("Streamer", "Send Length: "+send.length);
                Log.e("Streamer","Sent Frame. Sanity check: Width = " +
                        "" +
                        "   " +
                        ""+width);
                dos.writeInt(width);
                //Log.e("Streamer", "Height" + height);
                dos.writeInt(height);
                //dos.writeInt(send.length);

                dos.write(send, 0, send.length);
                dos.flush();
            }
        } catch (IOException e) {
        }
    }

    // Removed in favor of sendImage
    public void SendMessage(String data) {
        /*Log.d("Streamer", "Sending Message to Server");
        //out.println("Test Message");
        out.println(""+data);*/
    }
}
