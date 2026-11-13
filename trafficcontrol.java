import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.executors;

public class trafficcontrol {
  private static final int PORT = 8080;
  //handling 10 requests at a time
  private static final ExecutorService threadPool = Executors.newFixedThreadPool();

  public static void main(String[] args()){
    try (ServerSocket servserSocket = new ServerSocket(PORT)) {
      Socket clientSocket = serverSocket.accept(); //waiting for client to accept or give request
      System.out.Println("Connection established from:" clientSocket.getRemoteSocketAddress)); //printing connection established

      threadPool.execute(() -> {
        try {
          clientSocket.close = serverSocket.close();
          System.out.Println("Connection closed.")); //printing connection closed
        }
        catch(IOexception e){
          e.PrintStackTrace();
        }
      });
    } catch (IOexception e){ 
      System.out.println("Could not start server" + e.getmessage)
    }
  } 
}     
