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

    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.main-header nav ul');

    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!menuToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                menuToggle.classList.remove('active');
            }
        });

        // Close menu when clicking a link
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                menuToggle.classList.remove('active');
            });
        });
    }
});


document.getElementById('searchForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const searchQuery = document.getElementById('searchInput').value.trim();
    if (searchQuery) {
        window.location.href = `manga/${encodeURIComponent(searchQuery)}`;
    }
});






