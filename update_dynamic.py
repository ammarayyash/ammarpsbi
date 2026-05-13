import os

template_dir = r"c:\2024-2028\Semester 4\Pengembangan Sumbeer Belajar Inovatif\projek-psbi\dashboard\templates\dashboard"

# --- Update pengaturan.html ---
pengaturan_path = os.path.join(template_dir, 'pengaturan.html')
with open(pengaturan_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add messages snippet before form
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
    content = content.replace('<form>', messages_snippet + '                    <form method="POST">\n                        {% csrf_token %}')

# Inputs
content = content.replace('<input type="text" class="form-control" value="Alexender">', '<input type="text" name="first_name" class="form-control" value="{{ request.user.first_name }}">')
content = content.replace('<input type="text" class="form-control" value="Graham">', '<input type="text" name="last_name" class="form-control" value="{{ request.user.last_name }}">')
content = content.replace('<input type="text" class="form-control" value="@alexender_g">', '<input type="text" name="username" class="form-control" value="{{ request.user.username }}">')

# Textarea bio
bio_search = '<textarea class="form-control" rows="3">UI/UX Enthusiast. Sedang belajar desain interaktif dan web development.</textarea>'
bio_replace = '<textarea name="bio" class="form-control" rows="3">{{ request.user.userprofile.bio }}</textarea>'
content = content.replace(bio_search, bio_replace)

# Buttons
content = content.replace('<button type="button" class="cta-button" style="margin-top: 16px;">Simpan Perubahan</button>', '<button type="submit" class="cta-button" style="margin-top: 16px;">Simpan Perubahan</button>')

# Toggles
t1_search = '''<h4>Tampilkan Profil Publik</h4>
                            <p>Izinkan pengguna lain melihat progress dan badge Anda.</p>
                        </div>
                        <label class="switch">
                            <input type="checkbox" checked>'''
t1_replace = '''<h4>Tampilkan Profil Publik</h4>
                            <p>Izinkan pengguna lain melihat progress dan badge Anda.</p>
                        </div>
                        <label class="switch">
                            <input type="checkbox" name="is_public" {% if request.user.userprofile.is_public %}checked{% endif %}>'''
content = content.replace(t1_search, t1_replace)

t2_search = '''<h4>Tampilkan di Leaderboard</h4>
                            <p>Sertakan nama Anda dalam peringkat global.</p>
                        </div>
                        <label class="switch">
                            <input type="checkbox" checked>'''
t2_replace = '''<h4>Tampilkan di Leaderboard</h4>
                            <p>Sertakan nama Anda dalam peringkat global.</p>
                        </div>
                        <label class="switch">
                            <input type="checkbox" name="show_in_leaderboard" {% if request.user.userprofile.show_in_leaderboard %}checked{% endif %}>'''
content = content.replace(t2_search, t2_replace)

# Dynamic Alexender Sidebar Name
content = content.replace('<h4>Alexender</h4>', '<h4>{{ request.user.first_name|default:request.user.username }}</h4>')
content = content.replace('<span class="user-level">Lvl. 12</span>', '<span class="user-level">Lvl. {{ request.user.userprofile.level|default:"1" }}</span>')

with open(pengaturan_path, 'w', encoding='utf-8') as f:
    f.write(content)

# --- Update index.html ---
index_path = os.path.join(template_dir, 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Dynamic Alexender Sidebar Name is already done previously for index, but update level
content = content.replace('<span class="user-level">Lvl. 12</span>', '<span class="user-level">Lvl. {{ request.user.userprofile.level|default:"1" }}</span>')

# Level Card
content = content.replace('<h1 class="level-title">Level 12 <span class="level-badge">– Creative Designer</span></h1>', '<h1 class="level-title">Level {{ request.user.userprofile.level|default:"1" }} <span class="level-badge">– Creative Designer</span></h1>')
content = content.replace('<p class="xp-text">Selesaikan 1 misi lagi untuk naik ke Level 13!</p>', '<p class="xp-text">Terus belajar untuk naik ke level selanjutnya!</p>')
content = content.replace('<span class="xp-current">8.450</span>', '<span class="xp-current">{{ request.user.userprofile.xp|default:"0" }}</span>')
content = content.replace('<span class="xp-total">/ 10.000 XP</span>', '<span class="xp-total">/ 1.000 XP</span>') # let's just make it 1000 for realistic testing

# Daily Streak
content = content.replace('<h2 class="streak-number">14</h2>', '<h2 class="streak-number">{{ request.user.userprofile.streak_days|default:"0" }}</h2>')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Templates for settings and index updated.")
