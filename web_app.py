
from flask import Flask, render_template_string
import pandas as pd
import json

app = Flask(__name__)


def get_data():
    df = pd.read_csv("sales_data.csv")
    df["Revenue"] = df["Quantity"] * df["Price"]

    revenue = df.groupby("Product")["Revenue"].sum().sort_values(
        ascending=False
    )
    quantity = df.groupby("Product")["Quantity"].sum().sort_values(
        ascending=False
    )

    return df, revenue, quantity


@app.route("/")
def dashboard():
    df, revenue, quantity = get_data()

    total_revenue = float(df["Revenue"].sum())
    total_orders = len(df)
    average_revenue = total_revenue / total_orders if total_orders else 0

    table = df.to_html(
        index=False,
        classes="data-table",
        border=0,
        float_format=lambda x: f"{x:,.2f}"
    )

    ranking = revenue.rename("Total Revenue").reset_index()
    ranking.insert(0, "Rank", range(1, len(ranking) + 1))

    ranking_html = ranking.to_html(
        index=False,
        classes="data-table",
        border=0,
        float_format=lambda x: f"{x:,.2f}"
    )

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
        * {
          box-sizing: border-box;
        }

        body {
          margin: 0;
          font-family: Arial, Helvetica, sans-serif;
          background: #0b1f3a;
          color: #f8fafc;
          line-height: 1.6;
        }

        header {
          padding: 28px 5%;
          background: #10294b;
        }

        h1 {
          margin: 0 0 8px;
          color: #38bdf8;
          font-size: clamp(24px, 3vw, 34px);
        }

        .container {
          max-width: 1400px;
          margin: auto;
          padding: 25px;
        }

        .cards {
          display: grid;
          grid-template-columns: repeat(
            auto-fit, minmax(200px, 1fr)
          );
          gap: 18px;
        }

        .card, .panel {
          background: #142e50;
          padding: 22px;
          border-radius: 14px;
          margin-bottom: 22px;
          box-shadow: 0 5px 18px rgba(0, 0, 0, 0.15);
        }

        .metric {
          font-size: clamp(24px, 3vw, 32px);
          font-weight: bold;
          color: #34d399;
          margin-top: 12px;
          overflow-wrap: anywhere;
        }

        h2 {
          color: #38bdf8;
          font-size: 21px;
          margin-top: 0;
        }

        .charts {
          display: grid;
          grid-template-columns: repeat(
            auto-fit, minmax(min(100%, 400px), 1fr)
          );
          gap: 20px;
          align-items: stretch;
        }

        .chart-wrap {
          position: relative;
          width: 100%;
          height: 380px;
        }

        .table-wrap {
          overflow-x: auto;
          max-height: 420px;
        }

        table {
          border-collapse: collapse;
          width: 100%;
          background: #10294b;
          font-size: 14px;
        }

        th, td {
          text-align: left;
          padding: 12px;
          border-bottom: 1px solid #294665;
          white-space: nowrap;
        }

        th {
          color: #38bdf8;
          position: sticky;
          top: 0;
          background: #10294b;
        }

        tr:hover td {
          background: #1a3a60;
        }

        li {
          margin: 12px 0;
        }

        @media (max-width: 600px) {
          .container {
            padding: 14px;
          }

          header {
            padding: 22px 14px;
          }

          .card, .panel {
            padding: 16px;
          }

          .chart-wrap {
            height: 320px;
          }
        }
      </style>
    </head>

    <body>
      <header>
        <h1>📊 Sales Data Analytics Dashboard</h1>
        <p>Analyze sales performance and discover business insights.</p>
      </header>

      <main class="container">

        <section class="cards">
          <div class="card">
            <div>Total Revenue</div>
            <div class="metric">
              ₹{{ "%.2f"|format(total_revenue) }}
            </div>
          </div>

          <div class="card">
            <div>Total Orders</div>
            <div class="metric">{{ total_orders }}</div>
          </div>

          <div class="card">
            <div>Average Revenue per Order</div>
            <div class="metric">
              ₹{{ "%.2f"|format(average_revenue) }}
            </div>
          </div>
        </section>

        <section class="panel">
          <h2>Sales Data</h2>
          <div class="table-wrap">{{ table|safe }}</div>
        </section>

        <section class="charts">

          <div class="panel">
            <h2>Revenue by Product</h2>
            <div class="chart-wrap">
              <canvas id="revenueChart"></canvas>
            </div>
          </div>

          <div class="panel">
            <h2>Quantity Sold by Product</h2>
            <div class="chart-wrap">
              <canvas id="quantityChart"></canvas>
            </div>
          </div>

          <div class="panel">
            <h2>Revenue Contribution by Product</h2>
            <div class="chart-wrap">
              <canvas id="pieChart"></canvas>
            </div>
          </div>

        </section>

        <section class="panel">
          <h2>Product Revenue Ranking</h2>
          <div class="table-wrap">{{ ranking_html|safe }}</div>
        </section>

        <section class="panel">
          <h2>💡 Business Insights</h2>
          <ul>
            <li>
              <b>Best-selling product:</b> {{ best_selling }}
            </li>
            <li>
              <b>Highest-revenue product:</b> {{ highest_revenue }}
            </li>
            <li>
              <b>Lowest-revenue product:</b> {{ lowest_revenue }}
            </li>
          </ul>
        </section>

      </main>

      <script>
        const labels = {{ chart_labels|safe }};
        const revenue = {{ revenue_values|safe }};
        const qLabels = {{ quantity_labels|safe }};
        const quantities = {{ quantity_values|safe }};

        const palette = [
          '#38bdf8',
          '#a78bfa',
          '#34d399',
          '#fbbf24',
          '#fb7185',
          '#f97316',
          '#2dd4bf',
          '#818cf8',
          '#f472b6',
          '#a3e635'
        ];

        Chart.defaults.color = '#f8fafc';
        Chart.defaults.font.family = 'Arial, Helvetica, sans-serif';
        Chart.defaults.font.size = 14;
        Chart.defaults.devicePixelRatio = 2;

        const commonOptions = {
          responsive: true,
          maintainAspectRatio: false,
          devicePixelRatio: 2,
          animation: false,

          plugins: {
            legend: {
              display: true,
              labels: {
                color: '#f8fafc',
                font: {
                  size: 13
                },
                padding: 16
              }
            },
            tooltip: {
              titleFont: {
                size: 14
              },
              bodyFont: {
                size: 13
              }
            }
          },

          scales: {
            x: {
              ticks: {
                color: '#f8fafc',
                font: {
                  size: 12
                },
                maxRotation: 35,
                minRotation: 0
              },
              grid: {
                color: 'rgba(255,255,255,0.08)'
              }
            },

            y: {
              beginAtZero: true,
              ticks: {
                color: '#f8fafc',
                font: {
                  size: 12
                },
                precision: 0
              },
              grid: {
                color: 'rgba(255,255,255,0.12)'
              }
            }
          }
        };

        // Revenue by Product
        new Chart(document.getElementById('revenueChart'), {
          type: 'bar',

          data: {
            labels: labels,
            datasets: [{
              label: 'Revenue (₹)',
              data: revenue,
              backgroundColor: palette,
              borderRadius: 5
            }]
          },

          options: commonOptions
        });

        // Quantity Sold by Product
        new Chart(document.getElementById('quantityChart'), {
          type: 'bar',

          data: {
            labels: qLabels,
            datasets: [{
              label: 'Quantity Sold',
              data: quantities,
              backgroundColor: '#34d399',
              borderRadius: 5
            }]
          },

          options: commonOptions
        });

        // Revenue Contribution Pie Chart
        new Chart(document.getElementById('pieChart'), {
          type: 'pie',

          data: {
            labels: labels,
            datasets: [{
              data: revenue,
              backgroundColor: palette,
              borderColor: '#142e50',
              borderWidth: 2
            }]
          },

          options: {
            responsive: true,
            maintainAspectRatio: false,
            devicePixelRatio: 2,
            animation: false,

            plugins: {
              legend: {
                position: 'bottom',
                labels: {
                  color: '#f8fafc',
                  font: {
                    size: 13
                  },
                  padding: 14
                }
              },

              tooltip: {
                callbacks: {
                  label: function(context) {
                    const value = context.raw;
                    const total = context.dataset.data.reduce(
                      (sum, item) => sum + item, 0
                    );
                    const percent = total
                      ? ((value / total) * 100).toFixed(1)
                      : '0.0';

                    return context.label + ': ₹' +
                      value.toLocaleString('en-IN') +
                      ' (' + percent + '%)';
                  }
                }
              }
            }
          }
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
