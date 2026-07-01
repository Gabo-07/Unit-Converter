from flask import Flask, render_template, request

app = Flask(__name__)

# Tasas de conversión usando una unidad base (metro para longitud, gramo para peso)
length_rates = {
    'millimeter': 0.001,
    'centimeter': 0.01,
    'meter': 1.0,
    'kilometer': 1000.0,
    'inch': 0.0254,
    'foot': 0.3048,
    'yard': 0.9144,
    'mile': 1609.344
}

weight_rates = {
    'milligram': 0.001,
    'gram': 1.0,
    'kilogram': 1000.0,
    'ounce': 28.3495,
    'pound': 453.592
}

def convert_linear(value, from_unit, to_unit, rates):
    if from_unit not in rates or to_unit not in rates:
        return None
    # Convertimos primero a la unidad base, y de ahí a la unidad de destino
    base_value = value * rates[from_unit]
    result = base_value / rates[to_unit]
    return result

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    
    # Convertimos primero a Celsius
    celsius = value
    if from_unit == 'Fahrenheit':
        celsius = (value - 32) * 5/9
    elif from_unit == 'Kelvin':
        celsius = value - 273.15
        
    # Y de Celsius a la unidad de destino
    if to_unit == 'Fahrenheit':
        return (celsius * 9/5) + 32
    elif to_unit == 'Kelvin':
        return celsius + 273.15
        
    return celsius

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    active_tab = 'length'
    
    # Este diccionario guardará lo que el usuario escribió para no borrarlo al recargar
    form_data = {
        'value': '',
        'from_unit': '',
        'to_unit': '',
        'category': 'length'
    }

    if request.method == 'POST':
        try:
            value = float(request.form.get('value', 0))
            from_unit = request.form.get('from_unit')
            to_unit = request.form.get('to_unit')
            category = request.form.get('category')
            
            form_data = {
                'value': value,
                'from_unit': from_unit,
                'to_unit': to_unit,
                'category': category
            }
            active_tab = category

            if category == 'length':
                res = convert_linear(value, from_unit, to_unit, length_rates)
            elif category == 'weight':
                res = convert_linear(value, from_unit, to_unit, weight_rates)
            elif category == 'temperature':
                res = convert_temperature(value, from_unit, to_unit)
            else:
                res = None

            if res is not None:
                # Formateamos el resultado: 4 decimales y quitamos ceros inútiles a la derecha
                result = f"{res:.4f}".rstrip('0').rstrip('.')

        except ValueError:
            result = "Error: Por favor ingresa un número válido."

    return render_template('index.html', result=result, active_tab=active_tab, form_data=form_data)

if __name__ == '__main__':
    # Arranca el servidor local
    app.run(debug=True)
