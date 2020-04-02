from flask import Flask, render_template, request
import pyrebase

app = Flask(__name__)

# tengin við firebase realtime database á firebase.google.com ( db hjá danielsimongalvez@gmail.com )
config = {
    # hér kemur tengingin þín við Firebase gagnagrunninn ( realtime database )
	"apiKey": "AIzaSyCKiGgLLFzUcYxG_Xy6x1ZJrj-0ig6ahf0",
    "authDomain": "verk5-e1eff.firebaseapp.com",
    "databaseURL": "https://verk5-e1eff.firebaseio.com",
    "projectId": "verk5-e1eff",
    "storageBucket": "verk5-e1eff.appspot.com",
    "messagingSenderId": "14078416837",
    "appId": "1:14078416837:web:dd19239f9e7fb73c31ddac",
    "measurementId": "G-79ZDKJ0TTR"

}

fb = pyrebase.initialize_app(config)
db = fb.database()

# Test route til að setja gögn í db
@app.route('/')
def index():
	return render_template("index.html")

@app.route('/info', methods=['GET', 'POST'])
def info():
	check = False
	y = 0
	if request.method == 'POST':
		notendanafn = request.form['notendanafn']
		lykilord = request.form['lykilord']
		u = db.child("notandi").get().val()
		lst = list(u.items())
		for x in range(len(lst)):
			if lst[y][1]["notendanafn"] == notendanafn:
				y += 1
				print(lst[y][1]["notendanafn"])
				check = False
				break
			elif lst[y][1]["notendanafn"] != notendanafn:
				print(lst[y][1]["notendanafn"])
				check = True
				y+=1
		if check == True:
			db.child("notandi").push({"notendanafn":notendanafn, "lykilorð":lykilord}) 
			ola = "Velkominn á síðuna " + notendanafn + " <a href='/'>smeltu hér til að fara til baka</a>"
			return ola
		else:
			return "Þetta notendanafn er nú þegar í notkun,<a href='/'>vinsamlegast reyndu aftur</a>"
	else:
		return "<h1>Má ekki</h1>"
		
@app.route('/info2', methods=['GET', 'POST'])
def info2():
	check = False
	y = 0
	if request.method == 'POST':
		notendanafn = request.form['notendanafn']
		lykilord = request.form['lykilord']
		u = db.child("notandi").get().val()
		lst = list(u.items())
		for x in range(len(lst)):
			if lst[y][1]["notendanafn"] == notendanafn:
				if lst[y][1]["lykilorð"] == lykilord:
					y += 1
					check = True
					break
			elif lst[y][1]["notendanafn"] != notendanafn:
				check = False
				y+=1
		if check == True:
			ola = "Velkominn á síðuna " + notendanafn + " <a href='/'>smeltu hér til að fara til baka</a>"
			return ola
		else:
			return "Þetta notendanafn er ekki til,<a href='/'>vinsamlegast reyndu aftur</a>"
	else:
		return "<h1>Má ekki</h1>"



@app.route('/signupp')
def signupp():
	return render_template("signupp.html")


# Test route til að sækja öll gögn úr db
@app.route('/lesa')
def lesa():
	u = db.child("notandi").get().val()
	lst = list(u.items())
	print(lst)
	print(lst[0][1]["notendanafn"])
	print(len(lst))
	return "Lesum úr grunni"

if __name__ == "__main__":
	app.run(debug=True)

# skrifum nýjan í grunn hnútur sem heitir notandi 
# db.child("notandi").push({"notendanafn":"dsg", "lykilorð":1234}) 

# # förum í grunn og sækjum allar raðir ( öll gögn )
# u = db.child("notandi").get().val()
# lst = list(u.items())