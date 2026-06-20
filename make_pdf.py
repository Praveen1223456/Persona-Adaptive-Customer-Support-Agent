import os
from fpdf import FPDF

def create_sample_pdf():
    # Make sure the data folder exists before writing to it
    os.makedirs("data", exist_ok=True)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    content = """
    PASSWORD RECOVERY AND ACCESS LOCKOUT GUIDE

    1. Automated Recovery Flow
    Users can securely recover their account credentials by navigating to the login screen and clicking 'Forgot Password'. An automated transaction email containing a unique reset key link will be dispatched immediately.

    2. Access Token Lifespan
    For network security protection, the recovery link token remains active for exactly 15 minutes. If it is not accessed within this window, the token self-terminates, and the user must request a new validation signature.

    3. Account Lockout State
    If a user inputs an incorrect password 5 consecutive times, the system enters a hard security lock state. When an account is locked out, the AI agent cannot clear it; the issue must be passed to a human administrator to verify physical identification documents.
    """

    for line in content.split("\n"):
        # Strip trailing/leading spaces to keep text clean
        pdf.cell(200, 10, txt=line.strip(), ln=True, align='L')

    # Save it straight into your data folder
    pdf.output("data/password_reset_guide.pdf")
    print("✅ Successfully created password_reset_guide.pdf inside the data directory!")

if __name__ == "__main__":
    create_sample_pdf()