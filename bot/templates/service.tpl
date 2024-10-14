This is a {{ report_type }} report aggregated by service.
{% for row in rows %}
- <b>{{ row.service_name }}:</b> {{ row.cost|round(2) }} RUB {% endfor %}

<b>Total:</b> {{ total|round(2) }} RUB
