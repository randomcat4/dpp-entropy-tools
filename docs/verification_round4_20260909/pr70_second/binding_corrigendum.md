# C3 provenance corrigendum to the PR70 SECOND report

The completed reviewer report repeats a transcription error in the hash of input_binding.json: its printed value has 66 hexadecimal characters and is not a valid SHA-256 digest. The actual unchanged metadata file has SHA-256 `5d9bdeae61659ea837ff82298ddb3dfd6d77d922b14baea3ea9f65ecec621d7b` (64 characters).

C3 independently hashed all eight author input files and verified that every observed author-file hash matches both the reviewer source_binding.json and the original input_binding.json. The frozen author head remains f7be60759fd4d65184803b6585965dc7e5ccd624. No author source, mathematical assertion, reviewer report or input metadata was changed. The original malformed metadata digest remains visible in the archived reviewer files; publication_mapping.json binds those original reports to the copies. This note corrects provenance transcription only and is not an additional mathematical review or arithmetic run.
