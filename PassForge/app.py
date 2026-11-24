from flask import Flask, request, render_template
import joblib
import random
import string
import pandas as pd

app = Flask(__name__, template_folder="templates")

model = joblib.load("SVM_Model.pkl")
scaler = joblib.load("scaler.pkl")

def extract_features(p):
    return [[
        len(p),
        sum(c.isupper() for c in p),
        sum(c.islower() for c in p),
        sum(not c.isalnum() for c in p),
        sum(c.isdigit() for c in p)
    ]]

@app.route("/")
def home():
    return render_template("index.html", active_tab="about")

@app.route("/generate", methods=["POST"])
def generate():
    name = request.form.get("name", "")
    word = request.form.get("word", "")
    number = request.form.get("number", "")
    
    base = word + name[:2] + str(number)
    
    leetspeak = {'a':'@','e':'3','i':'1','o':'0','s':'$','t':'7','A':'@','E':'3','I':'1','O':'0','S':'$','T':'7'}
    
    password = ""
    for char in base:
        if char in leetspeak and random.choice([True, False]):
            password += leetspeak[char]
        else:
            password += char
            
    if len(password) < 10:
        password += "".join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=10 - len(password)))
    elif len(password) > 14:
        password = password[:14]
        
    chars = list(password)
    
    if not any(c.isupper() for c in chars):
        chars[0] = random.choice(string.ascii_uppercase)
    if not any(c.islower() for c in chars):
        chars[-1] = random.choice(string.ascii_lowercase)
    if not any(c.isdigit() for c in chars):
        chars[1 % len(chars)] = random.choice(string.digits)
    if not any(not c.isalnum() for c in chars):
        chars[2 % len(chars)] = random.choice("!@#$%^&*")
        
    password = "".join(chars)
        
    return render_template("index.html", generated_password=password, gen_name=name, gen_word=word, gen_number=number, active_tab="generator")

@app.route("/check", methods=["POST"])
def check():
    password = request.form.get("password", "")
    if not password:
        return render_template("index.html", active_tab="analyzer")
        
    features = extract_features(password)
    df = pd.DataFrame(features, columns=["Length", "No_of_Capital", "No_of_Small", "No_of_Special", "No_of_Numbers"])
    
    scaled_features = scaler.transform(df)
    
    pred = model.predict(scaled_features)[0]
    
    strength_result = "Strong Password" if pred == 1 else "Weak Password"
    return render_template("index.html", strength_result=strength_result, checked_password=password, active_tab="analyzer")

if __name__ == "__main__":
    app.run(debug=True)