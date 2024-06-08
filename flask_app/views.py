# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            if account is not None:
                login(request, account)
                return redirect('insert_recipe')
            else:
                return render(request, 'register.html', {'form': form, 'error': 'Authentication failed'})
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        account = authenticate(email=email, password=password)
        if account is not None:
            login(request, account)
            return redirect('insert_recipe')
        else:
            return render(request, 'Login.html', {'error': 'Invalid email or password'})
    else:
        return render(request, 'Login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'home.html')





# ... (Other Django imports if necessary)

from django.shortcuts import  redirect
from django.contrib.auth.decorators import login_required
from .forms import SearchRecipeForm, RecipeForm

@login_required
def insert_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)  # Create object but don't save yet
            recipe.user = request.user  # Assign the logged-in user
            recipe.save()
            return redirect('insert_recipe') # Redirect to a success page
    else:
        form = RecipeForm()
    return render(request, 'RecipeMake.html', {'form': form})

@login_required
def search_recipe(request):
    if request.method == 'GET':
        form = SearchRecipeForm(request.GET)
        if form.is_valid():
            word1 = form.cleaned_data.get('word1')
            word2 = form.cleaned_data.get('word2')
            word3 = form.cleaned_data.get('word3')
            dishtime = form.cleaned_data.get('dishtime')

            # Start with all recipes belonging to the logged-in user
            recipes = Recipe.objects.all()

            if word1:
                recipes = recipes.filter(ProductOtherProducts__icontains=word1)
            if word2:
                recipes = recipes.filter(ProductOtherProducts__icontains=word2)
            if word3:
                recipes = recipes.filter(ProductOtherProducts__icontains=word3)
            if dishtime:
                recipes = recipes.filter(DishTime__icontains=dishtime)

            context = {'recipes': recipes, 'form': form}
            return render(request, 'searchRecipe.html', context)
    else:
        form = SearchRecipeForm()

    context = {'form': form}
    return render(request, 'searchRecipe.html', context)

  # Make sure to import your Specials model

# views.py

@login_required
def home(request):
    """Displays a list of the logged-in user's recipes."""

    recipes = Recipe.objects.filter(user=request.user)
    context = {'recipes': recipes}
    return render(request, 'user_recipes.html', context)

from .models import Recipe

from django.shortcuts import render
from .models import RankedProductPricess
from django.db import connection
@login_required
def search_prices(request, recipe_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH SplitProducts AS (
                SELECT
                    r.id AS recipe_id,
                    TRIM(regexp_split_to_table(r."ProductOtherProducts", ',')) AS product
                FROM
                    flask_app_recipe r
            ),
            MatchedProducts AS (
                SELECT
                    sp.recipe_id,
                    sp.product,
                    s."ProductNameType",
                    s."ProductPrice",
                    similarity(sp.product, s."ProductNameType") AS similarity_score
                FROM
                    SplitProducts sp
                JOIN
                    flask_app_specials s
                ON
                    similarity(sp.product, s."ProductNameType") > 0.1  -- Adjust the threshold as needed
            ),
            RankedMatches AS (
                SELECT
                    mp.recipe_id,
                    mp.product,
                    mp."ProductNameType",
                    mp."ProductPrice",
                    ROW_NUMBER() OVER (PARTITION BY mp.recipe_id, mp.product ORDER BY mp.similarity_score DESC, mp."ProductPrice" ASC) as rank_num
                FROM
                    MatchedProducts mp
            )
            SELECT 
                rm.product,
                rm."ProductNameType",
                rm."ProductPrice"
            FROM 
                RankedMatches rm
            WHERE
                rm.rank_num = 1 AND rm.recipe_id = %s;
        """, [recipe_id])  # Pass recipe_id as a parameter
        prices = cursor.fetchall()

    context = {'prices': prices}
    return render(request, 'index.html', context)