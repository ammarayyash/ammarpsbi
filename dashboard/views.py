from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count, Avg, Q
from django.utils import timezone
from django.http import JsonResponse, FileResponse, Http404
from django.urls import reverse
from functools import wraps
from datetime import date
import os
from .models import (
    UserProfile,
    Mission,
    Question,
    Choice,
    UserMissionProgress,
    UserAnswer,
    Course,
    CommunityRoom,
    CommunityRoomMembership,
    CommunityMaterial,
    CommunityQuizQuestion,
    CommunityQuizSubmission,
    UniqueStreak,
)

# =========================================
# Staff/Admin Required Decorator
# =========================================
def staff_required(view_func):
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Anda tidak memiliki akses ke halaman admin.')
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper


def teacher_or_staff_required(view_func):
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        # Allow full staff/admin or teacher accounts (limited privileges)
        try:
            is_teacher = getattr(request.user.userprofile, 'is_teacher', False)
        except Exception:
            is_teacher = False
        if not (request.user.is_staff or is_teacher):
            messages.error(request, 'Anda tidak memiliki akses ke halaman ini.')
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper


# =========================================
# EXISTING VIEWS (unchanged)
# =========================================
@login_required(login_url='login')
def index(request):
    profile = request.user.userprofile

    # Mission stats
    all_missions = Mission.objects.all().order_by('order')
    progress_qs = UserMissionProgress.objects.filter(user=request.user)
    progress_dict = {p.mission_id: p.status for p in progress_qs}
    completed_count = progress_qs.filter(status='completed').count()
    total_missions = all_missions.count()
    path_pct = int((completed_count / total_missions * 100)) if total_missions else 0

    # XP progress to next level (500 XP per level)
    xp_in_level = profile.xp % 500
    xp_pct = int(xp_in_level / 500 * 100)

    # Level title based on level
    level_titles = {1: 'Pemula', 2: 'Explorer', 3: 'Apprentice', 4: 'Designer', 5: 'Artisan'}
    level_title = level_titles.get(profile.level, 'Master')

    # Learning path list
    mission_list = []
    prev_completed = True
    for m in all_missions:
        status = progress_dict.get(m.id, 'not_started')
        is_active = (status in ('reading', 'quiz', 'evaluation')) or (status == 'not_started' and prev_completed)
        mission_list.append({
            'mission': m,
            'status': status,
            'is_active': is_active,
            'is_completed': status == 'completed',
            'is_locked': status == 'not_started' and not prev_completed,
        })
        prev_completed = (status == 'completed')

    # Badges — earned based on achievements
    badge_defs = [
        {'icon': 'fa-rocket', 'name': 'Starter', 'condition': completed_count >= 1},
        {'icon': 'fa-palette', 'name': 'Creative', 'condition': completed_count >= 2},
        {'icon': 'fa-code', 'name': 'Coder', 'condition': profile.xp >= 100},
        {'icon': 'fa-lightbulb', 'name': 'Bright', 'condition': profile.xp >= 200},
        {'icon': 'fa-gem', 'name': 'Gem', 'condition': completed_count >= 3},
        {'icon': 'fa-bolt', 'name': 'Speedy', 'condition': profile.xp >= 300},
        {'icon': 'fa-crown', 'name': 'Crown', 'condition': completed_count >= 4},
        {'icon': 'fa-star', 'name': 'Star', 'condition': completed_count >= 5},
    ]
    earned_badges = sum(1 for b in badge_defs if b['condition'])

    # Top leaderboard preview
    user_rank = None
    for idx, p in enumerate(UserProfile.objects.select_related('user').order_by('-xp'), start=1):
        if p.user == request.user:
            user_rank = idx
            break
    top3 = list(UserProfile.objects.select_related('user').order_by('-xp')[:3])

    context = {
        'profile': profile,
        'xp_in_level': xp_in_level,
        'xp_pct': xp_pct,
        'xp_next': 500,
        'level_title': level_title,
        'completed_count': completed_count,
        'total_missions': total_missions,
        'path_pct': path_pct,
        'mission_list': mission_list,
        'badge_defs': badge_defs,
        'earned_badges': earned_badges,
        'top3': top3,
        'user_rank': user_rank,
    }
    return render(request, 'dashboard/index.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Django authenticates via username. We map email to username.
        # Find user by email
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = None
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Email atau Password salah!')
            
    return render(request, 'dashboard/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validation
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar!')
            return redirect('register')
            
        # Create user (username will be the email to ensure uniqueness)
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = fullname
        user.save()
        
        messages.success(request, 'Akun berhasil dibuat! Silakan masuk.')
        return redirect('login')
        
    return render(request, 'dashboard/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def kursus(request):
    courses = Course.objects.filter(is_active=True).order_by('order')
    return render(request, 'dashboard/kursus.html', {
        'profile': request.user.userprofile,
        'courses': courses
    })


def _safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@login_required(login_url='login')
def komunitas(request):
    if request.method == 'POST':
        token = (request.POST.get('token') or '').strip()
        if not token:
            messages.error(request, 'Masukkan token ruang kelas terlebih dahulu.')
            return redirect('komunitas')

        room = CommunityRoom.objects.filter(token__iexact=token).first()
        if not room:
            messages.error(request, 'Token kelas tidak valid.')
            return redirect('komunitas')

        CommunityRoomMembership.objects.get_or_create(room=room, user=request.user)
        messages.success(request, f'Berhasil masuk ke ruang kelas "{room.name}".')
        return redirect('komunitas_detail', pk=room.id)

    my_room_ids = list(
        CommunityRoomMembership.objects.filter(user=request.user).values_list('room_id', flat=True)
    )

    if request.user.is_staff:
        rooms = CommunityRoom.objects.all().annotate(
            member_count=Count('memberships', distinct=True),
            material_count=Count('materials', distinct=True),
            quiz_count=Count('quiz_questions', distinct=True),
        )
    else:
        rooms = CommunityRoom.objects.filter(id__in=my_room_ids).annotate(
            member_count=Count('memberships', distinct=True),
            material_count=Count('materials', distinct=True),
            quiz_count=Count('quiz_questions', distinct=True),
        )
    context = {
        'profile': request.user.userprofile,
        'rooms': rooms,
        'joined_count': len(my_room_ids),
    }
    return render(request, 'dashboard/komunitas.html', context)

@login_required(login_url='login')
def komunitas_detail(request, pk):
    room = get_object_or_404(CommunityRoom, pk=pk)
    is_allowed = request.user.is_staff or CommunityRoomMembership.objects.filter(
        room=room,
        user=request.user,
    ).exists()
    if not is_allowed:
        messages.error(request, 'Anda belum bergabung ke ruang kelas ini. Masukkan token terlebih dahulu.')
        return redirect('komunitas')

    materials = room.materials.all() if room.has_material_section else []
    questions = room.quiz_questions.all() if room.has_quiz_section else []
    latest_submission = CommunityQuizSubmission.objects.filter(room=room, user=request.user).first()
    quiz_result = None

    if request.method == 'POST' and room.has_quiz_section:
        if not questions:
            messages.error(request, 'Kuis belum tersedia untuk ruang kelas ini.')
            return redirect('komunitas_detail', pk=room.id)

        correct_count = 0
        answer_map = {}
        for question in questions:
            answer_key = f'question_{question.id}'
            selected = (request.POST.get(answer_key) or '').upper()
            answer_map[question.id] = selected
            if selected == question.correct_option:
                correct_count += 1

        total_questions = len(questions)
        percentage = int((correct_count / total_questions) * 100) if total_questions else 0
        # Only persist submissions if room is configured to store scores
        latest_submission = None
        if getattr(room, 'store_scores', False):
            latest_submission = CommunityQuizSubmission.objects.create(
                room=room,
                user=request.user,
                score=correct_count,
                total_questions=total_questions,
            )
        quiz_result = {
            'score': correct_count,
            'total': total_questions,
            'percentage': percentage,
            'answers': answer_map,
        }

        if percentage >= 75:
            messages.success(request, f'Nilai kuis Anda {correct_count}/{total_questions} ({percentage}%).')
        else:
            messages.info(request, f'Nilai kuis Anda {correct_count}/{total_questions} ({percentage}%). Silakan coba lagi.')
    context = {
        'profile': request.user.userprofile,
        'room': room,
        'materials': materials,
        'questions': questions,
        'quiz_result': quiz_result,
        'latest_submission': latest_submission,
    }
    return render(request, 'dashboard/komunitas_detail.html', context)

@teacher_or_staff_required
def admin_community_rooms(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action in ('create_room', 'update_room'):
            name = (request.POST.get('name') or '').strip()
            token = (request.POST.get('token') or '').strip().upper()
            description = (request.POST.get('description') or '').strip()
            content = (request.POST.get('content') or '').strip()
            content_mode = request.POST.get('content_mode') or 'both'

            if content_mode not in {'material', 'quiz', 'both'}:
                content_mode = 'both'

            if not name or not token:
                messages.error(request, 'Nama kelas dan token wajib diisi.')
                return redirect('admin_community_rooms')

            if action == 'create_room':
                try:
                    store_scores_flag = request.POST.get('store_scores') == 'on'
                    CommunityRoom.objects.create(
                        name=name,
                        token=token,
                        description=description,
                        content=content or 'Selamat datang di ruang kelas ini.',
                        content_mode=content_mode,
                        store_scores=store_scores_flag,
                    )
                    messages.success(request, 'Ruang kelas berhasil dibuat.')
                except IntegrityError:
                    messages.error(request, 'Token sudah dipakai. Gunakan token lain.')
            else:
                room = get_object_or_404(CommunityRoom, id=request.POST.get('room_id'))
                room.name = name
                room.token = token
                room.description = description
                room.content = content or 'Selamat datang di ruang kelas ini.'
                room.content_mode = content_mode
                # Update store_scores if provided
                if 'store_scores' in request.POST:
                    room.store_scores = request.POST.get('store_scores') == 'on'
                try:
                    room.save()
                    messages.success(request, 'Ruang kelas berhasil diperbarui.')
                except IntegrityError:
                    messages.error(request, 'Token sudah dipakai. Gunakan token lain.')

        elif action == 'delete_room':
            room = get_object_or_404(CommunityRoom, id=request.POST.get('room_id'))
            room.delete()
            messages.success(request, 'Ruang kelas berhasil dihapus.')
        return redirect('admin_community_rooms')

    rooms = CommunityRoom.objects.all().annotate(
        member_count=Count('memberships', distinct=True),
        material_count=Count('materials', distinct=True),
        quiz_count=Count('quiz_questions', distinct=True),
    )
    context = {
        'active_page': 'community',
        'rooms': rooms,
    }
    return render(request, 'dashboard/admin/community_rooms.html', context)


@teacher_or_staff_required
def admin_community_room_manage(request, room_id):
    room = get_object_or_404(CommunityRoom, id=room_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create_material':
            title = (request.POST.get('title') or '').strip()
            if not title:
                messages.error(request, 'Judul materi wajib diisi.')
                return redirect('admin_community_room_manage', room_id=room.id)

            CommunityMaterial.objects.create(
                room=room,
                title=title,
                body=(request.POST.get('body') or '').strip(),
                media_url=(request.POST.get('media_url') or '').strip() or None,
                media_file=request.FILES.get('media_file'),
                order=_safe_int(request.POST.get('order'), 0),
            )
            messages.success(request, 'Materi berhasil ditambahkan.')

        elif action == 'update_material':
            material = get_object_or_404(CommunityMaterial, id=request.POST.get('material_id'), room=room)
            title = (request.POST.get('title') or '').strip()
            if not title:
                messages.error(request, 'Judul materi wajib diisi.')
                return redirect('admin_community_room_manage', room_id=room.id)

            material.title = title
            material.body = (request.POST.get('body') or '').strip()
            material.media_url = (request.POST.get('media_url') or '').strip() or None
            material.order = _safe_int(request.POST.get('order'), material.order)
            if request.FILES.get('media_file'):
                material.media_file = request.FILES['media_file']
            material.save()
            messages.success(request, 'Materi berhasil diperbarui.')

        elif action == 'delete_material':
            material = get_object_or_404(CommunityMaterial, id=request.POST.get('material_id'), room=room)
            material.delete()
            messages.success(request, 'Materi berhasil dihapus.')

        elif action == 'create_question':
            question_text = (request.POST.get('question_text') or '').strip()
            option_a = (request.POST.get('option_a') or '').strip()
            option_b = (request.POST.get('option_b') or '').strip()
            option_c = (request.POST.get('option_c') or '').strip()
            option_d = (request.POST.get('option_d') or '').strip()
            correct_option = (request.POST.get('correct_option') or 'A').upper()
            if correct_option not in {'A', 'B', 'C', 'D'}:
                correct_option = 'A'

            if not question_text or not option_a or not option_b or not option_c or not option_d:
                messages.error(request, 'Semua field soal dan opsi jawaban wajib diisi.')
                return redirect('admin_community_room_manage', room_id=room.id)

            CommunityQuizQuestion.objects.create(
                room=room,
                question_text=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_option=correct_option,
                explanation=(request.POST.get('explanation') or '').strip(),
                order=_safe_int(request.POST.get('order'), 0),
            )
            messages.success(request, 'Soal kuis berhasil ditambahkan.')

        elif action == 'update_question':
            question = get_object_or_404(CommunityQuizQuestion, id=request.POST.get('question_id'), room=room)
            question_text = (request.POST.get('question_text') or '').strip()
            option_a = (request.POST.get('option_a') or '').strip()
            option_b = (request.POST.get('option_b') or '').strip()
            option_c = (request.POST.get('option_c') or '').strip()
            option_d = (request.POST.get('option_d') or '').strip()
            correct_option = (request.POST.get('correct_option') or 'A').upper()
            if correct_option not in {'A', 'B', 'C', 'D'}:
                correct_option = 'A'

            if not question_text or not option_a or not option_b or not option_c or not option_d:
                messages.error(request, 'Semua field soal dan opsi jawaban wajib diisi.')
                return redirect('admin_community_room_manage', room_id=room.id)

            question.question_text = question_text
            question.option_a = option_a
            question.option_b = option_b
            question.option_c = option_c
            question.option_d = option_d
            question.correct_option = correct_option
            question.explanation = (request.POST.get('explanation') or '').strip()
            question.order = _safe_int(request.POST.get('order'), question.order)
            question.save()
            messages.success(request, 'Soal kuis berhasil diperbarui.')

        elif action == 'delete_question':
            question = get_object_or_404(CommunityQuizQuestion, id=request.POST.get('question_id'), room=room)
            question.delete()
            messages.success(request, 'Soal kuis berhasil dihapus.')

        return redirect('admin_community_room_manage', room_id=room.id)

    materials = room.materials.all()
    questions = room.quiz_questions.all()
    recent_submissions = room.quiz_submissions.select_related('user')[:10]

    context = {
        'active_page': 'community',
        'room': room,
        'materials': materials,
        'questions': questions,
        'next_material_order': (materials.last().order + 1) if materials else 1,
        'next_question_order': (questions.last().order + 1) if questions else 1,
        'recent_submissions': recent_submissions,
    }
    return render(request, 'dashboard/admin/community_room_manage.html', context)

@login_required(login_url='login')
def misi(request):
    course_id = request.GET.get('course_id')
    
    if course_id:
        course = get_object_or_404(Course, pk=course_id)
        missions = Mission.objects.filter(course=course).order_by('order')
        page_title = f"Misi: {course.title}"
    else:
        missions = Mission.objects.all().order_by('order')
        page_title = "Semua Misi"
        
    progress_dict = {}
    for p in UserMissionProgress.objects.filter(user=request.user, mission__in=missions):
        progress_dict[p.mission_id] = p.status
    
    mission_list = []
    active_count = 0
    completed_count = 0
    locked_count = 0
    prev_completed = True
    for mission in missions:
        status = progress_dict.get(mission.id, 'not_started')
        is_locked = (status == 'not_started' and not prev_completed)
        mission_list.append({
            'mission': mission,
            'status': status,
            'is_locked': is_locked,
        })
        if status == 'completed':
            completed_count += 1
        elif is_locked:
            locked_count += 1
        else:
            active_count += 1
        prev_completed = (status == 'completed')
    
    context = {
        'mission_list': mission_list,
        'profile': request.user.userprofile,
        'active_count': active_count,
        'completed_count': completed_count,
        'locked_count': locked_count,
        'page_title': page_title,
    }
    return render(request, 'dashboard/misi.html', context)

@login_required(login_url='login')
def leaderboard(request):
    ranked = list(UserProfile.objects.select_related('user').order_by('-xp'))
    podium = ranked[:3]  # top 3
    rest = ranked[3:]    # rank 4+

    # Find current user rank
    user_rank = None
    for idx, p in enumerate(ranked, start=1):
        if p.user == request.user:
            user_rank = idx
            break

    context = {
        'podium': podium,
        'rest': rest,
        'user_rank': user_rank,
        'user_profile': request.user.userprofile,
    }
    return render(request, 'dashboard/leaderboard.html', context)

@login_required(login_url='login')
def pengaturan(request):
    if request.method == 'POST':
        user = request.user
        profile = user.userprofile
        action = request.POST.get('action', 'profile')

        if action == 'password':
            old_password = request.POST.get('old_password', '')
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')
            if not user.check_password(old_password):
                messages.error(request, 'Password lama tidak sesuai!')
            elif new_password != confirm_password:
                messages.error(request, 'Konfirmasi password baru tidak cocok!')
            elif len(new_password) < 6:
                messages.error(request, 'Password baru minimal 6 karakter!')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # keep logged in
                messages.success(request, 'Password berhasil diubah!')
            return redirect('pengaturan')

        # --- Profile update ---
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        bio = request.POST.get('bio', '')
        is_public = request.POST.get('is_public') == 'on'
        show_in_leaderboard = request.POST.get('show_in_leaderboard') == 'on'

        user.first_name = first_name
        user.last_name = last_name
        if username and not User.objects.filter(username=username).exclude(pk=user.pk).exists():
            user.username = username
        user.save()

        profile.bio = bio
        profile.is_public = is_public
        profile.show_in_leaderboard = show_in_leaderboard
        profile.save()

        messages.success(request, 'Pengaturan berhasil disimpan!')
        return redirect('pengaturan')

    return render(request, 'dashboard/pengaturan.html')


@login_required(login_url='login')
def upload_avatar(request):
    """Handle profile picture upload via AJAX or form POST."""
    if request.method == 'POST' and request.FILES.get('avatar'):
        file = request.FILES['avatar']
        profile = request.user.userprofile

        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if file.content_type not in allowed_types:
            messages.error(request, 'Format file tidak didukung. Gunakan JPG, PNG, GIF, atau WebP.')
            return redirect('pengaturan')

        # Validate file size (max 5MB)
        if file.size > 5 * 1024 * 1024:
            messages.error(request, 'Ukuran file terlalu besar. Maksimal 5MB.')
            return redirect('pengaturan')

        # Delete old avatar if exists
        if profile.avatar:
            old_path = profile.avatar.path
            if os.path.exists(old_path):
                os.remove(old_path)

        profile.avatar = file
        profile.save()
        messages.success(request, 'Foto profil berhasil diperbarui!')
    else:
        messages.error(request, 'Tidak ada file yang dipilih.')

    return redirect('pengaturan')

@login_required(login_url='login')
def forgot_password(request):
    return render(request, 'dashboard/forgot-password.html')

@login_required(login_url='login')
def materi_view(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    progress, created = UserMissionProgress.objects.get_or_create(user=request.user, mission=mission)
    
    if progress.status == 'not_started':
        progress.status = 'reading'
        progress.save()
    
    # Check for automatic module file
    module_info = None
    import os
    from django.conf import settings
    media_modul_dir = os.path.join(settings.MEDIA_ROOT, 'modul')
    if os.path.exists(media_modul_dir):
        for filename in os.listdir(media_modul_dir):
            # Check for various naming patterns
            if (filename.lower().startswith(f'modul{mission.order}') or 
                filename.lower().startswith(f'level{mission.order}') or
                f'{mission.order}' in filename.lower()):
                file_path = os.path.join('modul', filename)
                file_url = f"{settings.MEDIA_URL}{file_path}"
                
                # Determine file type and embed method
                if filename.lower().endswith('.pdf'):
                    embed_type = 'pdf'
                    # serve via Django view to ensure correct headers (inline)
                    try:
                        embed_url = reverse('serve_modul_pdf', args=[filename])
                    except Exception:
                        embed_url = file_url
                elif filename.lower().endswith(('.doc', '.docx')):
                    embed_type = 'doc'
                    # Use Google Docs viewer for DOC files
                    embed_url = f"https://docs.google.com/viewer?url={request.build_absolute_uri(file_url)}&embedded=true"
                elif filename.lower().endswith(('.txt', '.md')):
                    embed_type = 'text'
                    embed_url = file_url
                else:
                    embed_type = 'download'
                    embed_url = file_url
                
                module_info = {
                    'filename': filename,
                    'file_url': file_url,
                    'embed_type': embed_type,
                    'embed_url': embed_url,
                }
                break
    
    context = {
        'mission': mission,
        'progress': progress,
        'module_info': module_info,
    }
    return render(request, 'dashboard/materi.html', context)


def serve_modul_pdf(request, filename):
    """Serve a PDF from media/modul with inline Content-Disposition and proper Content-Type."""
    import os
    from django.conf import settings

    # Prevent path traversal by normalizing and ensuring filename has no directory
    if os.path.basename(filename) != filename:
        raise Http404("Invalid filename")

    path = os.path.join(settings.MEDIA_ROOT, 'modul', filename)
    if not os.path.exists(path):
        raise Http404("File not found")

    # Use FileResponse to stream and set headers for inline viewing
    f = open(path, 'rb')
    response = FileResponse(f, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    # Allow embedding in same-origin frames
    response['X-Frame-Options'] = 'SAMEORIGIN'
    return response

@login_required(login_url='login')
def kuis_view(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    progress, created = UserMissionProgress.objects.get_or_create(user=request.user, mission=mission)
    
    if progress.status == 'reading':
        progress.status = 'quiz'
        progress.save()
        
    # Redirect ke gamifikasi berdasarkan gamification_mode
    if mission.gamification_mode:
        mode_view_map = {
            'level1': 'gamifikasi_level1',
            'level2': 'gamifikasi_level2',
            'level3': 'gamifikasi_level3',
            'level4': 'gamifikasi_level4',
            'level5': 'gamifikasi_level5',
        }
        if mission.gamification_mode in mode_view_map:
            return redirect(mode_view_map[mission.gamification_mode])
    else:
        # Fallback ke sistem lama (berdasarkan urutan misi)
        gamifikasi_map_fallback = {
            1: 'gamifikasi_level1',
            2: 'gamifikasi_level2',
            3: 'gamifikasi_level3',
            4: 'gamifikasi_level4',
            5: 'gamifikasi_level5',
        }
        if mission.order in gamifikasi_map_fallback:
            return redirect(gamifikasi_map_fallback[mission.order])
        
    questions = mission.questions.all().order_by('order')
    
    if request.method == 'POST':
        # Mark activity date (used to keep streak alive for today)
        profile = request.user.userprofile
        prev_last = profile.last_streak_date
        today = timezone.localdate()
        if prev_last != today:
            profile.last_streak_date = today
            profile.save()

        all_correct = True
        for q in questions:
            choice_id = request.POST.get(f'question_{q.id}')
            if choice_id:
                choice = Choice.objects.get(id=choice_id)
                # Save answer
                UserAnswer.objects.update_or_create(
                    user=request.user,
                    question=q,
                    defaults={'choice': choice, 'is_correct': choice.is_correct}
                )
                if not choice.is_correct:
                    all_correct = False
            else:
                all_correct = False

        if all_correct:
            progress.status = 'completed'
            progress.completed_at = timezone.now()
            progress.save()
            # Add XP and level up
            profile = request.user.userprofile
            # Update streak based on previous last date
            if prev_last == today:
                pass
            else:
                if prev_last and (today - prev_last).days == 1:
                    profile.streak_days += 1
                else:
                    profile.streak_days = 1
            profile.last_streak_date = today
            profile.xp += mission.xp_reward
            profile.level = max(1, profile.xp // 500 + 1)
            profile.save()

            # If streak is a "nice number", record it as UniqueStreak
            NICE = {5, 10, 25, 50, 100, 365}
            if profile.streak_days in NICE:
                UniqueStreak.objects.get_or_create(user=request.user, streak_value=profile.streak_days)
            return redirect('misi_selesai', mission_id=mission.id)
        else:
            progress.status = 'evaluation'
            progress.save()
            return redirect('misi_evaluasi', mission_id=mission.id)
            
    return render(request, 'dashboard/kuis.html', {'mission': mission, 'questions': questions})

@login_required(login_url='login')
def evaluasi_view(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    progress = UserMissionProgress.objects.get(user=request.user, mission=mission)
    
    # Get questions that were answered incorrectly
    wrong_answers = UserAnswer.objects.filter(user=request.user, question__mission=mission, is_correct=False)
    questions = [wa.question for wa in wrong_answers]
    
    if request.method == 'POST':
        # Mark activity date for today
        profile = request.user.userprofile
        prev_last = profile.last_streak_date
        today = timezone.localdate()
        if prev_last != today:
            profile.last_streak_date = today
            profile.save()

        all_correct = True
        for q in questions:
            choice_id = request.POST.get(f'question_{q.id}')
            if choice_id:
                choice = Choice.objects.get(id=choice_id)
                UserAnswer.objects.update_or_create(
                    user=request.user,
                    question=q,
                    defaults={'choice': choice, 'is_correct': choice.is_correct}
                )
                if not choice.is_correct:
                    all_correct = False
            else:
                all_correct = False

        if all_correct:
            progress.status = 'completed'
            progress.completed_at = timezone.now()
            progress.save()
            # Add XP and level up, update streak based on previous date
            profile = request.user.userprofile
            if prev_last == today:
                pass
            else:
                if prev_last and (today - prev_last).days == 1:
                    profile.streak_days += 1
                else:
                    profile.streak_days = 1
            profile.last_streak_date = today
            profile.xp += mission.xp_reward
            profile.level = max(1, profile.xp // 500 + 1)
            profile.save()
            return redirect('misi_selesai', mission_id=mission.id)
        else:
            messages.error(request, 'Masih ada jawaban yang salah. Coba lagi!')
            return redirect('misi_evaluasi', mission_id=mission.id)
            
    return render(request, 'dashboard/evaluasi.html', {'mission': mission, 'questions': questions})

@login_required(login_url='login')
def selesai_view(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    next_mission = Mission.objects.filter(order=mission.order + 1).first()
    next_mission_url = reverse('misi_materi', args=[next_mission.id]) if next_mission else None
    return render(request, 'dashboard/selesai.html', {
        'mission': mission,
        'next_mission': next_mission,
        'next_mission_url': next_mission_url,
    })


# =========================================
# ADMIN VIEWS
# =========================================

@staff_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_missions = Mission.objects.count()
    total_completed = UserMissionProgress.objects.filter(status='completed').count()
    avg_xp = UserProfile.objects.aggregate(avg=Avg('xp'))['avg'] or 0
    
    # Mission completion stats for bar chart
    missions = Mission.objects.all().order_by('order')
    mission_stats = []
    max_completed = 1  # avoid division by zero
    for m in missions:
        count = UserMissionProgress.objects.filter(mission=m, status='completed').count()
        if count > max_completed:
            max_completed = count
        mission_stats.append({
            'title': m.title,
            'count': count,
        })
    
    # Calculate percentage relative to max
    for ms in mission_stats:
        ms['percentage'] = int((ms['count'] / max_completed) * 100) if max_completed > 0 else 0
    
    # Recent users (last 5)
    recent_users = User.objects.select_related('userprofile').order_by('-date_joined')[:5]
    
    # Recent completions
    recent_completions = UserMissionProgress.objects.filter(
        status='completed'
    ).select_related('user', 'mission').order_by('-completed_at')[:5]
    
    context = {
        'active_page': 'dashboard',
        'total_users': total_users,
        'total_missions': total_missions,
        'total_courses': Course.objects.count(),
        'total_completed': total_completed,
        'avg_xp': int(avg_xp),
        'mission_stats': mission_stats,
        'recent_users': recent_users,
        'recent_completions': recent_completions,
    }
    return render(request, 'dashboard/admin/dashboard.html', context)


@staff_required
def admin_users(request):
    users = User.objects.select_related('userprofile').all().order_by('-date_joined')
    
    # Annotate with completed missions count
    for u in users:
        u.completed_missions = UserMissionProgress.objects.filter(
            user=u, status='completed'
        ).count()
    
    context = {
        'active_page': 'users',
        'users': users,
    }
    return render(request, 'dashboard/admin/users.html', context)


@staff_required
def admin_user_edit(request, user_id):
    edit_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Update user info
        edit_user.first_name = request.POST.get('first_name', '')
        edit_user.last_name = request.POST.get('last_name', '')
        edit_user.email = request.POST.get('email', edit_user.email)
        
        username = request.POST.get('username', '')
        if username and not User.objects.filter(username=username).exclude(pk=edit_user.pk).exists():
            edit_user.username = username
        
        # Update role
        role = request.POST.get('role', 'user')
        if role == 'superuser':
            edit_user.is_staff = True
            edit_user.is_superuser = True
        elif role == 'staff':
            edit_user.is_staff = True
            edit_user.is_superuser = False
        elif role == 'guru':
            # Teacher account: not staff, but flagged on profile
            edit_user.is_staff = False
            edit_user.is_superuser = False
        else:
            edit_user.is_staff = False
            edit_user.is_superuser = False
        
        # Update active status
        edit_user.is_active = request.POST.get('is_active') == '1'
        edit_user.save()
        
        # Update profile
        profile = edit_user.userprofile
        profile.xp = int(request.POST.get('xp', profile.xp))
        profile.level = int(request.POST.get('level', profile.level))
        profile.bio = request.POST.get('bio', profile.bio)
        # Set teacher flag based on role selection
        profile.is_teacher = (role == 'guru')
        profile.save()
        
        messages.success(request, f'Data pengguna {edit_user.first_name or edit_user.username} berhasil diperbarui!')
        return redirect('admin_users')
    
    context = {
        'active_page': 'users',
        'edit_user': edit_user,
    }
    return render(request, 'dashboard/admin/user_edit.html', context)


@staff_required
def admin_user_delete(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user.is_superuser:
            messages.error(request, 'Tidak bisa menghapus superuser!')
        elif user == request.user:
            messages.error(request, 'Tidak bisa menghapus akun sendiri!')
        else:
            name = user.first_name or user.username
            user.delete()
            messages.success(request, f'Pengguna {name} berhasil dihapus.')
    return redirect('admin_users')


@staff_required
def admin_missions(request):
    course_filter = request.GET.get('course_id')
    
    if course_filter:
        missions = Mission.objects.filter(course_id=course_filter).order_by('order')
        filter_course = get_object_or_404(Course, id=course_filter)
    else:
        missions = Mission.objects.all().order_by('order')
        filter_course = None
    
    for m in missions:
        m.question_count = m.questions.count()
        m.completed_count = UserMissionProgress.objects.filter(
            mission=m, status='completed'
        ).count()
    
    courses = Course.objects.all().order_by('order')
    
    context = {
        'active_page': 'missions',
        'missions': missions,
        'courses': courses,
        'filter_course': filter_course,
    }
    return render(request, 'dashboard/admin/missions.html', context)


@staff_required
def admin_mission_create(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = None
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                pass
        
        mission = Mission.objects.create(
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            content=request.POST.get('content', ''),
            xp_reward=int(request.POST.get('xp_reward', 50)),
            order=int(request.POST.get('order', 0)),
            course=course,
            video_url=request.POST.get('video_url', ''),
            gamification_mode=request.POST.get('gamification_mode') or None,
        )
        if 'image' in request.FILES:
            mission.image = request.FILES['image']
        if 'background_image' in request.FILES:
            mission.background_image = request.FILES['background_image']
        mission.save()
        
        messages.success(request, f'Misi "{mission.title}" berhasil dibuat!')
        return redirect('admin_questions', mission_id=mission.id)
    
    courses = Course.objects.all().order_by('order')
    context = {
        'active_page': 'missions',
        'mission': None,
        'courses': courses,
    }
    return render(request, 'dashboard/admin/mission_form.html', context)


@staff_required
def admin_mission_edit(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    
    if request.method == 'POST':
        mission.title = request.POST.get('title', mission.title)
        mission.description = request.POST.get('description', mission.description)
        mission.content = request.POST.get('content', mission.content)
        mission.xp_reward = int(request.POST.get('xp_reward', mission.xp_reward))
        mission.order = int(request.POST.get('order', mission.order))
        
        course_id = request.POST.get('course_id')
        if course_id:
            try:
                mission.course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                mission.course = None
        else:
            mission.course = None
        
        mission.video_url = request.POST.get('video_url', mission.video_url)
        mission.gamification_mode = request.POST.get('gamification_mode') or None
        
        if 'image' in request.FILES:
            mission.image = request.FILES['image']
        if 'background_image' in request.FILES:
            mission.background_image = request.FILES['background_image']

        mission.save()
        
        messages.success(request, f'Misi "{mission.title}" berhasil diperbarui!')
        return redirect('admin_missions')
    
    courses = Course.objects.all().order_by('order')
    context = {
        'active_page': 'missions',
        'mission': mission,
        'courses': courses,
        'question_count': mission.questions.count(),
    }
    return render(request, 'dashboard/admin/mission_form.html', context)


@staff_required
def admin_mission_delete(request, mission_id):
    if request.method == 'POST':
        mission = get_object_or_404(Mission, id=mission_id)
        title = mission.title
        mission.delete()
        messages.success(request, f'Misi "{title}" berhasil dihapus.')
    return redirect('admin_missions')


@staff_required
def admin_questions(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    questions = mission.questions.all().order_by('order')
    
    # Calculate next order number
    next_order = (questions.last().order + 1) if questions.exists() else 1
    
    context = {
        'active_page': 'missions',
        'mission': mission,
        'questions': questions,
        'next_order': next_order,
    }
    return render(request, 'dashboard/admin/questions.html', context)


@staff_required
def admin_question_create(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text', '')
        order = int(request.POST.get('order', 0))
        correct_choice = request.POST.get('correct_choice', '1')
        
        question = Question.objects.create(
            mission=mission,
            text=question_text,
            order=order,
        )
        
        # Create choices
        for i in range(1, 5):
            choice_text = request.POST.get(f'choice_{i}', '')
            if choice_text.strip():
                Choice.objects.create(
                    question=question,
                    text=choice_text,
                    is_correct=(str(i) == correct_choice),
                )
        
        messages.success(request, 'Soal berhasil ditambahkan!')
    
    return redirect('admin_questions', mission_id=mission.id)


@staff_required
def admin_question_delete(request, mission_id, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, id=question_id, mission_id=mission_id)
        question.delete()
        messages.success(request, 'Soal berhasil dihapus.')
    return redirect('admin_questions', mission_id=mission_id)


# =========================================
# ADMIN COURSE VIEWS
# =========================================

@staff_required
def admin_courses(request):
    courses = Course.objects.all().order_by('order')
    
    for c in courses:
        c.mission_count = c.missions.count()
    
    context = {
        'active_page': 'courses',
        'courses': courses,
    }
    return render(request, 'dashboard/admin/courses.html', context)


@staff_required
def admin_course_create(request):
    if request.method == 'POST':
        course = Course.objects.create(
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            icon=request.POST.get('icon', 'fa-book'),
            order=int(request.POST.get('order', 0)),
            is_active=request.POST.get('is_active') == 'on',
        )
        messages.success(request, f'Kursus "{course.title}" berhasil dibuat!')
        return redirect('admin_courses')
    
    context = {
        'active_page': 'courses',
        'course': None,
    }
    return render(request, 'dashboard/admin/course_form.html', context)


@staff_required
def admin_course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        course.title = request.POST.get('title', course.title)
        course.description = request.POST.get('description', course.description)
        course.icon = request.POST.get('icon', course.icon)
        course.order = int(request.POST.get('order', course.order))
        course.is_active = request.POST.get('is_active') == 'on'
        course.save()
        
        messages.success(request, f'Kursus "{course.title}" berhasil diperbarui!')
        return redirect('admin_courses')
    
    context = {
        'active_page': 'courses',
        'course': course,
    }
    return render(request, 'dashboard/admin/course_form.html', context)


@staff_required
def admin_course_delete(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        title = course.title
        course.delete()
        messages.success(request, f'Kursus "{title}" berhasil dihapus.')
    return redirect('admin_courses')


@login_required(login_url='login')
def gamifikasi_level1(request):
    if request.method == 'POST':
        score = int(request.POST.get('score', 0))
        mission = Mission.objects.filter(order=1).first()
        if mission:
            progress, _ = UserMissionProgress.objects.get_or_create(user=request.user, mission=mission)
            if score >= 60:
                profile = request.user.userprofile
                profile.xp += mission.xp_reward
                profile.level = max(1, profile.xp // 500 + 1)
                profile.save()
                progress.status = 'completed'
                progress.completed_at = timezone.now()
                progress.save()
                messages.success(request, f'Selamat! Skor {score}/100. Misi Level 1 selesai!')
                return redirect('misi_selesai', mission_id=mission.id)
            else:
                messages.info(request, f'Skor {score}/100. Minimal 60 untuk lulus. Coba lagi!')
                return redirect('gamifikasi_level1')
    return render(request, 'dashboard/gamifikasi_level1.html')


@login_required(login_url='login')
def gamifikasi_level2(request):
    # Check if user has completed level 1
    level1_mission = Mission.objects.filter(order=1).first()
    if level1_mission:
        level1_progress = UserMissionProgress.objects.filter(
            user=request.user, 
            mission=level1_mission, 
            status='completed'
        ).exists()
        if not level1_progress:
            messages.error(request, 'Anda harus menyelesaikan Level 1 terlebih dahulu sebelum mengakses Level 2!')
            return redirect('gamifikasi_level1')
    
    if request.method == 'POST':
        score = int(request.POST.get('score', 0))
        mission = Mission.objects.filter(order=2).first()
        if mission:
            progress, _ = UserMissionProgress.objects.get_or_create(user=request.user, mission=mission)
            if score >= 70:
                profile = request.user.userprofile
                profile.xp += mission.xp_reward
                profile.level = max(1, profile.xp // 500 + 1)
                profile.save()
                progress.status = 'completed'
                progress.completed_at = timezone.now()
                progress.save()
                messages.success(request, f'Selamat! Skor {score}/100. Misi Level 2 selesai!')
                return redirect('misi_selesai', mission_id=mission.id)
            else:
                messages.info(request, f'Skor {score}/100. Minimal 70 untuk lulus. Coba lagi!')
                return redirect('gamifikasi_level2')
    return render(request, 'dashboard/gamifikasi_level2.html')


@login_required(login_url='login')
def gamifikasi_level3(request):
    # Check if user has completed level 2
    level2_mission = Mission.objects.filter(order=2).first()
    if level2_mission:
        level2_progress = UserMissionProgress.objects.filter(
            user=request.user, 
            mission=level2_mission, 
            status='completed'
        ).exists()
        if not level2_progress:
            messages.error(request, 'Anda harus menyelesaikan Level 2 terlebih dahulu sebelum mengakses Level 3!')
            return redirect('gamifikasi_level2')
    
    if request.method == 'POST':
        score = int(request.POST.get('score', 0))
        mission = Mission.objects.filter(order=3).first()
        if mission:
            progress, _ = UserMissionProgress.objects.get_or_create(user=request.user, mission=mission)
            if score >= 60:
                profile = request.user.userprofile
                profile.xp += mission.xp_reward
                profile.level = max(1, profile.xp // 500 + 1)
                profile.save()
                progress.status = 'completed'
                progress.completed_at = timezone.now()
                progress.save()
                messages.success(request, f'Selamat! Skor {score}/100. Misi Level 3 selesai!')
                return redirect('misi_selesai', mission_id=mission.id)
            else:
                messages.info(request, f'Skor {score}/100. Minimal 60 untuk lulus. Coba lagi!')
                return redirect('gamifikasi_level3')
    return render(request, 'dashboard/gamifikasi_level3.html')


@login_required(login_url='login')
def gamifikasi_level4(request):
    # Check if user has completed level 3
    level3_mission = Mission.objects.filter(order=3).first()
    if level3_mission:
        level3_progress = UserMissionProgress.objects.filter(
            user=request.user, 
            mission=level3_mission, 
            status='completed'
        ).exists()
        if not level3_progress:
            messages.error(request, 'Anda harus menyelesaikan Level 3 terlebih dahulu sebelum mengakses Level 4!')
            return redirect('gamifikasi_level3')
    
    if request.method == 'POST':
        score = int(request.POST.get('score', 0))
        mission = Mission.objects.filter(order=4).first()
        if mission:
            progress, _ = UserMissionProgress.objects.get_or_create(user=request.user, mission=mission)
            if score >= 60:
                profile = request.user.userprofile
                profile.xp += mission.xp_reward
                profile.level = max(1, profile.xp // 500 + 1)
                profile.save()
                progress.status = 'completed'
                progress.completed_at = timezone.now()
                progress.save()
                messages.success(request, f'Selamat! Skor {score}/100. Misi Level 4 selesai!')
                return redirect('misi_selesai', mission_id=mission.id)
            else:
                messages.info(request, f'Skor {score}/100. Minimal 60 untuk lulus. Coba lagi!')
                return redirect('gamifikasi_level4')
    return render(request, 'dashboard/gamifikasi_level4.html')


@login_required(login_url='login')
def gamifikasi_level5(request):
    # Check if user has completed level 4
    level4_mission = Mission.objects.filter(order=4).first()
    if level4_mission:
        level4_progress = UserMissionProgress.objects.filter(
            user=request.user, 
            mission=level4_mission, 
            status='completed'
        ).exists()
        if not level4_progress:
            messages.error(request, 'Anda harus menyelesaikan Level 4 terlebih dahulu sebelum mengakses Level 5!')
            return redirect('gamifikasi_level4')
    
    if request.method == 'POST':
        score = int(request.POST.get('score', 0))
        mission = Mission.objects.filter(order=5).first()
        if mission:
            progress, _ = UserMissionProgress.objects.get_or_create(user=request.user, mission=mission)
            if score >= 60:
                profile = request.user.userprofile
                profile.xp += mission.xp_reward
                profile.level = max(1, profile.xp // 500 + 1)
                profile.save()
                progress.status = 'completed'
                progress.completed_at = timezone.now()
                progress.save()
                messages.success(request, f'Selamat! Skor {score}/100. Misi Level 5 selesai!')
                return redirect('misi_selesai', mission_id=mission.id)
            else:
                messages.info(request, f'Skor {score}/100. Minimal 60 untuk lulus. Coba lagi!')
                return redirect('gamifikasi_level5')
    return render(request, 'dashboard/gamifikasi_level5.html')
