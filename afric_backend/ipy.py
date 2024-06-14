import secrets

def generate_secure_otp():
    otp = f"{secrets.randbelow(9000) + 1000}"
    return otp

# Générer un OTP sécurisé
secure_otp_code = generate_secure_otp()
print(f"Votre OTP sécurisé est : {secure_otp_code}")