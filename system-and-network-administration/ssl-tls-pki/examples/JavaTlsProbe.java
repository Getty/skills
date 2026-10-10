// Java 11+; usage: JavaTlsProbe host port expected-name ca.pem
// Explicit in-memory trust, HTTPS identity checking, and an application status check.
import javax.net.ssl.*;
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.KeyStore;
import java.security.cert.CertificateFactory;
import java.util.List;

public class JavaTlsProbe {
    public static void main(String[] args) {
        try { run(args); }
        catch (Exception e) { System.err.println(e.getClass().getSimpleName()+": "+e.getMessage()); System.exit(1); }
    }
    static void run(String[] args) throws Exception {
        if (args.length != 4) throw new IllegalArgumentException("usage: JavaTlsProbe host port expected-name ca.pem");
        int port = Integer.parseInt(args[1]);
        if (port < 1 || port > 65535 || args[2].matches(".*[\\r\\n /\\\\].*")) throw new IllegalArgumentException("invalid port/name");
        KeyStore store = KeyStore.getInstance(KeyStore.getDefaultType());
        store.load(null, null);
        int count = 0;
        try (InputStream input = Files.newInputStream(Path.of(args[3]))) {
            for (java.security.cert.Certificate c : CertificateFactory.getInstance("X.509").generateCertificates(input))
                store.setCertificateEntry("root-"+(count++), c);
        }
        if (count == 0) throw new IllegalArgumentException("empty CA bundle");
        TrustManagerFactory tm = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
        tm.init(store);
        SSLContext context = SSLContext.getInstance("TLS");
        context.init(null, tm.getTrustManagers(), null);
        try (Socket tcp = new Socket()) {
            tcp.connect(new InetSocketAddress(args[0], port), 5000);
            tcp.setSoTimeout(5000);
            try (SSLSocket socket = (SSLSocket)context.getSocketFactory().createSocket(tcp, args[2], port, true)) {
                SSLParameters parameters = socket.getSSLParameters();
                parameters.setEndpointIdentificationAlgorithm("HTTPS");
                parameters.setServerNames(List.of(new SNIHostName(args[2]))); // This small probe expects a DNS reference name.
                parameters.setProtocols(new String[]{"TLSv1.3", "TLSv1.2"});
                parameters.setApplicationProtocols(new String[]{"http/1.1"});
                socket.setSSLParameters(parameters);
                socket.startHandshake();
                socket.getOutputStream().write(("GET / HTTP/1.1\r\nHost: "+args[2]+"\r\nConnection: close\r\n\r\n").getBytes(StandardCharsets.US_ASCII));
                ByteArrayOutputStream status = new ByteArrayOutputStream();
                long deadline = System.nanoTime() + 5_000_000_000L;
                boolean terminated = false;
                while (status.size() < 16384) {
                    long remaining = deadline - System.nanoTime();
                    if (remaining <= 0) throw new SocketTimeoutException("HTTP status deadline exceeded");
                    socket.setSoTimeout((int)Math.max(1L, (remaining + 999_999L) / 1_000_000L));
                    int value = socket.getInputStream().read();
                    if (value < 0) break;
                    if (value == '\n') { terminated = true; break; }
                    status.write(value);
                }
                String line = status.toString(StandardCharsets.US_ASCII).stripTrailing();
                if (!terminated || !line.startsWith("HTTP/1.1 200 ")) throw new IOException("application rejection or missing status: "+line);
                System.out.println(socket.getSession().getProtocol()+" "+line);
            }
        }
    }
}
