/* Áp dụng trước CSS để tránh nháy sai nền; lỗi lưu trữ không chặn ứng dụng. */
(() => {
    const root = document.documentElement;
    const key = 'scheduling-theme';
    let theme = 'light';
    try {
        if (localStorage.getItem(key) === 'dark') theme = 'dark';
    } catch (_) { /* Trình duyệt có thể chặn lưu trữ. */ }

    function apply(value) {
        theme = value;
        root.dataset.theme = value;
        const meta = document.querySelector('meta[name="theme-color"]');
        if (meta) meta.content = value === 'light' ? '#ffffff' : '#28385e';
        const toggle = document.getElementById('themeToggle');
        if (toggle) toggle.setAttribute('aria-checked', String(value === 'light'));
    }
    apply(theme);
    document.addEventListener('DOMContentLoaded', () => {
        apply(theme);
        document.getElementById('themeToggle').addEventListener('click', () => {
            apply(theme === 'dark' ? 'light' : 'dark');
            try { localStorage.setItem(key, theme); } catch (_) { /* Vẫn đổi được trong phiên. */ }
        });
    }, { once: true });
})();
