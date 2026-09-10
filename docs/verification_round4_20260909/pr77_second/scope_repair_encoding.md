# Patch byte encoding record

The scope repair changes only README and proof Section 9 at head `2564e25a8b62a72992b9451988cd42e2d5a81834`, parent `8de8b0007f9374b7a5decb9b0a2f1c939fe897be`. All other 21 source files remain unchanged.

The original publication receipt hashes the LF-encoded patch text: `cfaea852330685e251b3d006bcccd07be2e0c86dcefa6916be7ac2b46192d55d`. The Windows local patch copied into the isolated SECOND packet has CRLF line endings and SHA256 `80e037b25dd40a4f45c60b974b8b82f61e6b2a415420cf521b7c2dd9724ab46c`. C3 checked that replacing CRLF with LF exactly recovers the receipt hash. These are explicit byte representations of the same patch; source-file hashes are independently bound to the immutable Git blobs. The SECOND report correctly records its actual CRLF input digest. Original reports and receipt are preserved.

The public patch copy uses LF. Publication mapping records every source and public-copy SHA256; this encoding normalization is not a new proof or arithmetic check.
