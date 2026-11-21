import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;

public class Main {

    static final String TOKEN = System.getenv("REGISTER_TOKEN");

    static final int MAX_BODY_BYTES = 4096;

    public static void main(String[] args) throws IOException {
        if (TOKEN == null || TOKEN.isBlank()){
            System.out.println("REGISTER_TOKEN is not set. Stopping");
            return;
        }

        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 1200), 0);
        server.createContext("/register", Main::handleRegister);
        server.start();

        System.out.println("Listening on http://127.0.0.1:1200/register");
    }

    static void handleRegister(HttpExchange exchange) throws IOException {
        if (!exchange.getRequestMethod().equals("POST")) {
            reply(exchange, 405, "Only POST is allowed");
            return;           
        }

        String auth = exchange.getRequestHeaders().getFirst("Authorization");
        if (auth == null || !auth.equals("Bearer " + TOKEN)) {
            reply(exchange, 401, "Missing or wrong Token");
            return;
        }

        byte[] bytes;
        try (InputStream in = exchange.getRequestBody()){
            bytes = in.readNBytes(MAX_BODY_BYTES + 1);
        }

        if (bytes.length > MAX_BODY_BYTES) {
            reply(exchange, 413, "Body is greater than 4KB");
            return;            
        }
    
        String body = new String(bytes, StandardCharsets.UTF_8);

        System.out.println("Recieved" + body);

        reply(exchange, 200, "recieved");
    }

    static void reply(HttpExchange exchange, int status, String text) throws IOException{
        byte[] bytes = text.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "text/plain; charset=utf-8");
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream out = exchange.getResponseBody()){
            out.write(bytes);
        }        
    }

}

