const slidesContainer = document.querySelector('.slides');
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');

let index = 0;
const totalSlides = slides.length;
let interval = setInterval(nextSlide, 3000);

// Add margins between slides using inline style
slides.forEach(slide => {
  slide.style.margin = '0 15px';
  slide.style.flex = '0 0 calc(100% - 30px)';
});

slidesContainer.style.display = 'flex';
slidesContainer.style.transition = 'transform 0.5s ease-in-out';

// Show the correct slide
function showSlide(i) {
  slidesContainer.style.transform = `translateX(-${i * (100 + 3)}%)`;
  dots.forEach(dot => dot.classList.remove('active'));
  dots[i].classList.add('active');
}

// Go to the next slide
function nextSlide() {
  index = (index + 1) % totalSlides;
  showSlide(index);
}

// Click on dots
dots.forEach((dot, i) => {
  dot.addEventListener('click', () => {
    index = i;
    showSlide(index);
    resetInterval();
  });
});

// Reset timer on manual change
function resetInterval() {
  clearInterval(interval);
  interval = setInterval(nextSlide, 3000);
}

// Initialize
showSlide(index);