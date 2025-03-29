document.addEventListener("DOMContentLoaded", function () {
    const hash = window.location.hash;
    
    if (hash) {
        const targetSection = document.querySelector(hash);
        
        if (targetSection) {
            targetSection.scrollIntoView();
        } else {
            window.addEventListener('sectionLoaded', function onSectionLoaded(event) {
                if (event.detail.sectionId === hash) {
                    const targetSection = document.querySelector(hash);
                    if (targetSection) {
                        targetSection.scrollIntoView();
                        window.removeEventListener('sectionLoaded', onSectionLoaded);
                    }
                }
            });
        }
    }

    function triggerSectionLoaded(sectionId) {
        window.dispatchEvent(new CustomEvent('sectionLoaded', {
            detail: { sectionId: sectionId }
        }));
    }

    // Make sure to trigger this event when sections are loaded
    // Example inside your loadNext() function
    // triggerSectionLoaded(sectionId);
});
