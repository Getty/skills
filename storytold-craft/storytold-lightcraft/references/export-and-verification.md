# Export policy and acceptance checks

**Read when:** delivering full-size, privacy-sensitive or cross-application photo outputs.

Specify output format, size, color space, depth, quality, metadata policy and enlargement policy. In the MCP export helper, use `longEdge:0` for full cropped resolution; `dontEnlarge` defaults to true. In the standalone render CLI, full cropped resolution is already the default. Set the size explicitly whenever reproducibility matters.

A requested bounding width/height is a fit, not necessarily a stretch to exactly those dimensions. Record actual output dimensions. PPI metadata does not create missing pixels. JPEG/AVIF/JXL quality, lossless settings and alpha support are format-specific; obtain accepted fields from the installed command/help rather than forwarding a generic bag of parameters.

After a batch, inspect each returned path and warning, not only the exit code. Repeated export may choose unique filenames. Count outputs, detect missing/duplicate results, hash inputs again when source preservation is required and sample more than one preview from a large shoot. Verify EXIF/geolocation removal for privacy-sensitive deliveries rather than assuming an innocuous filename is sufficient.

A successful save of settings is different from a successful pixel export. Reopen the persistent library to check catalog durability, and independently reopen rendered outputs to check dimensions, profiles, orientation, crop and appearance. For external-drive libraries, test an ordinary close/reopen cycle while the drive remains mounted; do not test crash recovery by killing a process that owns the only copy of the catalog.

## Evidence

- [light-cli](https://github.com/storytold/lightcraft/blob/main/apps/lightcraft-cli/src/main.rs)
- [light-mcp](https://github.com/storytold/lightcraft/blob/701f78ea2e586d4748705f10fdf5c4181dc1fd49/docs/mcp.md)
