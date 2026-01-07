/**
 * Mobile Sidebar Toggle
 * Handles opening and closing of mobile sidebar
 */
function toggleMobileSidebar() {
    const mobileSidebar = document.getElementById('mobileSidebar');
    if (mobileSidebar) {
        mobileSidebar.classList.toggle('hidden');
    }
}
