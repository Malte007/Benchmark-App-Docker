from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///benchmark.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    hardware = db.Column(db.String(200))
    oc = db.Column(db.String(100))
    benchmarks = db.relationship('Benchmark', backref='system', cascade="all, delete-orphan")

class BenchmarkType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    benchmarks = db.relationship('Benchmark', backref='benchmark_type', cascade="all, delete-orphan")

class Benchmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    system_id = db.Column(db.Integer, db.ForeignKey('system.id'), nullable=False)
    benchmark_type_id = db.Column(db.Integer, db.ForeignKey('benchmark_type.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/edit_system/<int:system_id>", methods=["GET", "POST"])
def edit_system(system_id):
    system = System.query.get_or_404(system_id)

    if request.method == "POST":
        system.name = request.form["name"]
        system.hardware = request.form.get("hardware", "")
        system.oc = request.form.get("oc", "")
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("edit_system.html", system=system)


@app.route("/", methods=["GET", "POST"])
def index():
    benchmark_types = BenchmarkType.query.all()
    selected_type_id = None
    benchmarks = []

    if request.method == "POST":
        selected_type_id = request.form.get("benchmark_type")
        if selected_type_id:
            benchmarks = Benchmark.query \
                .filter_by(benchmark_type_id=selected_type_id) \
                .order_by(Benchmark.score.desc()) \
                .all()

    return render_template(
        "index.html",
        benchmark_types=benchmark_types,
        selected_type_id=selected_type_id,
        benchmarks=benchmarks
    )


@app.route('/add_system', methods=['GET', 'POST'])
def add_system():
    if request.method == 'POST':
        name = request.form['name']
        hardware = request.form['hardware']
        oc = request.form['oc']
        new_system = System(name=name, hardware=hardware, oc=oc)
        db.session.add(new_system)
        db.session.commit()
        return redirect(url_for('index'))
    systems = System.query.all()
    return render_template('add_system.html', systems=systems)

@app.route('/delete_system/<int:system_id>')
def delete_system(system_id):
    system = System.query.get_or_404(system_id)
    db.session.delete(system)
    db.session.commit()
    return redirect(url_for('add_system'))

@app.route('/add_benchmark_type', methods=['GET', 'POST'])
def add_benchmark_type():
    if request.method == 'POST':
        name = request.form['name']
        new_type = BenchmarkType(name=name)
        db.session.add(new_type)
        db.session.commit()
        return redirect(url_for('index'))
    types = BenchmarkType.query.all()
    return render_template('add_benchmark_type.html', types=types)

@app.route('/delete_benchmark_type/<int:type_id>')
def delete_benchmark_type(type_id):
    b_type = BenchmarkType.query.get_or_404(type_id)
    db.session.delete(b_type)
    db.session.commit()
    return redirect(url_for('add_benchmark_type'))

@app.route('/add_benchmark', methods=['GET', 'POST'])
def add_benchmark():
    systems = System.query.all()
    benchmark_types = BenchmarkType.query.all()
    if request.method == 'POST':
        system_id = request.form['system_id']
        benchmark_type_id = request.form['benchmark_type_id']
        score = request.form['score']
        new_benchmark = Benchmark(score=score, system_id=system_id, benchmark_type_id=benchmark_type_id)
        db.session.add(new_benchmark)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_benchmark.html', systems=systems, benchmark_types=benchmark_types)

@app.route('/delete_benchmark/<int:benchmark_id>')
def delete_benchmark(benchmark_id):
    benchmark = Benchmark.query.get_or_404(benchmark_id)
    db.session.delete(benchmark)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

