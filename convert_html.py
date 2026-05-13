import os
import re

template_dir = r"c:\2024-2028\Semester 4\Pengembangan Sumbeer Belajar Inovatif\projek-psbi\dashboard\templates\dashboard"

urls = {
    'index.html': "{% url 'index' %}",
    'login.html': "{% url 'login' %}",
    'register.html': "{% url 'register' %}",
    'forgot-password.html': "{% url 'forgot_password' %}",
    'kursus.html': "{% url 'kursus' %}",
    'komunitas.html': "{% url 'komunitas' %}",
    'misi.html': "{% url 'misi' %}",
    'leaderboard.html': "{% url 'leaderboard' %}",
    'pengaturan.html': "{% url 'pengaturan' %}",
}

for filename in os.listdir(template_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(template_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add {% load static %} if not present
        if '{% load static %}' not in content:
            content = '{% load static %}\n' + content

        # Replace CSS links
        content = re.sub(r'href="style\.css"', 'href="{% static \'dashboard/style.css\' %}"', content)
        content = re.sub(r'href="auth\.css"', 'href="{% static \'dashboard/auth.css\' %}"', content)
        
        # Replace JS links
        content = re.sub(r'src="script\.js"', 'src="{% static \'dashboard/script.js\' %}"', content)

        # Replace URL hrefs
        for old_url, new_url in urls.items():
            content = content.replace(f'href="{old_url}"', f'href="{new_url}"')
            content = content.replace(f'action="{old_url}"', f'action="{new_url}"') # for forms

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("Conversion complete.")
