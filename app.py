import mlab
# import humanize
from datetime import datetime
from pymongo import *
from flask import *
from mongoengine import *
from models.all_classes import Recipe, Comment, User
from random import sample
# from models.user import User, Comment
# from gmail import GMail, Message

app = Flask(__name__)
app.secret_key = 'a super super secret key'
mlab.connect()
client = MongoClient('mongodb://htrieu:prototype101@ds263832.mlab.com:63832/final_project_c4e20')
db = client['final_project_c4e20']

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'GET':
        recipes = []
        re_query = db.recipe.find().sort('upvote',DESCENDING).limit(8)
        for recipe in re_query:
            recipes.append(recipe)
        return render_template('index.html', recipes = recipes)
    elif request.method == 'POST':
        form = request.form
        if 'search' in form:
            ingredients = form['ingredients']
            return redirect(url_for('search', ingredients = ingredients))
        elif 'new-recipe' in form:
            return redirect(url_for('new_recipe'))

@app.route('/search/<string:ingredients>')
def search(ingredients):
    ingredients_list = ingredients.split(',')
    # client = MongoClient('mongodb://htrieu:prototype101@ds263832.mlab.com:63832/final_project_c4e20')
    # db = client['final_project_c4e20']
    all_recipe = []
    col = db.recipe.find().sort('upvote',DESCENDING)
    for doc in col:
        ing = doc['ingredients']
        count = 0
        for item in ingredients_list:
            item = item.strip()
            l = [x for x in ing if (item in x or item == x)]
            if len(l) != 0:
                count += 1 
        if count == len(ingredients_list):
            all_recipe.append(doc)

    return render_template(
        'search.html',
        all_recipe = all_recipe
    )

@app.route('/user/')
def user():
    all_user = User.objects()

    return render_template(
        'user.html',
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
def new_recipe():
    if request.method == 'GET':
        return render_template('new-recipe.html')
    elif request.method == 'POST':
        form = request.form
        name = form['name']
        servings = form['servings']
        time_of_day = form['time_of_day']
        ingredients = form['ingredients'] #aa,bb
        ingredients = ingredients.split(",")
        ingredients = [i.strip() for i in ingredients]
        difficulty = form['difficulty']
        instructions = form['instructions']

        new_recipe = Recipe(
            name = name,
            servings = servings,
            ingredients = ingredients,
            difficulty = difficulty,
            time_of_day = time_of_day,
            instructions = instructions
        )
        new_recipe.save()

    if 'loggedin' in session:
        if session['loggedin'] == True:
            return redirect(url_for('user'))
        else:  
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/detail/<recipe_id>', methods = ['GET', 'POST'])
def detail(recipe_id):
    # print(User.objects.filter(comment_id__contains = '5bb4bb555f029f0c88021245'))
    session['recipe_id'] = recipe_id
    recipe = Recipe.objects.with_id(recipe_id)
    recipe_comment_list = []
    for recipe_comment in recipe.comment_id:
        recipe_comment_list.append(recipe_comment.id)
    comments = Comment.objects.filter(id__in = recipe_comment_list).order_by('time')
    form = request.form
    user_comment_list = []
    for comment in comments:
        user_comment = User.objects.filter(comment_id__contains = comment.id)
        if len(user_comment) > 0:
            user_comment_dict = {
                "content": comment.body,
                "time": timesince(comment.time),
                "user": user_comment[0].username
            }
            user_comment_list.append(user_comment_dict)
    if request.method == 'GET':
        return render_template('detail.html', recipe = recipe, user_comment_list = user_comment_list)
    elif request.method == 'POST':
        if 'loggedin' in session:
            if session['loggedin'] == True:
                if 'comment' in request.form:
                    user = User.objects.with_id(session['user_id'])
                    new_comment = Comment(
                        time = datetime.now(),
                        body = form['body']
                    )
                    new_comment.save()
                    new_comment.reload()
                    recipe.update(push__comment_id = new_comment)
                    user.update(push__comment_id = new_comment)
                    user_comment = User.objects.filter(comment_id__contains = new_comment.id)
                    return redirect(url_for('detail.html', recipe = recipe, user_comment_list = user_comment_list))
                elif 'update' in request.form:
                    return redirect(url_for('update_recipe', recipe_id = recipe_id))
            else:  
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
        
    
@app.route('/update_recipe/<recipe_id>', methods = ['GET', 'POST'])
def update_recipe(recipe_id):
    recipe = Recipe.objects.with_id(recipe_id)
    if request.method == 'GET':
        return render_template('update_recipe.html', recipe = recipe)
    elif request.method == 'POST':

        form = request.form
        
        #mongoengine_update
        recipe.update(name = form['name'])
        recipe.update(servings = form['servings'])
        recipe.update(difficulty = form['difficulty'])
        recipe.update(time_of_day = form['time_of_day'])
        recipe.update(ingredients = form['ingredients'])
        recipe.update(instructions = form['instructions'])
        recipe.save()

        return redirect(url_for('user'))

@app.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')
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
        
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        form = request.form
        username = form["username"]
        password = form["password"]
        
        found_user = User.objects(
            username = username,
            password = password
        )

        # Gop Admin va User login
        if form['login'] == "Login":
            if username == "admin" and password == "admin":
                session["loggedin"] = True
                return redirect(url_for("admin")) #hay submit page idk
            elif found_user != None:
                session['loggedin'] = True
                recipe_id = session['recipe_id']
                session['user_id'] = str(found_user.first().id)
                return redirect(url_for('detail', recipe_id = recipe_id))
            else:
                return "User does not exist. Please try again."
        elif form['login'] == "Sign up":
            return redirect(url_for("sign_up"))

@app.route('/order_page')
def order_page():
    all_orders = Order.objects()
    return render_template('order_page.html', all_orders = all_orders)

# @app.route('/update_is_accepted/<order_id>')
# def update_is_accepted(order_id):
#     order = Order.objects.with_id(order_id)
#     email = "'" + str(order.user_id.username) + "<" + str(order.user_id.email) + ">'"
#     password = order.user_id.password
#     order.update(is_accepted = True)
#     gmail = GMail(email,password)
#     msg = Message(
#     "Xét duyệt yêu cầu - Mùa Đông Không Lạnh",
#     to=email,
#     text= 'Yêu cầu của bạn đã được xử lý, chúng tôi sẽ liên hệ với bạn trong thời gian sớm nhất. Cảm ơn bạn đã sử dụng dịch vụ của ‘Mùa Đông Không Lạnh’')
#     gmail.send(msg)

#     return redirect(url_for('order'))

@app.route('/logout')
def logout():
    session['loggedin'] = False
    return redirect(url_for('index'))

@app.template_filter()
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.utcnow()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default

if __name__ == '__main__':
  app.run(debug=True)
 