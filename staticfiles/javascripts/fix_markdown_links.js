document.addEventListener("DOMContentLoaded", function () {
    console.log("Fixing markdown links...");

    // Select all <a> tags with href that contains ".md#" 
    const links = document.querySelectorAll('a[href*=".md#"]');
    
    links.forEach(link => {
        console.log("Fixing link: ", link.href);
        
        // Get the current href
        link.href = link.href.replace(".md#", "/#");

        console.log("Updated link: ", link.href);
    });
});