from fpdf import FPDF
import os

# --- CLASE PERSONALIZADA para el PDF con encabezado y pie de página ---
class PDF(FPDF):
    def header(self):
        # Logo (opcional, si tienes un logo para el PDF)
        # self.image('ruta/a/tu/logo.png', 10, 8, 33)
        
        # Título del encabezado
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 102, 204) # Azul fuerte
        self.cell(0, 10, 'Campaña de Concientización sobre el Dengue', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15) # Posición a 1.5 cm de la parte inferior
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150, 150, 150) # Gris
        # Número de página
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body_text):
        self.set_font('Times', '', 12)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, body_text)
        self.ln(6)

    def add_image_section(self, image_path, title, description=None):
        self.add_page()
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, title, 0, 1, "C")
        self.ln(5)

        if os.path.exists(image_path):
            try:
                # Calcular las dimensiones para que la imagen quepa bien en la página
                page_width = self.w - 2 * self.l_margin
                img_width, img_height = self.get_image_size(image_path)
                
                # Ajustar la imagen si es muy ancha
                if img_width > page_width:
                    scale_factor = page_width / img_width
                    img_width = page_width
                    img_height = img_height * scale_factor
                
                # Asegurarse de que la imagen no se salga de la página verticalmente
                # Considerar espacio para el pie de página
                if self.get_y() + img_height > self.h - self.b_margin - 10: # 10 es un buffer
                    self.add_page() # Si no cabe, ir a una nueva página

                self.image(image_path, x=self.l_margin, y=self.get_y(), w=img_width)
                self.ln(img_height + 5) # Salto de línea después de la imagen
                if description:
                    self.set_font("Arial", "I", 10)
                    self.set_text_color(50, 50, 50)
                    self.multi_cell(0, 5, description, 0, 'C')
                    self.ln(5)
            except Exception as e:
                self.set_font("Arial", "", 10)
                self.set_text_color(255, 0, 0)
                self.multi_cell(0, 5, f"Error al cargar la imagen: {image_path}. {e}", 0, 'C')
                self.ln(5)
        else:
            self.set_font("Arial", "", 10)
            self.set_text_color(255, 0, 0)
            self.multi_cell(0, 5, f"ERROR: Imagen no encontrada en: {image_path}", 0, 'C')
            self.ln(5)

# --- Funciones para generar los PDFs ---

def get_image_path(image_name):
    """Ayudante para construir la ruta correcta a las imágenes."""
    script_dir = os.path.dirname(__file__)
    # La ruta desde generate_pdfs.py (en scripts_generacion_contenido)
    # hasta img/ (en dengue-awareness-site)
    return os.path.join(script_dir, '..', 'dengue-awareness-site', 'img', image_name)

def generate_comprehensive_dengue_pdf(filename="dengue_completo.pdf"):
    """
    Genera un PDF completo con información detallada sobre el dengue,
    incluyendo infografías.
    """
    pdf = PDF()
    pdf.alias_nb_pages() # Permite {{nb}} en el pie de página
    pdf.add_page()

    # --- Portada ---
    pdf.set_font("Arial", "B", 24)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 20, "Guía Integral sobre el Dengue", 0, 1, "C")
    pdf.set_font("Arial", "", 16)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, "Conoce, Previene y Protege tu Salud", 0, 1, "C")
    pdf.ln(30)
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, "Generado por DipoleDengue Awareness Site", 0, 1, "C")
    pdf.ln(80) # Espacio para el centro de la página
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Fecha de generación: {os.environ.get('DATE_GENERATED', '20/06/2025')}", 0, 1, "C") # Usar variable de entorno si existe
    pdf.add_page() # Pasamos a la siguiente página para el contenido


    # --- 1. ¿Qué es el Dengue? ---
    pdf.chapter_title("1. ¿Qué es el Dengue?")
    pdf.chapter_body(
        "El dengue es una enfermedad viral aguda transmitida por la picadura de mosquitos hembra infectados, principalmente de la especie Aedes aegypti y, en menor medida, Aedes albopictus. Es una enfermedad endémica en más de 100 países de regiones tropicales y subtropicales, incluyendo gran parte de México y América Latina.\n\n"
        "Existen cuatro serotipos diferentes del virus del dengue (DENV-1, DENV-2, DENV-3 y DENV-4). La infección por un serotipo confiere inmunidad permanente contra ese serotipo específico, pero no contra los otros. Una infección posterior con un serotipo diferente (infección secundaria) aumenta significativamente el riesgo de desarrollar formas más graves de la enfermedad, como el dengue grave (anteriormente conocido como dengue hemorrágico)."
    )
    pdf.ln(5)

    # --- 2. Transmisión del Dengue ---
    pdf.chapter_title("2. Transmisión del Dengue")
    pdf.chapter_body(
        "La transmisión del dengue es un ciclo complejo que involucra al mosquito Aedes aegypti y a los seres humanos. No se transmite directamente de persona a persona. El ciclo funciona así:\n"
        "1.  Un mosquito Aedes aegypti (sano) pica a una persona que ya está infectada con el virus del dengue.\n"
        "2.  El mosquito se infecta con el virus y, después de un período de incubación extrínseca (generalmente 8-12 días), se vuelve infeccioso.\n"
        "3.  Este mosquito infectado puede luego picar a personas sanas, transmitiéndoles el virus.\n"
        "Es importante destacar que el mosquito Aedes aegypti es diurno, lo que significa que pica principalmente durante el día, especialmente al amanecer y al anochecer. Se reproduce en depósitos de agua limpia."
    )
    pdf.ln(5)

    # --- 3. Síntomas y Fases de la Enfermedad ---
    pdf.chapter_title("3. Síntomas y Fases de la Enfermedad")
    pdf.chapter_body(
        "El dengue puede manifestarse con una amplia gama de síntomas, desde casos asintomáticos hasta formas graves y potencialmente mortales. La enfermedad se divide típicamente en tres fases:\n\n"
        "A.  Fase Febril (Días 1-7):\n"
        "    - Fiebre alta súbita (40°C/104°F).\n"
        "    - Dolor de cabeza intenso (especialmente detrás de los ojos).\n"
        "    - Dolores musculares y articulares severos (a menudo llamado 'fiebre quebrantahuesos').\n"
        "    - Náuseas y vómitos.\n"
        "    - Erupciones cutáneas (rash) que pueden aparecer entre el día 3 y 6.\n"
        "    - Fatiga y debilidad general."
    )
    pdf.chapter_body(
        "B.  Fase Crítica (Días 3-7, coincide con la caída de la fiebre):\n"
        "    Esta fase es crucial y solo se presenta en algunos casos. Es cuando el paciente puede empeorar rápidamente, incluso si la fiebre disminuye. Los signos de alarma que requieren atención médica URGENTE incluyen:\n"
        "    - Dolor abdominal intenso y continuo.\n"
        "    - Vómitos persistentes (más de 3 en 6 horas).\n"
        "    - Acumulación de líquidos (ascitis, derrame pleural, edema).\n"
        "    - Sangrado de encías, nariz, o aparición de pequeños puntos rojos en la piel (petequias).\n"
        "    - Letargo, irritabilidad o inquietud.\n"
        "    - Hipotensión postural (mareo al ponerse de pie).\n"
        "    - Aumento del tamaño del hígado (hepatomegalia).\n"
        "    - Disminución rápida de plaquetas."
    )
    pdf.chapter_body(
        "C.  Fase de Recuperación (Días 7-10):\n"
        "    La mayoría de los pacientes que sobreviven a la fase crítica o que solo experimentaron la fase febril comienzan a mejorar. Se caracteriza por:\n"
        "    - Reabsorción gradual de líquidos.\n"
        "    - Estabilización del estado hemodinámico.\n"
        "    - Recuperación del apetito.\n"
        "    - En algunos casos, puede haber una erupción cutánea tardía que pica."
    )
    pdf.ln(5)
    pdf.add_image_section(get_image_path('infografia_sintomas.png'), "Infografía: Reconoce los Síntomas del Dengue", "Una guía visual rápida para identificar los signos de alerta del dengue.")
    pdf.ln(5)

    # --- 4. Prevención del Dengue ---
    pdf.chapter_title("4. Prevención del Dengue: ¡Es Tarea de Todos!")
    pdf.chapter_body(
        "Dado que no existe un tratamiento antiviral específico para el dengue y la prevención de las picaduras de mosquitos es fundamental. La clave radica en eliminar los criaderos de mosquitos Aedes aegypti. Sigue estas recomendaciones:\n\n"
        "1.  Elimina Criaderos:\n"
        "    Vacía, limpia y voltea cualquier recipiente que pueda acumular agua: cubetas, llantas, botellas, macetas, floreros, platos de mascotas. Haz esto al menos una vez por semana.\n"
        "2.  Lava y Tapa:\n"
        "    Lava con cepillo y jabón los bebederos de animales, piletas y cualquier contenedor de agua. Tapa herméticamente tinacos, cisternas y barriles de almacenamiento de agua.\n"
        "3.  Protege tu Hogar:\n"
        "    Instala mosquiteros en puertas y ventanas en buen estado. Utiliza repelentes de insectos de forma segura, siguiendo las instrucciones del fabricante, especialmente al amanecer y anochecer.\n"
        "4.  Ropa Protectora:\n"
        "    Siempre que sea posible, usa ropa de manga larga y pantalones, especialmente en áreas con alta presencia de mosquitos.\n"
        "5.  Participa:\n"
        "    Colabora con las campañas de salud pública para fumigación y descacharrización en tu comunidad."
    )
    pdf.ln(5)
    pdf.add_image_section(get_image_path('infografia_prevencion.png'), "Infografía: Estrategias Clave de Prevención", "Métodos efectivos para evitar la proliferación del mosquito transmisor del dengue.")
    pdf.ln(5)


    # --- 5. Mitos y Realidades del Dengue ---
    pdf.chapter_title("5. Mitos y Realidades del Dengue")
    pdf.chapter_body(
        "Existen muchos mitos alrededor del dengue que pueden dificultar su prevención y manejo. Es importante desmentirlos:\n\n"
        "MITO: El dengue se contagia de persona a persona.\n"
        "REALIDAD: Falso. El dengue solo se transmite a través de la picadura de un mosquito *Aedes aegypti* infectado.\n\n"
        "MITO: Si ya tuve dengue, no puedo volver a enfermarme.\n"
        "REALIDAD: Falso. Te vuelves inmune al serotipo que te infectó, pero puedes contraer los otros tres serotipos. De hecho, una segunda infección puede ser más grave.\n\n"
        "MITO: El mosquito *Aedes aegypti* solo pica de noche.\n"
        "REALIDAD: Falso. Este mosquito es de hábitos diurnos, pica principalmente al amanecer y al anochecer, aunque puede hacerlo en cualquier momento del día.\n\n"
        "MITO: La fumigación es la única solución contra el dengue.\n"
        "REALIDAD: Falso. La fumigación solo mata mosquitos adultos, pero no sus huevos ni larvas. La medida más efectiva es la eliminación constante de criaderos."
    )
    pdf.ln(5)
    pdf.add_image_section(get_image_path('infografia_mitos.png'), "Infografía: Desmintiendo Mitos sobre el Dengue", "Aclarando las confusiones comunes para una prevención más efectiva.")
    pdf.ln(5)

    # --- Criaderos Comunes ---
    pdf.chapter_title("6. Identifica y Elimina Criaderos Comunes")
    pdf.chapter_body(
        "Cualquier objeto que pueda acumular una pequeña cantidad de agua limpia es un potencial criadero del mosquito Aedes aegypti. Los más comunes incluyen:\n\n"
        "- **Llantas:** Acumulan agua de lluvia y son difíciles de secar.\n"
        "- **Cubetas y recipientes sin tapar:** Ya sean para almacenar agua o simplemente dejados al aire libre.\n"
        "- **Floreros y platos de macetas:** El agua estancada es ideal para las larvas.\n"
        "- **Bebederos de animales:** Deben lavarse y cambiarse el agua diariamente.\n"
        "- **Cisternas, tinacos y barriles:** Si no están bien tapados o tienen filtraciones.\n"
        "- **Botellas, latas y envases desechables:** Incluso una pequeña cantidad de agua es suficiente.\n"
        "- **Objetos en desuso:** Juguetes, adornos, etc., que puedan recoger agua."
    )
    pdf.ln(5)
    pdf.add_image_section(get_image_path('infografia_criaderos.png'), "Infografía: Criaderos Comunes del Mosquito", "Conoce dónde se reproduce el Aedes aegypti y cómo eliminarlo.")
    pdf.ln(5)

    # --- Llamada a la Acción Final ---
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 15, "¡Tu Participación es Clave!", 0, 1, "C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, 
        "La lucha contra el dengue es una responsabilidad compartida. Cada acción que tomes para eliminar criaderos, protegerte y difundir información, contribuye a la salud de tu comunidad.\n\n"
        "Si presentas síntomas de dengue, acude inmediatamente a tu centro de salud más cercano. No te automediques."
    )
    pdf.ln(10)
    pdf.set_font("Arial", "U", 12)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "Más recursos en: https://www.paho.org/es/temas/dengue", 0, 1, "C", link="https://www.gob.mx/salud/documentos/dengue")


    pdf.output(filename)
    print(f"PDF '{filename}' generado exitosamente en: {os.path.abspath(filename)}")


def generate_brief_dengue_pdf(filename="dengue_resumen.pdf"):
    """
    Genera un PDF conciso con la información esencial sobre el dengue.
    """
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Título
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "Dengue: Lo Esencial que Debes Saber", 0, 1, "C")
    pdf.ln(10)

    # ¿Qué es?
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, "1. ¿Qué es el Dengue?", 0, 1, "L")
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 6, "Enfermedad viral transmitida por la picadura del mosquito Aedes aegypti. No se contagia de persona a persona.")
    pdf.ln(5)

    # Síntomas Clave
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "2. Síntomas Comunes:", 0, 1, "L")
    pdf.set_font("Arial", "", 12)
    symptoms = [
        "- Fiebre alta súbita",
        "- Dolor de cabeza y detrás de los ojos",
        "- Dolores musculares y articulares",
        "- Náuseas y/o vómitos",
        "- Erupciones cutáneas"
    ]
    for s in symptoms:
        pdf.multi_cell(0, 6, s)
    pdf.ln(5)

    # Signos de Alarma
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(255, 0, 0) # Rojo para alerta
    pdf.cell(0, 8, "3. ¡Atención! Signos de Alarma (Busca ayuda médica URGENTE):", 0, 1, "L")
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    alarms = [
        "- Dolor abdominal intenso y continuo",
        "- Vómitos persistentes (más de 3 en 6 horas)",
        "- Sangrado de encías, nariz o puntos rojos en la piel",
        "- Cansancio extremo o irritabilidad",
        "- Dificultad para respirar"
    ]
    for a in alarms:
        pdf.multi_cell(0, 6, a)
    pdf.ln(5)

    # Prevención
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 8, "4. ¿Cómo Prevenir el Dengue?", 0, 1, "L")
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    prevention_brief = [
        "Lava: Cepilla y limpia recipientes que acumulen agua.",
        "Tapa: Cubre herméticamente tinacos, cubetas y cisternas.",
        "Voltea: Pon boca abajo baldes, cubetas, o cualquier objeto que pueda almacenar agua.",
        "Elimina: Desecha basura, llantas viejas y objetos en desuso que puedan ser criaderos."
    ]
    for p in prevention_brief:
        pdf.multi_cell(0, 6, p)
    pdf.ln(5)
    
    # Añadir infografía de prevención si existe
    pdf.add_image_section(get_image_path('infografia_prevencion.png'), "Infografía: Prevención en 4 Pasos", "Un recordatorio visual de las acciones clave.")

    # Llamada a la Acción
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 8, "¡Tu Ayuda es Vital!", 0, 1, "C")
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, "Mantén tu entorno limpio y sin agua estancada. Si tienes síntomas, acude al médico de inmediato.")
    pdf.ln(5)
    pdf.set_font("Arial", "U", 12)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "Más información: https://www.gob.mx/salud/acciones-y-programas/dengue", 0, 1, "C", link="https://www.gob.mx/salud/acciones-y-programas/dengue")

    pdf.output(filename)
    print(f"PDF '{filename}' generado exitosamente en: {os.path.abspath(filename)}")


if __name__ == "__main__":
    # Generar ambos PDFs
    generate_comprehensive_dengue_pdf()
    generate_brief_dengue_pdf()
    print("\nAmbos PDFs han sido generados.")