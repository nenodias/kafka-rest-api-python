import pexpect


def build_ca_pems(input_file: str, password: bytes):
    output_file = input_file.replace("keystore.p12", ".caroot.pem").replace("uploads", "certs")
    args = f"openssl pkcs12 -in {input_file} -out {output_file}"
    print(args)
    process = pexpect.spawn(args)
    process.echo = True
    process.expect("Enter Import Password:", timeout=5)
    process.sendline(password)
    process.expect("Enter PEM pass phrase:", timeout=5)
    process.sendline(password)
    process.expect("Verifying - Enter PEM pass phrase:", timeout=5)
    process.sendline(password)
    process.sendline()

def build_rsa_pems(input_file: str, password: bytes):
    output_file = input_file.replace("keystore.p12", ".rsakey.pem").replace("uploads", "certs")
    args = f"openssl pkcs12 -in {input_file} -nodes -nocerts -out {output_file}"
    print(args)
    process = pexpect.spawn(args)
    process.expect("Enter Import Password:", timeout=5)
    process.sendline(password)
    process.sendline()

