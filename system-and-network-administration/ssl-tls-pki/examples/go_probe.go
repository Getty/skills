// A deliberately small HTTPS/1.1 TLS acceptance probe, not a general HTTP client.
// Usage: go_probe host port expected-name ca.pem ; no system trust mutations.
package main

import (
    "bufio"
    "crypto/tls"
    "crypto/x509"
    "fmt"
    "net"
    "os"
    "strconv"
    "strings"
    "time"
)
func run() error {
    if len(os.Args) != 5 { return fmt.Errorf("usage: go_probe host port expected-name ca.pem") }
    port, err := strconv.Atoi(os.Args[2]); if err != nil || port < 1 || port > 65535 { return fmt.Errorf("invalid port") }
    if strings.ContainsAny(os.Args[3], "\r\n /\\") { return fmt.Errorf("invalid reference name") }
    data, err := os.ReadFile(os.Args[4]); if err != nil { return err }
    pool := x509.NewCertPool()
    if !pool.AppendCertsFromPEM(data) { return fmt.Errorf("CA file contains no parsable certificates") }
    cfg := &tls.Config{RootCAs:pool, ServerName:os.Args[3], MinVersion:tls.VersionTLS12, NextProtos:[]string{"http/1.1"}}
    conn, err := tls.DialWithDialer(&net.Dialer{Timeout:5*time.Second}, "tcp", net.JoinHostPort(os.Args[1], strconv.Itoa(port)), cfg)
    if err != nil { return err }; defer conn.Close()
    if err = conn.SetDeadline(time.Now().Add(5*time.Second)); err != nil { return err }
    if _, err = fmt.Fprintf(conn, "GET / HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n", os.Args[3]); err != nil { return err }
    rawLine, err := bufio.NewReaderSize(conn, 16384).ReadSlice('\n'); if err != nil { return err }
    line := string(rawLine)
    if !strings.HasPrefix(line, "HTTP/1.1 200 ") { return fmt.Errorf("application rejected request: %s", strings.TrimSpace(line)) }
    fmt.Printf("verified %s; TLS version 0x%x; %s", os.Args[3], conn.ConnectionState().Version, line)
    return nil
}
func main() { if err := run(); err != nil { fmt.Fprintln(os.Stderr, err); os.Exit(1) } }
