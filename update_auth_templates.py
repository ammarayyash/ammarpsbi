import os

template_dir = r"c:\2024-2028\Semester 4\Pengembangan Sumbeer Belajar Inovatif\projek-psbi\dashboard\templates\dashboard"

# Update index.html
index_path = os.path.join(template_dir, 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("<h4>Alexender</h4>", "<h4>{{ request.user.first_name|default:request.user.username }}</h4>")
content = content.replace('href="{% url \'login\' %}" class="logout-btn"', 'href="{% url \'logout\' %}" class="logout-btn"')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Update login.html
login_path = os.path.join(template_dir, 'login.html')
with open(login_path, 'r', encoding='utf-8') as f:
    content = f.read()

messages_snippet = """
            {% if messages %}
            <div style="margin-bottom: 20px;">
                {% for message in messages %}
                <div style="padding: 10px; border-radius: 8px; margin-bottom: 10px; color: white; background: {% if message.tags == 'error' %}rgba(255, 71, 87, 0.9){% else %}rgba(39, 174, 96, 0.9){% endif %}; text-align: left; font-size: 0.9rem;">
                    {{ message }}
                </div>
                {% endfor %}
            </div>
            {% endif %}
"""

if "{% if messages %}" not in content:
    content = content.replace('<form class="auth-form"', messages_snippet + '            <form class="auth-form"')

content = content.replace('<form class="auth-form" action="{% url \'index\' %}">', '<form class="auth-form" method="POST" action="{% url \'login\' %}">\n                {% csrf_token %}')
content = content.replace('<form class="auth-form" action="{% url \'login\' %}">', '<form class="auth-form" method="POST" action="{% url \'login\' %}">\n                {% csrf_token %}')
content = content.replace('type="email" placeholder="nama@email.com" required', 'type="email" name="email" placeholder="nama@email.com" required')
content = content.replace('type="password" placeholder="••••••••" required', 'type="password" name="password" placeholder="••••••••" required')

with open(login_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Update register.html
register_path = os.path.join(template_dir, 'register.html')
with open(register_path, 'r', encoding='utf-8') as f:
    content = f.read()

if "{% if messages %}" not in content:
    content = content.replace('<form class="auth-form"', messages_snippet + '            <form class="auth-form"')

content = content.replace('<form class="auth-form" action="{% url \'login\' %}">', '<form class="auth-form" method="POST" action="{% url \'register\' %}">\n                {% csrf_token %}')
content = content.replace('type="text" placeholder="John Doe" required', 'type="text" name="fullname" placeholder="John Doe" required')
content = content.replace('type="email" placeholder="nama@email.com" required', 'type="email" name="email" placeholder="nama@email.com" required')
content = content.replace('type="password" placeholder="Buat password yang kuat" required', 'type="password" name="password" placeholder="Buat password yang kuat" required')

with open(register_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Template logic updated.")
