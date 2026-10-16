/* Hai panel luôn giữ trong DOM; chuyển tab chỉ đổi trạng thái hiển thị. */
(() => {
    const tabs = [document.getElementById('tab-lab'), document.getElementById('tab-theory')];
    const panels = [document.getElementById('panel-lab'), document.getElementById('panel-theory')];
    const positions = [0, 0];
    let active = 0;
    function selectTab(index, focus = false) {
        if (index !== active) {
            positions[active] = window.scrollY;
            tabs.forEach((tab, i) => {
                tab.setAttribute('aria-selected', String(i === index));
                tab.tabIndex = i === index ? 0 : -1;
                panels[i].hidden = i !== index;
            });
            active = index;
            // Gantt dùng CSS theo phần trăm, tự đo lại khi panel được hiện.
            window.scrollTo({ top: positions[index], behavior: 'instant' });
        }
        if (focus) tabs[index].focus({ preventScroll: true });
    }
    tabs.forEach((tab, i) => {
        tab.addEventListener('click', () => selectTab(i));
        tab.addEventListener('keydown', event => {
            let target;
            if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') target = 1 - i;
            if (event.key === 'Home') target = 0;
            if (event.key === 'End') target = 1;
            if (target !== undefined) {
                event.preventDefault();
                selectTab(target, true);
            }
        });
    });
    // Liên kết ở header vẫn mở đúng vùng thử nghiệm từ tab lý thuyết.
    document.querySelectorAll('.section-nav a, .skip-link, .page-footer a').forEach(link => {
        link.addEventListener('click', () => selectTab(0));
    });
    const toc = [...document.querySelectorAll('.theory-toc a')];
    function markSection(id) {
        toc.forEach(link => {
            if (link.getAttribute('href') === `#${id}`) link.setAttribute('aria-current', 'location');
            else link.removeAttribute('aria-current');
        });
    }
    toc.forEach(link => link.addEventListener('click', () => markSection(link.hash.slice(1))));
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(entries => {
            if (active !== 1) return;
            const visible = entries.filter(entry => entry.isIntersecting)
                .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
            if (visible.length) markSection(visible[0].target.id);
        }, { rootMargin: '-8% 0px -65% 0px', threshold: 0 });
        document.querySelectorAll('.theory-section').forEach(section => observer.observe(section));
    }
})();
