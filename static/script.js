

// #DEV: code for slide careousel
$(document).ready(function () {
    $('.owl-carousel').owlCarousel({
        loop: true,
        nav: true,
        dots: true,
        autoplay: true,
        mouseDrag: false,
        animateOut: 'slideOutUp',
        responsive: {
            0: {
                items: 1,
            },
            600: {
                items: 1,
            },
            1000: {
                items: 1,
            }
        }
    });
});
//#DEV: Code for counter       
function startCounter(entries, observer) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const counters = document.querySelectorAll(".counter");
            counters.forEach(counter => {
                const target = +counter.getAttribute("data-target");
                let count = 0;
                const increment = target / 100;

                const updateCount = () => {
                    if (count < target) {
                        count += increment;
                        counter.innerText = Math.floor(count);
                        requestAnimationFrame(updateCount);
                    } else {
                        counter.innerText = target;
                    }
                };

                updateCount();
            });

            observer.disconnect();
        }
    });
}
document.addEventListener("DOMContentLoaded", function () {
    const cardData = [
        {
            img: "/static/images/A-frame/A-20.jpg",
            title: '"A" Frame',
            description: "A timeless and iconic design, perfect for high-end resorts offering a unique blend of luxury and nature.",
            link: "/designs/A-Frame"
        },
        {
            img: "/static/images/prefabricated/p-3.jpg",
            title: "Prefabricated Luxury House",
            description: "A sophisticated, customizable home that combines modern design with luxurious comfort for discerning owners.",
            link: "/designs/Prefabricated-Luxury-house"
        },
        {
            img: "/static/images/double-storey/14.jpg",
            title: "Double Storey",
            description: "A stylish and efficient double Storey house offering modern luxury in a compact space.",
            link: "/designs/Double-Storey-Houses"
        },
        {
            img: "/static/images/A-frame/A-11.jpg",
            title: "Wooden House",
            description: "A charming wooden abode offering a luxurious, nature-inspired retreat with spacious living options.",
            link: "/designs/Wooden-House"
        },
        {
            img: "/static/images/Wooden/w-1.jpg",
            title: "Wooden Resort",
            description: "A stunning wooden resort combining elegance and nature, perfect for upscale vacation retreats.",
            link: "/designs/Wooden-Resort"
        },
        {
            img: "/static/images/A-frame/A-7.jpg",
            title: '"A" Frame Cottages',
            description: "Elegant A-frame cottages designed to offer luxury and comfort in exclusive resort settings.",
            link: "/designs/A-Frame-Cottages"
        },
        {
            img: "/static/images/portable/p-1.jpg",
            title: "Portable House",
            description: "A luxurious, portable living space offering refined comfort wherever you go.",
            link: "/designs/Portable-House"
        },
        {
            img: "/static/images/prefabricated/p-1.jpg",
            title: "Prefabricated Wooden House",
            description: "A beautifully crafted wooden home that combines sleek design with luxurious living.",
            link: "/designs/Prefabricated-Wooden-house"
        },
        {
            img: "/static/images/modular/m-1.jpg",
            title: 'Modular Cottage',
            description: "A luxury modular cottage offering customizable layouts with elegance and practicality.",
            link: "/designs/Modular-Cottage"
        },
        {
            img: "/static/images/prefabricated/p-2.jpg",
            title: "Prefabricated House",
            description: "A sleek and stylish prefabricated home, designed for modern living with luxurious finishes.",
            link: "/designs/Prefabricated-house"
        },
        {
            img: "/static/images/portable/p-2.jpg",
            title: "Portable Cabin",
            description: "A luxurious, portable cabin offering sophistication and comfort in any location.",
            link: "/designs/Portable-Cabin"
        },
        {
            img: "/static/images/portable/p-3.jpg",
            title: 'Office Cabin',
            description: "A refined, portable office cabin designed to provide luxury and functionality on the move.",
            link: "/designs/Office-Cabin"
        }
    ];

    const cardContainer = document.getElementById("card-container");
    cardContainer.classList.add(
        "grid", "grid-cols-1", "sm:grid-cols-2", "lg:grid-cols-3",
        "gap-4", "md:gap-4", "max-w-full", "mx-auto", "p-1"
    );

    cardData.forEach(card => {
        const cardElement = document.createElement("a");
        cardElement.href = card.link;
        cardElement.classList.add(
            "relative",
            "bg-white", "shadow-lg", "rounded-lg", "overflow-hidden",
            "w-full", "p-1", "md:p-3",
            "flex", "flex-col", "min-h-[400px]", "md:min-h-[200px]",
            "hover:shadow-xl", "transition-transform", "duration-300",
            "hover:scale-[1.02]",
            "no-underline", "text-inherit"
        );

        cardElement.innerHTML = `
            <div class="relative group overflow-hidden rounded-md">
                <img src="${card.img}" alt="${card.title}" class="w-full h-80 object-cover transition-transform duration-300 group-hover:scale-105">
                <div class="absolute inset-0 bg-black bg-opacity-70 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center text-white text-lg font-semibold text-center px-4">
                    Explore details and Gallery
                </div>
            </div>
            <div class="p-3 flex-grow">
                <h2 class="text-xl md:text-2xl font-bold mb-1">${card.title}</h2>
                <p class="text-sm md:text-lg text-gray-700">${card.description}</p>
            </div>
        `;

        cardContainer.appendChild(cardElement);
    });
});


//    DEV: code for scrollbar indicator 
document.addEventListener("scroll", function () {
    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrollPercentage = Math.round((scrollTop / scrollHeight) * 100);

    const progressIndicator = document.getElementById("progressIndicator");
    const progressText = document.getElementById("progressText");
    const progressCircle = document.getElementById("progressCircle");

    // Show indicator when scrolling starts
    if (scrollTop > 50) {
        progressIndicator.classList.add("show");
    } else {
        progressIndicator.classList.remove("show");
    }

    // Change text to arrow at 100%
    if (scrollPercentage === 100) {
        progressText.innerHTML = '<i class="fa-solid fa-arrow-up-long arrow"></i>';
    } else {
        progressText.textContent = scrollPercentage + "%";
    }

    // Update progress bar
    const totalLength = 163.36;
    const offset = totalLength - (scrollPercentage / 100) * totalLength;
    progressCircle.style.strokeDashoffset = offset;
});

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: "smooth" });
}
// ########################################################

const observer = new IntersectionObserver(startCounter, { threshold: 0.5 });
observer.observe(document.querySelector(".bg-black"));


// #DEV: code for skill bar

document.addEventListener("DOMContentLoaded", function () {
    const skillBars = document.querySelectorAll(".skill-bar");
    const section = document.querySelector("#skills-section");

    const observer = new IntersectionObserver(
        (entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    skillBars.forEach(bar => {
                        const width = bar.getAttribute("data-width");
                        bar.style.width = width + "%";
                        bar.style.transition = "width 2s ease-in-out";

                        // Find the number element next to the skill bar
                        const percentageSpan = bar.parentElement.previousElementSibling.querySelector(".percentage-count");

                        // Start counting animation
                        animateCount(percentageSpan, width);
                    });
                    observer.unobserve(section); // Stop observing after first animation
                }
            });
        },
        { threshold: 0.3 }
    );

    if (section) {
        observer.observe(section);
    }
});

// Function to animate the counter
function animateCount(element, targetValue) {
    let start = 0;
    let end = parseInt(targetValue);
    let duration = 2000; // 2 seconds
    let increment = Math.ceil(end / (duration / 20)); // Calculate step increment

    let timer = setInterval(() => {
        start += increment;
        if (start > end) start = end;
        element.textContent = start + "%";
        if (start >= end) {
            clearInterval(timer);
        }
    }, 20); // Update every 20ms for a smooth effect
}

// #DEV: code for review section
const testimonials = [
  {
    name: "Neha Verma",
    role: "Product Manager, GrowFast",
    review: "Reliable, strategic, and supportive. Definitely helped us scale.",
    rating: 4.5,
    image: "../static/images/person.jpg"
  },
  {
    name: "Harsh Tiwari",
    role: "CEO, DevDart",
    review: "A good experience overall with solid support.",
    rating: 4.0,
    image: "../static/images/person.jpg"
  },
  {
    name: "Priya Raj",
    role: "Operations Lead, EcoChain",
    review: "Service quality is top-notch. We saw improvements quickly.",
    rating: 5.0,
    image: "../static/images/person.jpg"
  },
  {
    name: "Kabir Malhotra",
    role: "Marketing Head, SnapWorld",
    review: "From strategy to execution, they exceeded our expectations.",
    rating: 4.5,
    image: "../static/images/person.jpg"
  },
  {
    name: "Ananya Desai",
    role: "Co-founder, GreenBay",
    review: "Their insights were actionable and helped our startup grow.",
    rating: 4.8,
    image: "../static/images/person.jpg"
  },
  {
    name: "Rohan Singh",
    role: "CTO, ByteBridge",
    review: "Clear communication and timely delivery. Very satisfied.",
    rating: 4.2,
    image: "../static/images/person.jpg"
  }
];

// Star rating logic
function generateStarRating(rating) {
  const fullStars = Math.floor(rating);
  const halfStar = rating % 1 >= 0.5 ? 1 : 0;
  const emptyStars = 5 - fullStars - halfStar;

  return (
    '★'.repeat(fullStars) +
    (halfStar ? '⯨' : '') +
    '☆'.repeat(emptyStars)
  );
}

// Generate testimonial cards
function generateTestimonialCards() {
  const swiperWrapper = document.querySelector(".swiper-wrapper");

  testimonials.forEach(testimonial => {
    const card = `
      <div class="swiper-slide">
        <div class="testimonial-card p-4 border rounded-lg bg-gray-50">
          <div class="profile-section flex items-center gap-4 mb-3">
            <img src="${testimonial.image}" alt="${testimonial.name}" class="w-14 h-14 rounded-full object-cover">
            <div class="profile-info text-left">
              <strong class="block text-sm">${testimonial.name}</strong>
              <p class="text-xs text-gray-500">${testimonial.role}</p>
              <div class="text-yellow-500 text-xl font-semibold mt-1">${generateStarRating(testimonial.rating)} <span class="text-gray-400 text-base">(${testimonial.rating})</span></div>
            </div>
          </div>
          <div class="separator my-2 border-t border-gray-300"></div>
          <p class="review text-sm text-gray-700">${testimonial.review}</p>
        </div>
      </div>
    `;
    swiperWrapper.insertAdjacentHTML("beforeend", card);
  });
}

// On DOM load
document.addEventListener("DOMContentLoaded", () => {
  generateTestimonialCards();

  // Swiper init
  const swiper = new Swiper(".testimonial-slider", {
    loop: true,
    autoplay: {
      delay: 3000,
      disableOnInteraction: false
    },
    slidesPerView: "auto",
    spaceBetween: 20,
    breakpoints: {
      320: { slidesPerView: 1, spaceBetween: 10 },
      768: { slidesPerView: 2, spaceBetween: 15 },
      1024: { slidesPerView: 3, spaceBetween: 20 },
      1440: { slidesPerView: 4, spaceBetween: 25 }
    }
  });
});


// #DEV: code for plan with us part parallex with zoom effect
document.addEventListener('DOMContentLoaded', () => {
    gsap.registerPlugin(ScrollTrigger);
    gsap.to("#parallax-image", {
        scrollTrigger: {
            trigger: ".parallax-section",
            start: "top bottom",
            end: "bottom top",
            scrub: 1
        },
        scale: 1.5,
        yPercent: 20,
        ease: "none"
    });
    gsap.fromTo("#parallax-text",
        { y: 50, opacity: 0.8, scale: 0.95 },
        {
            y: 0,
            opacity: 1,
            scale: 1,
            scrollTrigger: {
                trigger: ".parallax-section",
                start: "top bottom",
                end: "center center",
                scrub: 1
            },
            ease: "power2.out"
        }
    );
    function updateHeight() {
        const section = document.querySelector('.parallax-section');
        if (window.innerWidth >= 1024) {
            section.style.height = '600px';
        } else if (window.innerWidth >= 768) {
            section.style.height = '500px';
        } else {
            section.style.height = '400px';
        }
    }
    window.addEventListener('resize', updateHeight);
    updateHeight();
});

// #DEV: Project section image slider Code
const track = document.getElementById('carouselTrack');
const slides = document.querySelectorAll('.carousel-slide');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
let currentIndex = 0;
let autoSlideInterval;
const slideInterval = 2500; // 3 seconds

function updateCarousel() {
    const slideWidth = slides[0].offsetWidth;
    const gap = 24; // matches your gap-6 (6 * 4px = 24px)
    track.style.transform = `translateX(-${currentIndex * (slideWidth + gap)}px)`;

    // Hide/show buttons based on position
    prevBtn.style.display = currentIndex === 0 ? 'none' : 'block';
    nextBtn.style.display = currentIndex >= slides.length - 1 ? 'none' : 'block';
}

function nextSlide() {
    if (currentIndex >= slides.length - 1) {
        currentIndex = 0; // Reset to first slide
    } else {
        currentIndex++;
    }
    updateCarousel();
}

function prevSlide() {
    if (currentIndex <= 0) {
        currentIndex = slides.length - 1; // Go to last slide
    } else {
        currentIndex--;
    }
    updateCarousel();
}

function startAutoSlide() {
    autoSlideInterval = setInterval(nextSlide, slideInterval);
}

function stopAutoSlide() {
    clearInterval(autoSlideInterval);
}

// Initialize
updateCarousel();
startAutoSlide();

// Event listeners
nextBtn.addEventListener('click', () => {
    stopAutoSlide();
    nextSlide();
    startAutoSlide();
});

prevBtn.addEventListener('click', () => {
    stopAutoSlide();
    prevSlide();
    startAutoSlide();
});


// Handle window resize
window.addEventListener('resize', () => {
    updateCarousel();
});