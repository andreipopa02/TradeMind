
def verification_email_template(user_name: str, verification_link: str) -> str:
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
        <div style="background-color: #ffffff; border-radius: 8px; padding: 20px; max-width: 600px; margin: auto;">
            <h2 style="color: #333333;">Salut, {user_name}!</h2>
            <p>Iti multumim ca te-ai inregistrat in aplicatia TradeMind.</p>
            <p>Te rugam sa confirmi adresa ta de email apasand pe butonul de mai jos:</p>
            <a href="{verification_link}" style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">Confirmă Emailul</a>
            <p style="margin-top: 30px;">Acest email a fost trimis ca urmare a dezvoltarii unei noi aplicatii, 
            daca nu tu ai solicitat aceasta operatiune, te rog ignora acest mesaj.</p>
            <p style="color: #777;">Echipa TradeMind</p>
        </div>
    </body>
    </html>
    """

def reset_password_email_template(user_name: str, reset_link: str) -> str:
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
        <div style="background-color: #ffffff; border-radius: 8px; padding: 20px; max-width: 600px; margin: auto;">
            <h2 style="color: #333333;">Salut, {user_name}!</h2>
            <p>Ai cerut resetarea parolei pentru contul tau TradeMind.</p>
            <p>Apasa pe butonul de mai jos pentru a seta o parola noua:</p>
            <a href="{reset_link}" style="display: inline-block; padding: 10px 20px; background-color: #007BFF; color: white; text-decoration: none; border-radius: 5px;">Resetează parola</a>
            <p style="margin-top: 30px;">Acest email a fost trimis ca urmare a dezvoltarii unei noi aplicatii, 
            daca nu tu ai solicitat aceasta operatiune, te rog ignora acest mesaj.</p>
            <p style="color: #777;">Echipa TradeMind</p>
        </div>
    </body>
    </html>
    """
