document.addEventListener("DOMContentLoaded", function() {
    // Function to handle auto-scrolling
    function setupAutoScroll(containerSelector) {
        const scrollContainer = document.querySelector(containerSelector);
        if (!scrollContainer) return; // Exit if the container is not found
        
        let isScrolling = true;
        let scrollDirection = 1; // 1 for right, -1 for left

        function autoScroll() {
            if (isScrolling) {
                scrollContainer.scrollBy({ 
                    left: scrollDirection, 
                    behavior: 'smooth' 
                });

                // Check if the scroll has reached the right end
                if (scrollContainer.scrollLeft + scrollContainer.clientWidth >= scrollContainer.scrollWidth) {
                    scrollDirection = -1; // Change direction to left
                }

                // Check if the scroll has reached the left end
                if (scrollContainer.scrollLeft <= 0) {
                    scrollDirection = 1; // Change direction to right
                }
            }
            requestAnimationFrame(autoScroll);
        }

        // Start the scrolling function
        autoScroll();

        // Event listeners to pause/resume scrolling
        scrollContainer.addEventListener('mouseover', () => isScrolling = false);
        scrollContainer.addEventListener('mouseout', () => isScrolling = true);
    }

    // Setup auto-scrolling for both containers
    setupAutoScroll('.manga-scroll');
    setupAutoScroll('.recommended-scroll');
});
