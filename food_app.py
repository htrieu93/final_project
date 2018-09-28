import mlab
from datetime import *
from flask import *
from mongoengine import *
from models.recipe import Recipe
from models.customer import Customer
from models.user import User
from models.order import Order
from gmail import GMail, Message

app = Flask(__name__)
app.secret_key = 'a super super secret key'
mlab.connect()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/<str:ing>')
def search(Ing):
    all_service = Recipe.objects(
        gender = g, 
        # yob__lte = 1998, 
        # height__gte = 165,
        # address__icontains = "Hanoi" 
    )

    return render_template(
        'search.html',
        all_service = all_service
    )

@app.route('/user/<int:g>')
def user(g):
    all_customer = user.objects[:10](
        gender = g,
        contacted = False
    )

    return render_template(
        'customer.html',
        all_user = all_user
    )

@app.route('/admin')
def admin():
    all_service = Service.objects()
    return render_template(
        'admin.html', all_service = all_service
    )

@app.route('/delete/<recipe_id>')
def delete(service_id):
    recipe = Recipe.objects.with_id(recipe_id)
    if recipe is not None:
        recipe.delete()
        return redirect(url_for('user'))
    else:
        return "ID not found"

@app.route('/new-recipe', methods = ['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('new-recipe.html')
    elif request.method == 'POST':
        form = request.form
        name = form['name']
        servings = form['servings']
        time = form['time']
        ingredients = form['ingredients']

        new_recipe = Recipe(
            name = name,
            servings = servings,
            time = time,
            ingredients = ingredients
        )
        new_recipe.save()

        return redirect(url_for('user'))

@app.route('/detail/<service_id>')
def detail(service_id):
    service = Service.objects.with_id(service_id)
    session['service_id'] = service_id
    if 'loggedin' in session:
        if session['loggedin'] == True:
            return render_template('detail.html', service = service)
        else:  
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    
@app.route('/update_recipe/<recipe_id>', methods = ['GET', 'POST'])
def update_recipe(recipe_id):
    recipe = Recipe.objects.with_id(Recipe_id)
    if request.method == 'GET':
        return render_template('update_service.html', recipe = recipe)
    elif request.method == 'POST':

        form = request.form
        
        #mongoengine_update
        service.update(name = form['name'])
        service.update(yob = form['yob'])
        service.update(phone = form['phone'])
        service.update(descriptions = form['descriptions'])
        service.update(measurements = form['measurements'])
        service.save()

        return redirect(url_for('user'))

@app.route('/sign_in', methods = ['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('sign_in.html')
    elif request.method == 'POST':
        form = request.form
        
        if form['fullname'] == '':
            fullname = ''
        else:
            fullname = form['fullname']
        
        if form['email'] == '':
            email = ''
        else:
            email = form['email']
            
        username = form['username']
        password = form['password']
        
        new_user = User(
            username = username,
            password = password,
            email = email,
            fullname = fullname
        )
        new_user.save()
        
        return "User created"

# @app.route('/login', methods = ['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     elif request.method == 'POST':
#         form = request.form
#         username = form['username']
#         password = form['password']

#         found_user = User.objects(
#             username = username,
#             password = password
#         )
        
#         if form['login'] == 'Login':
#             if found_user != None:
#                 session['loggedin'] = True
#                 service_id = session['service_id']
#                 session['user_id'] = str(found_user.first().id)
#                 return redirect(url_for('detail', service_id = service_id))
#             else:
#                 return "User does not exist. Please try again."
#         elif form['login'] == 'Đăng Ký':
#             return redirect(url_for('sign_in'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        form = request.form
        username = form["username"]
        password = form["password"]
        login = form["login"]
        if login == "Login":
            if username == "admin" and password == "admin":
                session["loggedin"]=True
                return redirect(url_for("admin")) #hay submit page idk
            else:
                return "Viết admin trước dồi tính"
        elif login == "Đăng Ký":
            return redirect(url_for("sign_in"))

@app.route('/order')
def order():
    new_order = Order(
        service_id = session['service_id'],
        user_id = session['user_id'],
        time = datetime.now(),
        is_accepted = False
    )
    new_order.save()

    return "Đã gửi yêu cầu"

@app.route('/order_page')
def order_page():
    all_orders = Order.objects()
    return render_template('order_page.html', all_orders = all_orders)

@app.route('/update_is_accepted/<order_id>')
def update_is_accepted(order_id):
    order = Order.objects.with_id(order_id)
    email = "'" + str(order.user_id.username) + "<" + str(order.user_id.email) + ">'"
    password = order.user_id.password
    order.update(is_accepted = True)
    gmail = GMail(email,password)
    msg = Message(
    "Xét duyệt yêu cầu - Mùa Đông Không Lạnh",
    to=email,
    text= 'Yêu cầu của bạn đã được xử lý, chúng tôi sẽ liên hệ với bạn trong thời gian sớm nhất. Cảm ơn bạn đã sử dụng dịch vụ của ‘Mùa Đông Không Lạnh’')
    gmail.send(msg)

    return redirect(url_for('order'))

@app.route('/logout')
def logout():
    session['loggedin'] = False
    return redirect(url_for('index'))

if __name__ == '__main__':
  app.run(debug=True)
 