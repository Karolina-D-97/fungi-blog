from flask import Flask, render_template, request
import requests
import smtplib

url = 'https://api.npoint.io/965a93bbc326c42d8c9e'
blog_response = requests.get(url)
posts = blog_response.json()

FROM_EMAIL = ""
TO_EMAIL = ""
OWN_PASSWORD = ""

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html", all_posts=posts)


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone_number"]
        message = request.form["message"]
        send_email(name, email, phone, message)
        return "Successfully sent your message"
    return render_template("contact.html")

@app.route('/post/<int:index>')
def show_post(index):
    post = posts[index-1]
    return render_template('post.html', post=post)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(FROM_EMAIL, OWN_PASSWORD)
        connection.sendmail(FROM_EMAIL, TO_EMAIL, email_message)

if __name__ == "__main__":
    app.run(debug=True)
