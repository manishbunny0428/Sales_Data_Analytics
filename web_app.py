
from flask import Flask, render_template_string
import pandas as pd
import json

app = Flask(__name__)

def get_data():
    df = pd.read_csv("sales_data.csv")
    df["Revenue"] = df["Quantity"] * df["Price"]

    revenue = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
    quantity = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)

    return df, revenue, quantity

@app.route("/")
def dashboard():
    df, revenue, quantity = get_data()

    total_revenue = float(df["Revenue"].sum())
    total_orders = len(df)
    average_revenue = total_revenue / total_orders if total_orders else 0

    table = df.to_html(index=False, classes="data-table", border=0)
    ranking = revenue.rename("Total Revenue").reset_index()
    ranking.insert(0, "Rank", range(1, len(ranking) + 1))
    ranking_html = ranking.to_html(index=False, classes="data-table", border=0, float_format=lambda x: f"{x:,.2f}")

    chart_labels = json.dumps(revenue.index.tolist())
    revenue_values = json.dumps([float(x) for x in revenue.values])
    quantity_labels = json.dumps(quantity.index.tolist())
    quantity_values = json.dumps([int(x) for x in quantity.values])

    best_selling = quantity.idxmax() if not quantity.empty else "N/A"
    highest_revenue = revenue.idxmax() if not revenue.empty else "N/A"
    lowest_revenue = revenue.idxmin() if not revenue.empty else "N/A"

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Sales Data Analytics Dashboard</title>
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      <style>
        * { box-sizing: border-box; }
        body { margin: 0; font-family: Arial, sans-serif; background: #0b1f3a; color: #f8fafc; }
        header { padding: 28px 5%; background: #10294b; }
        h1 { margin: 0 0 8px; color: #38bdf8; }
        .container { max-width: 1250px; margin: auto; padding: 25px; }
        .cards { display: grid; grid-template-columns: repeat(auto-fit,minmax(200px,1fr)); gap: 18px; }
        .card, .panel { background: #142e50; padding: 22px; border-radius: 14px; margin-bottom: 22px; }
        .metric { font-size: 28px; font-weight: bold; color: #34d399; margin-top: 12px; }
        .charts { display: grid; grid-template-columns: repeat(auto-fit,minmax(300px,1fr)); gap: 20px; }
        .chart-wrap { height: 320px; }
        h2 { color: #38bdf8; }
        .table-wrap { overflow-x: auto; max-height: 420px; }
        table { border-collapse: collapse; width: 100%; background: #10294b; }
        th, td { text-align: left; padding: 10px; border-bottom: 1px solid #294665; white-space: nowrap; }
        th { color: #38bdf8; position: sticky; top: 0; background: #10294b; }
        li { margin: 12px 0; }
        @media(max-width:600px) { .container { padding: 14px; } header { padding: 22px 14px; } }
      </style>
    </head>
    <body>
      <header>
        <h1>📊 Sales Data Analytics Dashboard</h1>
        <p>Analyze sales performance and discover business insights.</p>
      </header>
      <main class="container">
        <section class="cards">
          <div class="card"><div>Total Revenue</div><div class="metric">₹{{ "%.2f"|format(total_revenue) }}</div></div>
          <div class="card"><div>Total Orders</div><div class="metric">{{ total_orders }}</div></div>
          <div class="card"><div>Average Revenue</div><div class="metric">₹{{ "%.2f"|format(average_revenue) }}</div></div>
        </section>

        <section class="panel">
          <h2>Sales Data</h2>
          <div class="table-wrap">{{ table|safe }}</div>
        </section>

        <section class="charts">
          <div class="panel"><h2>Revenue by Product</h2><div class="chart-wrap"><canvas id="revenueChart"></canvas></div></div>
          <div class="panel"><h2>Quantity Sold by Product</h2><div class="chart-wrap"><canvas id="quantityChart"></canvas></div></div>
          <div class="panel"><h2>Revenue Contribution</h2><div class="chart-wrap"><canvas id="pieChart"></canvas></div></div>
        </section>

        <section class="panel">
          <h2>Product Revenue Ranking</h2>
          <div class="table-wrap">{{ ranking_html|safe }}</div>
        </section>

        <section class="panel">
          <h2>💡 Business Insights</h2>
          <ul>
            <li><b>Best-selling product:</b> {{ best_selling }}</li>
            <li><b>Highest-revenue product:</b> {{ highest_revenue }}</li>
            <li><b>Lowest-revenue product:</b> {{ lowest_revenue }}</li>
          </ul>
        </section>
      </main>

      <script>
        const labels = {{ chart_labels|safe }};
        const revenue = {{ revenue_values|safe }};
        const qLabels = {{ quantity_labels|safe }};
        const quantities = {{ quantity_values|safe }};
        const palette = ['#38bdf8','#a78bfa','#34d399','#fbbf24','#fb7185','#f97316','#2dd4bf','#818cf8','#f472b6','#a3e635'];

        Chart.defaults.color = '#f8fafc';
        new Chart(document.getElementById('revenueChart'), {
          type: 'bar',
          data: { labels, datasets: [{ label: 'Revenue (₹)', data: revenue, backgroundColor: palette }] },
          options: { responsive: true, maintainAspectRatio: false }
        });
        new Chart(document.getElementById('quantityChart'), {
          type: 'bar',
          data: { labels: qLabels, datasets: [{ label: 'Quantity', data: quantities, backgroundColor: '#34d399' }] },
          options: { responsive: true, maintainAspectRatio: false }
        });
        new Chart(document.getElementById('pieChart'), {
          type: 'pie',
          data: { labels, datasets: [{ data: revenue, backgroundColor: palette }] },
          options: { responsive: true, maintainAspectRatio: false }
        });
      </script>
    </body>
    </html>
    """,
    total_revenue=total_revenue,
    total_orders=total_orders,
    average_revenue=average_revenue,
    table=table,
    ranking_html=ranking_html,
    best_selling=best_selling,
    highest_revenue=highest_revenue,
    lowest_revenue=lowest_revenue,
    chart_labels=chart_labels,
    revenue_values=revenue_values,
    quantity_labels=quantity_labels,
    quantity_values=quantity_values
    )

if __name__ == "__main__":
    app.run(debug=True)

