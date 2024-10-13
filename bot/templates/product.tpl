This is a {{ report_type }} report aggregated by products.
{% for row in rows %}
- <b>{{ row.sku_name }}:</b> {{ row.cost|round(2) }} RUB {% endfor %}
