from flask import Blueprint, render_template, request
from app.data.forms import CatalogFilterForm, SuppliersFilterForm, InvoicesFilterForm
from app.data.model import FetchModel
from app.auth.access import permission_required

data = Blueprint("data", __name__, template_folder="templates")
fetch_model = FetchModel()

@data.route("/", methods=["GET"])
@permission_required(["monitoring_viewer"])
def index():
    return render_template("data/monitoring.html", title="Мониторинг данных")

@data.route("/catalog", methods=["GET", "POST"])
@permission_required(["catalog_viewer"])
def catalog():
    form = CatalogFilterForm()
    items = []
    columns = []
    
    # Получаем доступные категории для выпадающего списка
    categories_result = fetch_model.get_categories()
    if categories_result['status']:
        form.category.choices = [("", "Все")] + [(m['category'], m['category']) 
                                                for m in categories_result['data']]
    
    if request.method == "POST":
        # Собираем параметры фильтрации
        params = {
            "category": form.category.data or "",
            "min_price": float(form.min_price.data) if form.min_price.data else 0,
            "max_price": float(form.max_price.data) if form.max_price.data else 0,
            "sort_by": form.sort_by.data or "name_asc"
        }
        
        # Получаем товары с фильтрацией
        result = fetch_model.get_products(params)
        print(result)
        if result['status']:
            items = result['data']
            if items:
                columns = list(items[0].keys())  # Получаем названия колонок из первого элемента
    
    return render_template("data/catalog.html", 
                         form=form, 
                         items=items, 
                         columns=columns,
                         title="Каталог заготовок")


@data.route("/suppliers", methods=["GET", "POST"])
@permission_required(["suppliers_viewer"])
def suppliers():
    form = SuppliersFilterForm()    
    suppliers = []
    columns = []
    
    # Заполняем список городов
    cities_result = fetch_model.get_cities()
    if cities_result['status']:
        cities = [("", "Все")] + [(city['city'], city['city']) for city in cities_result['data']]
        form.city.choices = cities
    
    # Применяем фильтры
    if request.method == "POST":
        filter_params = {
            'city': form.city.data or "",
            'min_contract_date': form.min_contract_date.data,
            'max_contract_date': form.max_contract_date.data,
            'sort_by': form.sort_by.data or "name_asc"
        }
    
        result = fetch_model.get_suppliers(filter_params)
        if result['status']:
            suppliers = result['data']
            if suppliers:
                columns = list(suppliers[0].keys()) 
    
    return render_template('data/suppliers.html',
                         form=form,
                         suppliers=suppliers,
                         columns=columns)

@data.route("/invoices", methods=["GET", "POST"])
@permission_required(["invoices_viewer"])
def invoices():
    form = InvoicesFilterForm()
    invoices = []
    columns = []
    
    # Заполняем список поставщиков
    suppliers_result = fetch_model.get_suppliers_list()
    if suppliers_result['status']:
        form.supplier_id.choices = suppliers_result['data']
    

    if request.method == "POST":
        filter_params = {
            'supplier_id': form.supplier_id.data,
            'min_delivery_date': form.min_delivery_date.data,
            'max_delivery_date': form.max_delivery_date.data,
            'min_total_cost': float(form.min_total_cost.data) if form.min_total_cost.data else 0,
            'max_total_cost': float(form.max_total_cost.data) if form.max_total_cost.data else 0,
            'sort_by': form.sort_by.data
        }
    
        result = fetch_model.get_invoices(filter_params)
        if result['status']:
            invoices = result['data']
            if invoices:
                columns = list(invoices[0].keys())
    
    return render_template('data/invoices.html',
                         form=form,
                         invoices=invoices,
                         columns=columns)