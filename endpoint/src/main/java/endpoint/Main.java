package endpoint;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.OffsetDateTime;
import java.time.format.DateTimeParseException;
import java.util.UUID;

public class Main {

    static final String TOKEN = System.getenv("REGISTER_TOKEN");
    static final int MAX_BODY_BYTES = 4096;
    static final ObjectMapper JSON = new ObjectMapper();

    // One registration, after it has been read and checked
    record Registration(UUID id, String domain, String serviceHost, int servicePort, OffsetDateTime timeUtc) {}

    // Our own error type: "this field is wrong". The message goes back to the sender with a 400.
    static class BadField extends Exception {
        BadField(String message) {
            super(message);
        }
    }

    public static void main(String[] args) throws IOException {
        if (TOKEN == null || TOKEN.isBlank()) {
            System.out.println("REGISTER_TOKEN is not set. Stopping.");
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
            reply(exchange, 401, "Missing or wrong token");
            return;
        }
        byte[] bytes;
        try (InputStream in = exchange.getRequestBody()) {
            bytes = in.readNBytes(MAX_BODY_BYTES + 1);
        }
        if (bytes.length > MAX_BODY_BYTES) {
            reply(exchange, 413, "Body is bigger than 4 KB");
            return;
        }
        String body = new String(bytes, StandardCharsets.UTF_8);

        // NEW: read the JSON and check every field
        Registration reg;
        try {
            reg = parse(body);
        } catch (BadField e) {
            reply(exchange, 400, e.getMessage());
            return;
        }

        System.out.println("Valid: " + reg);
        reply(exchange, 200, "valid");
    }

    // Turns the body text into a Registration, or throws BadField naming the problem
    static Registration parse(String body) throws BadField {
        JsonNode json;
        try {
            json = JSON.readTree(body);
        } catch (JsonProcessingException e) {
            throw new BadField("Body is not valid JSON");
        }
        if (json == null || !json.isObject()) {
            throw new BadField("Body must be a JSON object");
        }

        String rawId = text(json, "registration_id");
        UUID id;
        try {
            id = UUID.fromString(rawId);
        } catch (IllegalArgumentException e) {
            throw new BadField("registration_id is not a valid UUID");
        }
        if (rawId.length() != 36) {
            throw new BadField("registration_id is not a valid UUID");
        }

        String domain = text(json, "domain");
        String serviceHost = text(json, "service_host");

        JsonNode portNode = json.get("service_port");
        if (portNode == null || !portNode.isInt()) {
            throw new BadField("service_port is missing or not a whole number");
        }
        int servicePort = portNode.intValue();
        if (servicePort < 1 || servicePort > 65535) {
            throw new BadField("service_port must be between 1 and 65535");
        }

        OffsetDateTime timeUtc;
        try {
            timeUtc = OffsetDateTime.parse(text(json, "time_utc"));
        } catch (DateTimeParseException e) {
            throw new BadField("time_utc is not a valid time (example: 2026-11-20T09:30:00Z)");
        }

        return new Registration(id, domain, serviceHost, servicePort, timeUtc);
    }

    // Returns a required text field, or throws BadField if it is missing or empty
    static String text(JsonNode json, String field) throws BadField {
        JsonNode node = json.get(field);
        if (node == null || !node.isTextual() || node.asText().isBlank()) {
            throw new BadField(field + " is missing or empty");
        }
        return node.asText().trim();
    }

    static void reply(HttpExchange exchange, int status, String text) throws IOException {
        byte[] bytes = text.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "text/plain; charset=utf-8");
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream out = exchange.getResponseBody()) {
            out.write(bytes);
        }
    }
}
