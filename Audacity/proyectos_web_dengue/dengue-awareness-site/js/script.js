document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault(); // Previene el comportamiento de anclaje por defecto

            const targetId = this.getAttribute('href'); // Obtiene el ID del destino
            const targetElement = document.querySelector(targetId); // Encuentra el elemento destino

            if (targetElement) {
                const headerOffset = document.querySelector('.navbar').offsetHeight; // Altura del navbar fijo
                const elementPosition = targetElement.getBoundingClientRect().top; // Posición del elemento relativa a la ventana
                const offsetPosition = elementPosition + window.scrollY - headerOffset; // Posición absoluta ajustada

                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth" // Desplazamiento suave
                });
            }
        });
    });

    // Add a class to navbar on scroll for a subtle change (e.g., solid background)
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) { // Si el usuario ha hecho scroll más de 50px
            navbar.classList.add('scrolled'); // Añade la clase 'scrolled'
        } else {
            navbar.classList.remove('scrolled'); // Remueve la clase 'scrolled'
        }
    });

    // FAQ Accordion Functionality
    const accordionHeaders = document.querySelectorAll('.accordion-header');

    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const currentItem = header.parentElement; // El .accordion-item
            const content = header.nextElementSibling; // El .accordion-content

            // Cierra todos los demás ítems del acordeón (opcional, si solo quieres uno abierto a la vez)
            accordionHeaders.forEach(otherHeader => {
                const otherItem = otherHeader.parentElement;
                const otherContent = otherHeader.nextElementSibling;

                if (otherItem !== currentItem && otherHeader.classList.contains('active')) {
                    otherHeader.classList.remove('active');
                    otherContent.style.maxHeight = 0;
                    otherContent.style.paddingTop = '0';
                    otherContent.style.paddingBottom = '0';
                }
            });

            // Abre o cierra el ítem clickeado
            header.classList.toggle('active');
            if (header.classList.contains('active')) {
                // Calcula el scrollHeight de los elementos internos para el max-height
                // Esto es importante para que el max-height se ajuste dinámicamente al contenido
                content.style.maxHeight = content.scrollHeight + 'px';
                content.style.paddingTop = '15px';
                content.style.paddingBottom = '15px';
            } else {
                content.style.maxHeight = 0;
                content.style.paddingTop = '0';
                content.style.paddingBottom = '0';
            }
        });
    });

    // Animation on scroll for elements (using Intersection Observer)
    const fadeElements = document.querySelectorAll(
        '.hero-content, .hero-graphic, .metrics-section h2, .metric-card, ' +
        '.main-content-section .section-header, .image-container, .content-item, ' +
        '.info-section h2, .info-card, .faq-accordion, .cta-content'
    );

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target); // Dejar de observar una vez que el elemento ha aparecido
            }
        });
    }, {
        threshold: 0.1 // Activar cuando el 10% del elemento es visible
    });

    fadeElements.forEach(element => {
        element.classList.add('fade-in-on-scroll'); // Añadir clase inicial para los estilos de transición
        observer.observe(element);
    });
});