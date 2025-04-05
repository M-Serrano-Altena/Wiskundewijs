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

    let previousActiveLinkPrimary = null;
    let previousActiveLinkSecondary = null;
    let allOriginalHeaders = Array.from(document.querySelectorAll("h1, h2, h3, h4, h5, h6"));
    let allHeaders = Array.from(document.querySelectorAll("h1, h2, h3, h4, h5, h6"));
    let lastScrollY = window.scrollY;
    let lastActiveIndex = -1;

    let lastActiveId = null;
    let visibleHeaders = new Set(); // Track visible headers

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                visibleHeaders.add(entry.target); // Mark header as visible
            } else {
                visibleHeaders.delete(entry.target); // Remove header when out of view
            }
        });
        window.dispatchEvent(new Event("scroll")); // Trigger scroll event to check for closest header
        
    }, { threshold: 0.1 }); // Adjust threshold if needed

    const originalHeadersObserver = new MutationObserver((mutationsList) => {
        for (let mutation of mutationsList) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                const target = mutation.target;
                const targetId = target.getAttribute('href').substring(1); // Get the ID from the href
                const targetIndex = allHeaders.findIndex(header => header.id === targetId);
                if (target.classList.contains('md-nav__link--active') && targetIndex < lastActiveIndex) {
                    console.log('Removing active header:', target);
                    target.classList.remove('md-nav__link--active');
                }
            }
        }
    });

    allOriginalHeaders.forEach(header => {
        const config = { attributes: true, attributeFilter: ['class'] };
        if (!tocContainerPrimary || !tocContainerSecondary) return; // Ensure both containers exist

        const primaryTocLink = tocContainerPrimary.querySelector(`a[href="#${header.id}"]`);
        const secondaryTocLink = tocContainerSecondary.querySelector(`a[href="#${header.id}"]`);
        if (primaryTocLink) {
            originalHeadersObserver.observe(secondaryTocLink, config);
        }
        if (secondaryTocLink) {
            originalHeadersObserver.observe(primaryTocLink, config);
        }
    });
    
    
    // Step 2: Scroll Event - Find the closest visible header
    window.addEventListener('scroll', () => {
        const isScrollingDown = window.scrollY >= lastScrollY;
        lastScrollY = window.scrollY;
        let closestHeader = null;

        visibleHeaders.forEach(header => {
            const top = header.getBoundingClientRect().top;
            if (top >= 0 && top <= 150) { // Adjust 150 to fine-tune activation point
                if (!closestHeader || top < closestHeader.getBoundingClientRect().top) {
                    closestHeader = header;
                }
            }
        });

        if (visibleHeaders.size === 0 && !isScrollingDown) {
            currentHeader = allHeaders[lastActiveIndex]; // Get the last active header
            if (currentHeader && currentHeader.getBoundingClientRect().top > 0) {
                prev_index = Math.max(lastActiveIndex - 1, 0); // Go back to the previous section if no headers are visible when scrolling up
                closestHeader = allHeaders[prev_index]; // Get the previous header
            }
        }
            
    
        if (closestHeader && closestHeader.id !== lastActiveId) {
            updateToC(closestHeader.id, tocContainerSecondary);
            updateToC(closestHeader.id, tocContainerPrimary);
            lastActiveId = closestHeader.id;
        }
    });

    function markPassedHeaders(allHeaders, container) {
        allHeaders.forEach((header, index) => {
            const tocLink = container.querySelector(`a[href="#${header.id}"]`);
            if (!tocLink) return;
    
            if (index < lastActiveIndex) {
                tocLink.classList.add('md-nav__link--passed');
                tocLink.classList.remove('md-nav__link--active');
            } else if (index === lastActiveIndex) {
                tocLink.classList.add('md-nav__link--active');
                tocLink.classList.remove('md-nav__link--passed');
            } else {
                tocLink.classList.remove('md-nav__link--passed');
            }
        });
    }
    
    // Step 3: Update the Table of Contents highlighting
    function updateToC(activeId, container) {
        const tocLink = container.querySelector(`a[href="#${activeId}"]`);
        let previousActiveLink = null; // Reset previous active link for each update
        let isPrimary = container === tocContainerPrimary; // Check if the container is primary or secondary

        if (isPrimary) {
            previousActiveLink = previousActiveLinkPrimary; // Reset previous active link for each update
        } else {
            previousActiveLink = previousActiveLinkSecondary; // Reset previous active link for each update
        }


        if (tocLink) {
            if (previousActiveLink && tocLink !== previousActiveLink) {
                previousActiveLink.classList.remove('md-nav__link--active');
            }
            tocLink.classList.add('md-nav__link--active');
            if (isPrimary) {
                previousActiveLinkPrimary = tocLink;
            } else {
                previousActiveLinkSecondary = tocLink;
            }
            lastActiveIndex = allHeaders.findIndex(h => h.id === activeId);
        }

        markPassedHeaders(allHeaders, container);
    
    }

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
                // console.log(`Loaded: ${file}`);

                // Remove "not-observed" class (for styling purposes)
                el.classList.remove("not-observed");
                el.classList.add("observed");

                // Move to the next section
                index++;

                allHeaders = Array.from(document.querySelectorAll("h1, h2, h3, h4, h5, h6")); // Get all headers
                allHeaders.forEach(header => observer.observe(header)); // Observe all headers

                // Preemptively load the next section
                if (!use_observer || (index <= next_index && index + 1 < elements.length)) {
                    setTimeout(() => loadNext(), loading_delay); // Load it after 1 sec
                }

                if (sectionId && !sectionLoaded) {
                    const targetElement = document.querySelector(sectionId);
                    if (targetElement) {
                        targetElement.scrollIntoView({ behavior: "auto", block: "start" });
                        window.scrollBy(0, -69) // nice
                        window.dispatchEvent(new Event("scroll")); // Trigger scroll event to check for closest header
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
