function showContent(sectionId) {
    const sections = document.getElementsByClassName('content-section');
    for (const section of sections) {
        section.style.display = section.id === sectionId ? 'block' : 'none';
    }

    // Update active state of navigation links
    const links = document.getElementsByClassName('nav')[0].getElementsByTagName('a');
    for (const link of links) {
        if (link.onclick && link.onclick.toString().includes(sectionId)) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const defaultSection = document.getElementsByClassName('nav')[0].getElementsByTagName('a')[0].getAttribute('onclick');
    const sectionId = defaultSection.match(/'(.*?)'/)[1];
    showContent(sectionId);
});