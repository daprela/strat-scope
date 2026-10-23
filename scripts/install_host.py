"""Provision local TLS and its public trust anchor; run outside sandbox explicitly.

Private keys stay in ~/.local/share/strat-scope/tls with mode 0600.
Existing identities are preserved; --renew reissues only the leaf certificate.
"""

import argparse
import os
import subprocess
from pathlib import Path


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path,
                        default=Path.home() / ".local/share/strat-scope")
    parser.add_argument("--trust-user", action="store_true")
    parser.add_argument("--trust-system", action="store_true")
    parser.add_argument("--renew", action="store_true")
    args = parser.parse_args()
    base = args.base.resolve()
    repository = Path(__file__).resolve().parents[1]
    if base.is_relative_to(repository) or base in repository.parents:
        raise SystemExit("TLS and active stores must be outside the synced checkout")
    os.umask(0o077)
    tls = base / "tls"
    tls.mkdir(parents=True, exist_ok=True, mode=0o700)
    (base / "store").mkdir(exist_ok=True, mode=0o700)
    root, root_key = tls / "root.crt", tls / "root.key"
    leaf, key = tls / "server.crt", tls / "server.key"
    if not root.exists():
        if root_key.exists():
            raise SystemExit("Existing CA key without public certificate; inspect manually")
        run("openssl", "req", "-x509", "-newkey", "ec", "-pkeyopt", "ec_paramgen_curve:P-256",
            "-nodes", "-keyout", str(root_key), "-out", str(root), "-days", "3650",
            "-subj", "/CN=Strat Scope Local Development CA",
            "-addext", "basicConstraints=critical,CA:TRUE,pathlen:0",
            "-addext", "keyUsage=critical,keyCertSign,cRLSign")
    if not leaf.exists() or args.renew:
        request = tls / "server.csr"
        extension = tls / "server.ext"
        extension.write_text("subjectAltName=IP:127.0.0.1\nbasicConstraints=critical,CA:FALSE\n"
                             "keyUsage=critical,digitalSignature\nextendedKeyUsage=serverAuth\n")
        run("openssl", "req", "-new", "-newkey", "ec", "-pkeyopt", "ec_paramgen_curve:P-256",
            "-nodes", "-keyout", str(key), "-out", str(request),
            "-subj", "/CN=Strat Scope Loopback")
        run("openssl", "x509", "-req", "-in", str(request), "-CA", str(root),
            "-CAkey", str(root_key), "-CAcreateserial", "-out", str(leaf),
            "-days", "365", "-sha256", "-extfile", str(extension))
        request.unlink()
        extension.unlink()
    run("openssl", "verify", "-CAfile", str(root), "-verify_ip", "127.0.0.1", str(leaf))
    if args.trust_user:
        # Chromium M146+ uses the XDG database; support existing legacy browsers too.
        data_home = Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local/share")))
        for database in (Path.home() / ".pki/nssdb", data_home / "pki/nssdb"):
            database.mkdir(parents=True, exist_ok=True)
            if not (database / "cert9.db").exists():
                run("certutil", "-N", "-d", "sql:" + str(database), "--empty-password")
            run("certutil", "-A", "-d", "sql:" + str(database), "-n", "Strat Scope Local Development CA",
                "-t", "C,,", "-i", str(root))
    if args.trust_system:
        # Fedora's supported system anchor location; never copy any private key.
        destination = "/etc/pki/ca-trust/source/anchors/strat-scope-local.crt"
        run("sudo", "-n", "install", "-m", "0644", str(root), destination)
        run("sudo", "-n", "update-ca-trust", "extract")
    run("openssl", "x509", "-in", str(leaf), "-noout", "-sha256", "-fingerprint",
        "-dates", "-ext", "subjectAltName")


if __name__ == "__main__":
    main()
