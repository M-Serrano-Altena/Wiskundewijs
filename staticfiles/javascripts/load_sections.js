// import { mountTableOfContents, watchTableOfContents } from "assets/javascripts/src/templates/assets/javascripts/components/toc/index.ts";

document.addEventListener("DOMContentLoaded", function () {
    const elements = Array.from(document.querySelectorAll(".not-observed"));
    const use_observer = false; // Use IntersectionObserver for lazy loading
    const loading_delay = 100 * use_observer; // Delay between loading sections
    let index = 0;
    let next_index = 1; // Preload the next section

    let tocContainerPrimary = document.querySelector(
        "body > div.md-container > main > div > div.md-sidebar.md-sidebar--primary > div > div > nav > ul > li.md-nav__item.md-nav__item--active.md-nav__item--section.md-nav__item--nested > nav > ul > li.md-nav__item.md-nav__item--active > nav > ul.md-nav__list[data-md-component='toc']"
    );

    let tocContainerSecondary = document.querySelector(
        'body > div.md-container > main > div > div.md-sidebar.md-sidebar--secondary > div > div > nav > ul.md-nav__list[data-md-component="toc"]'
    );

    const sectionId = window.location.hash; // Get the current section ID from the URL
    let sectionLoaded = false;

    
    // Observer to detect when the next section is visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && entry.target.dataset.pending === "true") {
                entry.target.dataset.pending = "false"; // Prevent multiple triggers
                next_index++; // Allow the next section to be loaded
                observer.unobserve(entry.target); // Stop observing this element
                setTimeout(() => loadNext(), loading_delay); // Wait 1 second before loading
            }
        });
    }, { threshold: 0 }); // Trigger when the section is visible

    function loadNext() {
        if (index >= elements.length) return; // Stop when all are loaded

        const el = elements[index];
        const file = el.getAttribute("data-load");
        
        fetch(file)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Failed to load ${file}`);
                }
                return response.json();
            })
            .then(data => {
                el.innerHTML = data.content; // Load the content

                // Update TOC
                if (!tocContainerSecondary) {

                    tocContainerSecondary = document.querySelector(
                        'body > div.md-container > main > div > div.md-sidebar.md-sidebar--secondary > div > div > nav.md-nav.md-nav--secondary[aria-label="Inhoudsopgave"]'
                    );
                    createTocSecondary(tocContainerSecondary);
                    tocContainerSecondary = document.querySelector(
                        'body > div.md-container > main > div > div.md-sidebar.md-sidebar--secondary > div > div > nav > ul.md-nav__list[data-md-component="toc"]'
                    );
                }

                if (!tocContainerPrimary) {
                    tocContainerPrimary = document.querySelector(
                        "body > div.md-container > main > div > div.md-sidebar.md-sidebar--primary > div > div > nav > ul > li.md-nav__item.md-nav__item--active.md-nav__item--section.md-nav__item--nested > nav > ul > li.md-nav__item.md-nav__item--active"
                    );
                    createTocPrimary(tocContainerPrimary);
                    tocContainerPrimary = document.querySelector(
                        "body > div.md-container > main > div > div.md-sidebar.md-sidebar--primary > div > div > nav > ul > li.md-nav__item.md-nav__item--active.md-nav__item--section.md-nav__item--nested > nav > ul > li.md-nav__item.md-nav__item--active > nav > ul.md-nav__list[data-md-component='toc']"
                    );
                }

                mergeToc(data.toc);


                // Process LaTeX with MathJax
                return MathJax.typesetPromise([el]);
            })
            .then(() => {
                console.log(`Loaded: ${file}`);

                // Remove "not-observed" class (for styling purposes)
                el.classList.remove("not-observed");
                el.classList.add("observed");

                // Move to the next section
                index++;

                // If there's another section, observe it for visibility
                if (index < elements.length) {
                    elements[index].dataset.pending = "true"; // Mark it as "pending"
                    observer.observe(elements[index]); // Start observing
                }

                // Preemptively load the next section
                if (!use_observer || (index <= next_index && index + 1 < elements.length)) {
                    setTimeout(() => loadNext(), loading_delay); // Load it after 1 sec
                }

                if (sectionId && !sectionLoaded) {
                    const targetElement = document.querySelector(sectionId);
                    if (targetElement) {
                        targetElement.scrollIntoView({ behavior: "auto", block: "center" });
                        sectionLoaded = true; // Mark as loaded to prevent multiple scrolls
                    }
                }

            })
            .catch(error => {
                console.error(error);
                el.innerHTML = "<p>Error loading content.</p>";
                index++; // Move to the next even if there's an error
                if (index < elements.length) {
                    elements[index].dataset.pending = "true";
                    observer.observe(elements[index]);
                }
            });
    }

    // Start by loading the first section immediately
    loadNext();

    function createTocSecondary(container) {
        // Create the <label> element
        const label = document.createElement("label");
        label.classList.add("md-nav__title");
        label.setAttribute("for", "__toc");
    
        const span = document.createElement("span");
        span.classList.add("md-nav__icon", "md-icon");
        label.appendChild(span);
        label.innerHTML += " Inhoudsopgave"; // Add text after the span
    
        // Create the <ul> element
        const ul = document.createElement("ul");
        ul.classList.add("md-nav__list");
        ul.setAttribute("data-md-component", "toc");
    
        container.appendChild(label);
        container.appendChild(ul);
    }

    function createTocPrimary(container) {
        const label = document.createElement("label");
        label.classList.add("md-nav__link");
        label.setAttribute("for", "__toc");

        const existingAnchor = container.querySelector("a");

        const labelSpan = document.createElement("span");
        labelSpan.classList.add("md-ellipsis");
        labelSpan.textContent = existingAnchor.textContent;
        label.appendChild(labelSpan);
    
        const labelIcon = document.createElement("span");
        labelIcon.classList.add("md-nav__icon", "md-icon");
        label.appendChild(labelIcon);

        const nav = document.createElement("nav");
        nav.classList.add("md-nav", "md-nav--secondary");
        nav.setAttribute("aria-label", "Inhoudsopgave");

        createTocSecondary(nav);

        container.insertBefore(label, existingAnchor);
        container.appendChild(nav);

    }

    // Function to merge TOC
    function mergeToc(newTocHtml) {
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = newTocHtml;

    
        if (!tocContainerSecondary && !tocContainerPrimary) {
            console.warn("TOC containers not found.");
            return;
        }

        // Track occurrences of each header ID
        const idCounts = new Map();
        document.querySelectorAll("h1, h2, h3, h4, h5, h6").forEach(header => {
            if (header.id) {
                idCounts.set(header.id, (idCounts.get(header.id) || 0) + 1);
            }
        });
        let duplicateIds = new Set([...idCounts].filter(([_, count]) => count > 1).map(([id]) => id));

        idMapCounter = new Map();
        duplicateIds.forEach(id => {
            idMapCounter.set(id, 1);
        });
    
        // add the new list of items to the existing toc
        tempDiv.querySelectorAll("li").forEach(newList => {
            const anchor = newList.querySelector("a");
            if (!anchor) return; // Skip if no anchor is found

            const href = anchor.getAttribute("href");
            if (href.startsWith("#")) {
                let baseId = href.substring(1); // Remove the '#' from the href
                let newId = baseId;

                // Only rename if it's a duplicate
                if (duplicateIds.has(baseId)) {
                    while (document.getElementById(newId)) {
                        let counter = idMapCounter.get(newId) || 1; // Start from 1 if not set                            
                        idMapCounter.set(newId, counter + 1);

                        // update newId and add it to the map
                        newId = `${baseId}_${counter}`;

                        if (!idMapCounter.has(newId)) {
                            idMapCounter.set(newId, 1); // add the new ID to the map
                        }
                    }
                    
                    // Update the duplicateIds set if new ID is duplicate
                    for (const [id, count] of idMapCounter) {
                        if (count >= 2) {
                            duplicateIds.add(id); // Add the ID to duplicateIds set if its count is 2 or greater
                        }
                    }


                    // Update anchor link
                    anchor.setAttribute("href", `#${newId}`);

                    // Update the actual header ID

                    // Get all elements with the same baseId
                    const targetSections = document.querySelectorAll(`#${baseId}`);

                    // If there are multiple elements with the same ID, get the last one
                    const targetSection = targetSections[targetSections.length - 1];
                    if (targetSection) {
                        targetSection.setAttribute("id", newId);
                    }
                }
            }
        });

        tempDiv.querySelectorAll(":scope > li").forEach(newList => {
            // Append the new list item to the existing toc
            if (tocContainerPrimary) {
                tocContainerPrimary.appendChild(newList.cloneNode(true));
            }
            if (tocContainerSecondary) {
                tocContainerSecondary.appendChild(newList.cloneNode(true));
            }
        });
    }


});
