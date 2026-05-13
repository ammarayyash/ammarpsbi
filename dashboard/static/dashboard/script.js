document.addEventListener('DOMContentLoaded', () => {
    // =========================================================
    // 0. THEME SWITCHER
    // =========================================================
    const themes = ['dark', 'dim', 'light'];
    const themeLabels = ['Tema Malam', 'Tema Sedang', 'Tema Terang'];
    const themeIcons = ['fa-moon', 'fa-cloud-moon', 'fa-sun'];
    
    let currentThemeIndex = parseInt(localStorage.getItem('themeIndex') || '0');
    const themeBtn = document.getElementById('themeToggleBtn');
    
    function applyTheme(index) {
        document.documentElement.setAttribute('data-theme', themes[index]);
        if(themeBtn) {
            themeBtn.querySelector('.sidebar-text').innerText = themeLabels[index];
            themeBtn.querySelector('i').className = `fa-solid ${themeIcons[index]}`;
        }
    }
    
    // Apply initially
    applyTheme(currentThemeIndex);
    
    if(themeBtn) {
        themeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            currentThemeIndex = (currentThemeIndex + 1) % themes.length;
            localStorage.setItem('themeIndex', currentThemeIndex);
            applyTheme(currentThemeIndex);
            
            // Optional visual feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => this.style.transform = 'scale(1)', 150);
        });
    }

    // 1. Sidebar Active State Handling Based on URL
    const currentLocation = location.pathname.split("/").pop();
    const navLinks = document.querySelectorAll('.sidebar-nav a');
    
    navLinks.forEach(link => {
        const linkHref = link.getAttribute('href');
        if (linkHref === currentLocation || (currentLocation === '' && linkHref === 'index.html')) {
            document.querySelectorAll('.sidebar-nav li').forEach(nav => nav.classList.remove('active'));
            link.parentElement.classList.add('active');
        }
    });

    // 2. Animate Progress Bars on Load
    const progressBars = document.querySelectorAll('.progress-bar, .path-progress-bar');
    progressBars.forEach(bar => {
        const targetWidth = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.transition = 'width 1.5s cubic-bezier(0.2, 0.8, 0.2, 1)';
            bar.style.width = targetWidth;
        }, 300);
    });

    // 3. CTA Button Interaction — only for real <button> elements, not <a> links
    const ctaBtns = document.querySelectorAll('button.cta-button');
    ctaBtns.forEach(ctaBtn => {
        ctaBtn.addEventListener('click', function(e) {
            if(this.classList.contains('loading')) return;
            if(this.type === 'submit') return; // let forms submit normally
            
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Memuat...';
            this.style.opacity = '0.8';
            this.classList.add('loading');
            
            setTimeout(() => {
                this.innerHTML = originalText;
                this.style.opacity = '1';
                this.classList.remove('loading');
            }, 1500);
        });
    });

    // 4. Badge Hover Micro-interaction
    const badges = document.querySelectorAll('.badge-item');
    badges.forEach(badge => {
        if (badge.classList.contains('earned')) {
            badge.addEventListener('mouseenter', function() {
                this.style.transform = `scale(1.15) rotate(${Math.random() * 10 - 5}deg)`;
                this.style.filter = 'drop-shadow(0 0 10px rgba(138, 43, 226, 0.6))';
            });
            badge.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1) rotate(0deg)';
                this.style.filter = '';
            });
        }
        
        badge.addEventListener('click', function() {
            const badgeName = this.getAttribute('title');
            if (this.classList.contains('earned')) {
                showToast(`Badge "${badgeName}" telah diraih! Luar biasa.`, 'success');
            } else {
                showToast(`Badge "${badgeName}" masih terkunci. Terus belajar!`, 'info');
            }
        });
    });

    // 5. Module Click Interaction (Simulate completing a module)
    const activeModules = document.querySelectorAll('.module-item.active');
    activeModules.forEach(mod => {
        mod.addEventListener('click', function(e) {
            // We should let normal link navigation happen if it's a real link, 
            // but the original code had a visual simulator. We'll keep it but let the navigation occur.
        });
    });

    // 6. Interactive Toast Notification System
    function showToast(message, type = 'info') {
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container';
            document.body.appendChild(toastContainer);
            
            // Add basic styles for toast container
            const style = document.createElement('style');
            style.innerHTML = `
                .toast-container { position: fixed; bottom: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 10px; }
                .toast { padding: 15px 25px; border-radius: 12px; color: white; font-weight: 500; font-size: 0.95rem; backdrop-filter: blur(10px); transform: translateX(120%); transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55); display: flex; align-items: center; gap: 10px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
                .toast.show { transform: translateX(0); }
                .toast.success { background: rgba(39, 174, 96, 0.9); border: 1px solid #2ecc71; }
                .toast.info { background: rgba(138, 43, 226, 0.9); border: 1px solid #9b59b6; }
            `;
            document.head.appendChild(style);
        }

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = type === 'success' ? '<i class="fa-solid fa-circle-check"></i>' : '<i class="fa-solid fa-bell"></i>';
        toast.innerHTML = `${icon} <span>${message}</span>`;
        
        toastContainer.appendChild(toast);
        
        setTimeout(() => toast.classList.add('show'), 10);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 400);
        }, 3000);
    }

    // 7. Page Transition Effect removed based on user request
    const allLinks = document.querySelectorAll('a:not([target="_blank"])');
    allLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') {
                e.preventDefault(); 
            }
        });
    });

    // 8. Streak Daily Click
    const streakCard = document.querySelector('.streak-card');
    if(streakCard) {
        const streakNumber = streakCard.querySelector('.streak-number');
        streakCard.addEventListener('click', () => {
            if (streakNumber) {
                showToast(`Kamu punya streak ${streakNumber.innerText} Hari berturut-turut!`, 'success');
            }
        });
        streakCard.style.cursor = 'pointer';
    }

    // =========================================================
    // 9. SIDEBAR TOGGLE (Collapse / Expand)
    // =========================================================
    const sidebar = document.getElementById('appSidebar');
    const toggleBtn = document.getElementById('sidebarToggle');
    const container = document.querySelector('.dashboard-container');

    function applySidebarState(collapsed) {
        if (!sidebar) return;
        if (collapsed) {
            sidebar.classList.add('collapsed');
            if (container) container.classList.add('sidebar-collapsed');
        } else {
            sidebar.classList.remove('collapsed');
            if (container) container.classList.remove('sidebar-collapsed');
        }
    }

    // Restore state from localStorage
    const savedCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    applySidebarState(savedCollapsed);

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            const isCollapsed = sidebar.classList.contains('collapsed');
            applySidebarState(!isCollapsed);
            localStorage.setItem('sidebarCollapsed', !isCollapsed);
        });
    }

    // =========================================================
    // 10. AVATAR UPLOAD PREVIEW
    // =========================================================
    const avatarInput = document.getElementById('avatarInput');
    const avatarPreview = document.getElementById('avatarPreview');
    const avatarSubmitBtn = document.getElementById('avatarSubmitBtn');

    if (avatarInput) {
        avatarInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    avatarPreview.src = e.target.result;
                    if (avatarSubmitBtn) {
                        avatarSubmitBtn.style.display = 'inline-flex';
                    }
                };
                reader.readAsDataURL(this.files[0]);
                showToast('Foto dipilih. Klik "Simpan Foto Profil" untuk mengunggah.', 'info');
            }
        });
    }
});
