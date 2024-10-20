from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret_key'  # Clave secreta para usar sesiones

# Ruta inicial para mostrar el formulario de registro
@app.route('/', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtener datos del formulario
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        turno = request.form['turno']
        seminarios = request.form.getlist('seminarios')

        # Crear una lista de inscritos si no existe
        if 'inscritos' not in session:
            session['inscritos'] = []

        # Agregar el nuevo registro a la lista de inscritos
        session['inscritos'].append({
            'fecha': fecha,
            'nombre': nombre,
            'apellidos': apellidos,
            'turno': turno,
            'seminarios': ', '.join(seminarios)
        })
        session.modified = True  # Marcar la sesión como modificada

        return redirect(url_for('listado_inscritos'))

    return render_template('nuevo.html')

# Ruta para mostrar el listado de inscritos
@app.route('/listado')
def listado_inscritos():
    inscritos = session.get('inscritos', [])
    return render_template('index.html', inscritos=inscritos)

# Ruta para editar un inscrito
@app.route('/editar/<int:index>', methods=['GET', 'POST'])
def editar(index):
    inscritos = session.get('inscritos', [])

    # Comprobar que el índice es válido
    if index < 0 or index >= len(inscritos):
        return "Error: El inscrito no existe", 404

    if request.method == 'POST':
        # Actualizar los datos del inscrito
        inscritos[index]['fecha'] = request.form['fecha']
        inscritos[index]['nombre'] = request.form['nombre']
        inscritos[index]['apellidos'] = request.form['apellidos']
        inscritos[index]['turno'] = request.form['turno']
        inscritos[index]['seminarios'] = ', '.join(request.form.getlist('seminarios'))

        session['inscritos'] = inscritos  # Actualizar la lista de inscritos en la sesión
        return redirect(url_for('listado_inscritos'))

    inscrito = inscritos[index]
    return render_template('editar.html', inscrito=inscrito, index=index)

# Ruta para eliminar un inscrito
@app.route('/eliminar/<int:index>')
def eliminar(index):
    inscritos = session.get('inscritos', [])
    inscritos.pop(index)  # Eliminar el inscrito de la lista
    session['inscritos'] = inscritos  # Actualizar la sesión
    return redirect(url_for('listado_inscritos'))

# Ruta para reiniciar el registro y agregar uno nuevo
@app.route('/nuevo')
def nuevo_registro():
    return redirect(url_for('registro'))

if __name__ == '__main__':
    app.run(debug=True)
