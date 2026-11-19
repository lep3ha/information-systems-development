from flask import Blueprint, render_template, request, flash
from auth.access import login_required, group_required
from .models import queries_model

queries_bp = Blueprint('queries', __name__, template_folder='templates')

@queries_bp.route('/', methods=['GET', 'POST'])
@login_required
@group_required
def query_handler():
    if request.method == 'GET':
        return render_template('input_category.html')
    else:
        category_id = request.form.get('category_id', '').strip()

        products = queries_model.get_products_by_category(category_id)

        if products:
            return render_template('query_results.html',
                                   title='Товары по категории',
                                   results=products)
        else:
            flash('Товары по указанной категории не найдены')
            return render_template('input_category.html')