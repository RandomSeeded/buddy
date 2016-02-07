import java.net.ServerSocket;
import java.net.Socket;
import java.io.*;

public class server {
  public static void main(String[] args) throws Exception {
    int port = 1337;
    ServerSocket listener = new ServerSocket(port);
    System.out.println("Server is listening on port "+port);
    try {
      while(true) {
        Phone myPhone = new Phone(listener.accept());
        myPhone.start();
      }
    } finally {
      listener.close();
    }
  }
}

class Phone extends Thread {
  Socket socket;
  // BufferedReader input;
  // PrintWriter output;

  public Phone(Socket socket) {
    this.socket = socket;
    System.out.println("Phone connected!");
    // try {
    //   input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
    //   output = new PrintWriter(socket.getOutputStream(), true);
    //   output.println("This is a message from the server.");
    // } catch (IOException e)  {
    //   System.out.println("Phone disconnected. "+e);
    // }
  }
  
  public void run() {
    System.out.println("Run method got called.");
    try {

      DataInputStream dis = new DataInputStream(socket.getInputStream());

      while(true) {
          int width = dis.readInt();
          int height = dis.readInt();

          System.out.println("Width :"+width);
          System.out.println("Height :"+height);

          // (important!) Figure out why the width and height dont match up with the number of pixels
          // NOTE: fixed (conversion to grayscale). We can stil leave as-is though. 
          // int numPixels = width * height;

          int numPixels = dis.readInt();
          byte[] pixels = new byte[numPixels];

          int read = 0;
          while (read < numPixels) {
            read += dis.read(pixels, read, numPixels - read);
          }

          System.out.println("Pixels :"+pixels);
      }
    } catch (IOException e) {
      System.out.println("IOException: "+e);
    }
  }
}



