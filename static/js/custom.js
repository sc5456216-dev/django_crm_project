// Custom JS
console.log('Custom JS loaded.');

// Auto-close sidebar on link click (mobile)
document.addEventListener('DOMContentLoaded', function() {
    const sidebarCollapse = document.getElementById('sidebarNav');
    if (sidebarCollapse) {
        const links = sidebarCollapse.querySelectorAll('.nav-link');
        links.forEach(link => {
            link.addEventListener('click', () => {
                const bsCollapse = bootstrap.Collapse.getInstance(sidebarCollapse);
                if (bsCollapse) {
                    bsCollapse.hide();
                }
            });
        });
    }
});