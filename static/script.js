// script.js
document.addEventListener("DOMContentLoaded", function() {
    const scrollContainer = document.querySelector('.manga-scroll');
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
    
    scrollContainer.addEventListener('mouseover', () => isScrolling = false);
    scrollContainer.addEventListener('mouseout', () => isScrolling = true);
    
    autoScroll();
});
