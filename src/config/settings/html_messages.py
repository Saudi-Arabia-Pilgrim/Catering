VERIFY_CODE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Template</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f8f9fa; color: #333333; margin: 0; padding: 60px 0px;">
    <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border: 1px solid #ddd; border-radius: 8px;">
        <!-- Content -->
        <div style="text-align: center;">
            <h1 style="color: #d9534f; font-size: 24px;">Verification Code</h1>
            <p style="font-size: 16px; margin: 10px 0;">Enter the code below to continue:</p>
            <div style="display: inline-block; background-color: #f0f0f0; padding: 10px 20px; font-size: 20px; font-weight: bold; color: #333333; border-radius: 5px; margin-top: 20px;">{code}</div>
            <p style="font-size: 16px; margin-top: 20px;">This code is valid for <strong>10 minutes</strong>.</p>
        </div>

        <!-- Footer -->
        <div style="text-align: center; font-size: 12px; color: #999999; margin-top: 30px; padding-bottom: 20px;">
            <p style="margin: 0;">WiderAI Team</p>
        </div>

        <!-- Location -->
        <div style="padding: 20px; background-color: rgba(223, 220, 220, 0.5);">
            <h1 style="font-family: Georgia, 'Times New Roman', Times, serif; font-size: 17px; margin: 0;">
                Catering is a service developed by <a href="https://www.widerai.us" style="color: blue; text-decoration: none;">WiderAI, Inc</a>
            </h1>
            <h5 style="font-family: Arial, Helvetica, sans-serif; margin: 0; font-size: 13px; font-weight: 400; padding: 5px 0 10px;">
                Riyadh, Saudia Arabia.
            </h5>
            <a href="https://www.widerai.us/support" style="font-size: 15px; color: blue;">Help & Support</a>
        </div>
    </div>
</body>
</html>
"""