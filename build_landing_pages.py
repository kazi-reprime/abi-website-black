#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ABI landing page generator — one template, 17 pages (EN/ES, multi-location).
Run: python3 build.py   → writes pages next to this script.
"""
import os, json, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.abi.edu"

# ── Next class date: first Monday of the upcoming month (computed at build) ──
def _next_first_monday():
    today = datetime.date.today()
    d = datetime.date(today.year, today.month, 1)
    while d.weekday() != 0:
        d += datetime.timedelta(days=1)
    if d <= today:
        y, m = (today.year, today.month + 1) if today.month < 12 else (today.year + 1, 1)
        d = datetime.date(y, m, 1)
        while d.weekday() != 0:
            d += datetime.timedelta(days=1)
    return d

NEXT_MON = _next_first_monday()
NEXT_START_EN = NEXT_MON.strftime("%a, %b ") + str(NEXT_MON.day)          # e.g. "Mon, Jul 6"
_ES_MO = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
NEXT_START_ES = "lun, %s %d" % (_ES_MO[NEXT_MON.month - 1], NEXT_MON.day)  # e.g. "lun, jul 6"

# ───────────────────────── icons ─────────────────────────
def icon(name, size=22):
    P = {
        "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.08 4.18 2 2 0 0 1 4.06 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.22a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
        "badge": '<circle cx="12" cy="9" r="6"/><path d="M9 14.5 7.5 22l4.5-2.5L16.5 22 15 14.5"/><path d="m10 9 1.5 1.5L14.5 7"/>',
        "cal": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01"/>',
        "mic": '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10v1a7 7 0 0 0 14 0v-1M12 18v4M8 22h8"/>',
        "hand": '<circle cx="12" cy="6" r="3.4"/><path d="M12 4.6v2.8M10.9 5.4h2.2"/><path d="M3 15.5c2-1.6 4-1.6 5.6-.6l3 1.8c.9.6.9 1.9-.2 2.2H8M11.4 18.9l5.2.1c2 0 3.4-.9 4.4-2.3"/>',
        "case": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2M2 13h20"/>',
        "bldg": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 21v-4h6v4M8 7h2M14 7h2M8 11h2M14 11h2"/>',
        "shield": '<path d="M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10z"/><path d="m9 11.5 2 2 4-4.5"/>',
        "people": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><circle cx="17" cy="9" r="2.4"/><path d="M16.5 14.7c2.6.3 4.5 2.2 4.5 4.8"/>',
        "star": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1L12 2z"/>',
        "cert": '<rect x="3" y="3" width="14" height="18" rx="2"/><path d="M7 8h6M7 12h6M7 16h3"/><circle cx="17.5" cy="16.5" r="3"/><path d="m16 19 -.5 3 2-1 2 1-.5-3"/>',
        "user": '<circle cx="12" cy="8.5" r="3.5"/><path d="M5 20c0-3.6 3.1-6 7-6s7 2.4 7 6"/>',
        "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 7L22 7"/>',
        "pin": '<path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/>',
        "check": '<circle cx="12" cy="12" r="10"/><path d="m8 12.2 2.6 2.6L16 9.5"/>',
        "chat": '<path d="M21 12a8.5 8.5 0 0 1-8.5 8.5c-1.6 0-3-.4-4.3-1L3 21l1.6-4.8A8.5 8.5 0 1 1 21 12z"/>',
        "chev": '<path d="m6 9 6 6 6-6"/>',
        "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
        "train": '<rect x="5" y="3" width="14" height="14" rx="3"/><path d="M5 11h14M9.5 17 7 21M14.5 17 17 21M9 14h.01M15 14h.01"/>',
    }
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
            % (size, size, P[name]))

# ───────────────────────── shared strings ─────────────────────────
S = {
 "en": {
  "topbar": "Start your barber journey today for only $150 per week*",
  "limited": "Limited Seats — Enrollment Open", "reserve": "Reserve Your Spot Today",
  "next_start": "Next Start:", "call": "Request a Call",
  "form_sub": "Fill out the form and an Admissions Advisor will contact you.",
  "fn": "First Name", "ln": "Last Name", "ph": "Phone", "em": "Email",
  "q_loc": "Which School Location Would You Prefer To Attend?",
  "q_fmt": "What is your Preferred Learning Format?",
  "opt_loc": "Select a location", "opt_fmt": "Select an option",
  "locs": ["Manhattan Campus — 48 West 39th Street", "Bronx Campus — 121 Westchester Square"],
  "fmts": ["Morning · Mon–Fri 8:00 AM–2:00 PM", "Afternoon · Mon–Fri 2:00 PM–8:00 PM", "Weekend · Sat–Sun 9:00 AM–7:00 PM"],
  "submit": "Submit",
  "consent": "By clicking “submit” you consent that ABI can contact you via phone, SMS or email for booking confirmations or promotional offers.",
  "success_h": "Thank you!", "success_p": "An ABI admissions agent will call you within 24 hours.",
  "form_err": "Something went wrong. Please try again or call us at",
  "trust": [("shield","30+ Years of Excellence Training Future Barbers"),
            ("people","Thousands of Successful Graduates"),
            ("star","Top-Rated Barber School in New York"),
            ("cert","Approved by NYSED · Licensed by BPSS")],
  "features": [("badge","Licensed by NYSED (BPSS)"),("cal","Day, evening, weekend schedules"),
               ("mic","Hands-on training in our professional Barber clinic"),
               ("hand","Financial assistance ACCES-VR, VA & more"),
               ("case","Career support · Job placement assistance"),
               ("bldg","Modern campus in the heart of New York City and Bronx")],
  "about_eb": "Overview", "tech_eb": "Techniques", "tech_h": "Skills & Techniques You'll Master",
  "curr_eb": "Curriculum", "curr_h": "Course Modules",
  "tuition_eb": "Tuition", "tuition_h": "Flexible Payment Plans",
  "tuition_lead": "Every plan includes NY State Board Exam prep, hands-on training and job placement support. Pay weekly while you attend.",
  "plans": [
    {"name":"Plan A — Morning","sched":"Mon–Fri · 8:00 AM – 2:00 PM","hours":"30 hrs/week · 17 weeks (~4 months)",
     "price":"$5,600","terms":"$500 down (incl. $100 registration) + 17 weekly payments of $300","pop":False},
    {"name":"Plan B — Afternoon","sched":"Mon–Fri · 2:00 PM – 8:00 PM","hours":"30 hrs/week · 17 weeks (~4 months)",
     "price":"$4,600","terms":"$500 down (incl. $100 registration) + 16 weekly payments of $250 + final $100","pop":True},
    {"name":"Plan C — Weekend","sched":"Sat & Sun · 9:00 AM – 7:00 PM","hours":"18 hrs/week · 27 weeks (~6–7 months)",
     "price":"$4,600","terms":"$550 down (incl. $100 registration) + 27 weekly payments of $150","pop":False}],
  "pop_tag": "Most Popular", "plan_cta": "Let's Do It ✂",
  "plans_note": "Additional fees: books, tools and supplies can be purchased from ABI or other suppliers. ACCES-VR financial assistance available. Post-9/11 GI Bill® and VA benefits accepted.",
  "req_eb": "Admissions", "req_h": "Entrance Requirements",
  "reqs": ["Social Security Card","High School Diploma (HSD) or GED — or pass the ATB entrance exam at ABI",
           "Must be at least 17 years of age","Proof of residential address",
           "Valid photo ID or Driver's License","$500 down payment"],
  "testi_eb": "Student Stories", "testi_h": "What Our Students Say",
  "testi_sub": "Real reviews from our Google profile.",
  "testi": [
    {"q":"The level of knowledge and training is superb! One of the best teachers around, King David, will show you everything there is to know about barbering — 100% commitment from this school.","n":"Jerrick Matthews","r":"Current student"},
    {"q":"I'm a student here and King David has been awesome!! He has 30 years of experience, gives us great techniques and keeps polishing our basic skills.","n":"Carlos Perez","r":"Student"},
    {"q":"Passed by the barber school for only 3 dollars for a regular haircut — and it's actually good! Great that we could help student trainees practice toward their 500 hours.","n":"Vincybie Lee","r":"Haircut client"},
    {"q":"Donovan gave me a great haircut. He did exactly what I asked him to do… Well worth $3 plus a $7 tip. $10 for a haircut!!!","n":"Tina Banee","r":"Haircut client"},
    {"q":"I'm currently enrolled here and I'm happy with the progress from learning from the teachers and classmates. Nothing but positivity and eager to learn more in this field.","n":"Zyee Fin","r":"Current student"}],
  "closing_h": "Ready to Start Your Barbering Career?",
  "closing_p": "New classes begin the first Monday of every month. Seats fill fast — call us or reserve your spot today, in English or Spanish.",
  "closing_cta": "Reserve Your Spot", "closing_call": "Call",
  "mbar_call": "Call Now", "mbar_cta": "Become a Barber",
  "bubble_tip": "Hey, I'm one of the assistants at ABI. How can I help?",
  "exit_h": "Wait — your chair is waiting",
  "exit_p": "Classes start the first Monday of every month and seats are limited. Leave your info and an admissions advisor will call you within 24 hours.",
  "exit_cta": "Reserve My Spot",
  "f_about": "New York's only dedicated barber school — changing lives for over 30 years. Licensed by the New York State Department of Education. Est. 1996.",
  "f_visit": "Visit Us", "f_links": "Quick Links",
  "f_linkitems": [("Programs","/programs/index.html"),("Admissions","/admissions.html"),
                  ("Veterans · GI Bill®","/veterans.html"),("Admissions","/admissions.html"),
                  ("$3 Haircuts","/haircuts.html"),("Contact","/contact.html")],
  "gibill": "GI BILL® is a registered trademark of the U.S. Department of Veterans Affairs (VA).",
  "details_h": "Program Details", "d_dur": "Duration", "d_tui": "Tuition", "d_from": "from", "d_sch": "Schedules",
  "d_sch_v": "Morning · Afternoon · Weekend",
  "count_h": "Next class starts in", "count_lbl": ["Days","Hours","Min","Sec"],
  "en_es_phones": [("English","(212) 290-2289","+12122902289"),("Spanish","(212) 290-0278","+12122900278")],
 },
 "es": {
  "topbar": "Comienza tu carrera de barbero hoy por solo $150 por semana*",
  "limited": "Cupos Limitados — Inscripción Abierta", "reserve": "Reserva Tu Lugar Hoy",
  "next_start": "Próximo Inicio:", "call": "Solicitar Llamada",
  "form_sub": "Completa el formulario y un asesor de admisiones te contactará.",
  "fn": "Nombre", "ln": "Apellido", "ph": "Teléfono", "em": "Correo Electrónico",
  "q_loc": "¿A cuál sede te gustaría asistir?",
  "q_fmt": "¿Cuál es tu horario preferido?",
  "opt_loc": "Selecciona una sede", "opt_fmt": "Selecciona una opción",
  "locs": ["Sede de Manhattan — 48 West 39th Street", "Sede del Bronx — 121 Westchester Square"],
  "fmts": ["Mañanas · Lun–Vie 8:00 AM–2:00 PM", "Tardes · Lun–Vie 2:00 PM–8:00 PM", "Fines de Semana · Sáb–Dom 9:00 AM–7:00 PM"],
  "submit": "Enviar",
  "consent": "Al hacer clic en “enviar” aceptas que ABI pueda contactarte por teléfono, SMS o correo electrónico para confirmaciones de citas u ofertas promocionales.",
  "success_h": "¡Gracias!", "success_p": "Un agente de admisiones de ABI te llamará dentro de 24 horas.",
  "form_err": "Algo salió mal. Inténtalo de nuevo o llámanos al",
  "trust": [("shield","Más de 30 Años de Excelencia Formando Barberos"),
            ("people","Miles de Graduados Exitosos"),
            ("star","Escuela de Barbería Mejor Calificada de Nueva York"),
            ("cert","Aprobada por NYSED · Licenciada por BPSS")],
  "features": [("badge","Licenciada por NYSED (BPSS)"),("cal","Horarios de día, tarde y fin de semana"),
               ("mic","Entrenamiento práctico en nuestra clínica profesional de barbería"),
               ("hand","Asistencia financiera ACCES-VR, VA y más"),
               ("case","Apoyo profesional · Asistencia de empleo"),
               ("bldg","Campus moderno en el corazón de Nueva York y el Bronx")],
  "about_eb": "Resumen", "tech_eb": "Técnicas", "tech_h": "Habilidades y Técnicas Que Dominarás",
  "curr_eb": "Plan de Estudios", "curr_h": "Módulos del Curso",
  "tuition_eb": "Matrícula", "tuition_h": "Planes de Pago Flexibles",
  "tuition_lead": "Todos los planes incluyen preparación para el examen del Estado de NY, entrenamiento práctico y apoyo para la colocación laboral. Paga semanalmente mientras estudias.",
  "plans": [
    {"name":"Plan A — Mañanas","sched":"Lun–Vie · 8:00 AM – 2:00 PM","hours":"30 hrs/semana · 17 semanas (~4 meses)",
     "price":"$5,600","terms":"$500 de pago inicial (incluye $100 de inscripción) + 17 pagos semanales de $300","pop":False},
    {"name":"Plan B — Tardes","sched":"Lun–Vie · 2:00 PM – 8:00 PM","hours":"30 hrs/semana · 17 semanas (~4 meses)",
     "price":"$4,600","terms":"$500 de pago inicial (incluye $100 de inscripción) + 16 pagos semanales de $250 + pago final de $100","pop":True},
    {"name":"Plan C — Fines de Semana","sched":"Sáb y Dom · 9:00 AM – 7:00 PM","hours":"18 hrs/semana · 27 semanas (~6–7 meses)",
     "price":"$4,600","terms":"$550 de pago inicial (incluye $100 de inscripción) + 27 pagos semanales de $150","pop":False}],
  "pop_tag": "Más Popular", "plan_cta": "¡Hagámoslo! ✂",
  "plans_note": "Tarifas adicionales: libros, herramientas y suministros se pueden comprar en ABI o con otros proveedores. Asistencia financiera ACCES-VR disponible. Beneficios de Post-9/11 GI Bill® y VA aceptados.",
  "req_eb": "Admisiones", "req_h": "Requisitos de Admisión",
  "reqs": ["Tarjeta de Seguro Social","Diploma de Preparatoria (HSD) o GED — o aprobar el examen ATB de admisión en ABI",
           "Tener al menos 17 años de edad","Comprobante de domicilio",
           "Identificación con foto válida o licencia de conducir","Pago inicial de $500"],
  "testi_eb": "Historias de Estudiantes", "testi_h": "Lo Que Dicen Nuestros Estudiantes",
  "testi_sub": "Reseñas reales de nuestro perfil de Google.",
  "testi": [
    {"q":"¡El nivel de conocimiento y entrenamiento es excelente! Uno de los mejores maestros, King David, te enseña todo lo que hay que saber sobre barbería — 100% de compromiso de esta escuela.","n":"Jerrick Matthews","r":"Estudiante actual"},
    {"q":"Soy estudiante aquí y ¡King David ha sido increíble! Tiene 30 años de experiencia, nos da grandes técnicas y sigue puliendo nuestras habilidades básicas.","n":"Carlos Perez","r":"Estudiante"},
    {"q":"Pasé por la escuela de barbería: solo $3 por un corte regular — ¡y de verdad está bueno! Genial poder ayudar a los estudiantes a practicar para sus 500 horas.","n":"Vincybie Lee","r":"Cliente de corte"},
    {"q":"Donovan me dio un gran corte. Hizo exactamente lo que le pedí… Bien vale los $3 más $7 de propina. ¡¡$10 por un corte!!","n":"Tina Banee","r":"Cliente de corte"},
    {"q":"Estoy inscrito aquí y estoy feliz con el progreso aprendiendo de los maestros y compañeros. Pura positividad y ganas de aprender más en este campo.","n":"Zyee Fin","r":"Estudiante actual"}],
  "closing_h": "¿Listo para Empezar Tu Carrera de Barbería?",
  "closing_p": "Las clases nuevas comienzan el primer lunes de cada mes. Los cupos se llenan rápido — llámanos o reserva tu lugar hoy.",
  "closing_cta": "Reserva Tu Lugar", "closing_call": "Llámanos",
  "mbar_call": "Llámanos", "mbar_cta": "Conviértete en Barbero",
  "bubble_tip": "Hola, soy uno de los asistentes de ABI. ¿Cómo puedo ayudarte?",
  "exit_h": "Espera — tu silla te está esperando",
  "exit_p": "Las clases comienzan el primer lunes de cada mes y los cupos son limitados. Déjanos tu información y un asesor de admisiones te llamará dentro de 24 horas.",
  "exit_cta": "Reservar Mi Lugar",
  "f_about": "La única escuela de barbería dedicada de Nueva York — cambiando vidas por más de 30 años. Licenciada por el Departamento de Educación del Estado de NY. Est. 1996.",
  "f_visit": "Visítanos", "f_links": "Enlaces Rápidos",
  "f_linkitems": [("Programas","/programs/index.html"),("Admisiones","/admissions.html"),
                  ("Veteranos · GI Bill®","/veterans.html"),("Admisiones","/admissions.html"),
                  ("Cortes de $3","/haircuts.html"),("Contacto","/contact.html")],
  "gibill": "GI BILL® es una marca registrada del Departamento de Asuntos de Veteranos de EE. UU. (VA).",
  "details_h": "Detalles del Programa", "d_dur": "Duración", "d_tui": "Matrícula", "d_from": "desde", "d_sch": "Horarios",
  "d_sch_v": "Mañanas · Tardes · Fines de Semana",
  "count_h": "La próxima clase comienza en", "count_lbl": ["Días","Horas","Min","Seg"],
  "en_es_phones": [("English","(212) 290-2289","+12122902289"),("Español","(212) 290-0278","+12122900278")],
 },
}

MANHATTAN = {"name_en":"Manhattan Campus","name_es":"Sede de Manhattan",
             "addr":"48 West 39th Street, New York, NY 10018","tel_disp":"(212) 290-2289","tel":"+12122902289"}
BRONX = {"name_en":"Bronx Campus","name_es":"Sede del Bronx",
         "addr":"121 Westchester Square, Bronx, NY 10461","tel_disp":"(718) 676-0640","tel":"+17186760640"}

# ───────────────────────── page data ─────────────────────────
CURR_MAN_EN = [
 ("Theory & Science",["Sanitation & Sterilization","Barber History","NY State Laws & Regulations","Shop Management","Professional Ethics"]),
 ("Cutting Techniques",["Fades (Low, Mid, High)","Tapers & Classic Cuts","Clipper Over Comb","Scissor Over Comb","Flat Tops & High-Top Fades"]),
 ("Styling & Finishing",["Razor Lineups & Shape Ups","Blowouts & Pompadours","Afro & Mohawk Styling","Beard Trimming & Design","Shampoo & Conditioning"]),
 ("Shaving & Skin Care",["Straight Razor Shaving","Facial Massage Techniques","Hot Towel Treatments","Skin & Scalp Analysis","Safety & Hygiene"]),
 ("Business & Career",["Client Consultation Skills","Barbershop Operation","Building a Clientele","Job Placement Prep","NY State Board Exam Prep"])]
CURR_MAN_ES = [
 ("Teoría y Ciencia",["Sanitización y Esterilización","Historia de la Barbería","Leyes y Regulaciones del Estado de NY","Administración de Barbería","Ética Profesional"]),
 ("Técnicas de Corte",["Fades (Bajos, Medios, Altos)","Tapers y Cortes Clásicos","Clipper Sobre Peine","Tijera Sobre Peine","Flat Tops y High-Top Fades"]),
 ("Estilizado y Acabado",["Líneas con Navaja y Shape Ups","Blowouts y Pompadours","Estilizado de Afro y Mohawk","Recortes y Diseño de Barba","Lavado y Acondicionamiento"]),
 ("Afeitado y Cuidado de la Piel",["Afeitado con Navaja","Técnicas de Masaje Facial","Tratamientos con Toallas Calientes","Análisis de Piel y Cuero Cabelludo","Seguridad e Higiene"]),
 ("Negocio y Carrera",["Habilidades de Consulta con el Cliente","Operación de Barbería","Construcción de Clientela","Preparación para Empleo","Preparación del Examen del Estado de NY"])]
CURR_BX_EN = [
 ("Theory & Science",["Sanitation & Sterilization","Infection Control","Anatomy & Chemistry","NY State Laws & Regulations","Professional Ethics"]),
 CURR_MAN_EN[1], CURR_MAN_EN[3], CURR_MAN_EN[4]]
CURR_BX_ES = [
 ("Teoría y Ciencia",["Sanitización y Esterilización","Control de Infecciones","Anatomía y Química","Leyes y Regulaciones del Estado de NY","Ética Profesional"]),
 CURR_MAN_ES[1], CURR_MAN_ES[3], CURR_MAN_ES[4]]

TECH_MAN_EN = ["Classic Tapers","Low Fades","Mid Fades","High Fades","High-Top Fades","Pompadours","Fohawks","Caesars","Bald Heads","Afros","Flat Tops","Razor Lineups","Classical Haircuts","Beard Trims","Shape Ups","Blowouts","Mohawks","Shampoos","Shaving Techniques","Facial Massage","Clipper Over Comb","Scissor Over Comb"]
TECH_MAN_ES = ["Degradados Clásicos","Fades Bajos","Fades Medios","Fades Altos","High-Top Fades","Pompadours","Mohawks","Caesars","Cabezas Rapadas","Afro","Flat Tops","Líneas con Navaja","Cortes Clásicos","Recortes de Barba","Shape Ups","Blowouts","Lavados","Técnicas de Afeitado","Masaje Facial","Clipper Sobre Peine","Tijera Sobre Peine"]
TECH_BX_EN = ["Shear Over Comb","Clipper Cutting","Razor Cutting","Point Cutting","Thinning Shears","Straight Razor Shaving","Beard Maintenance","Mustache & Beard Design","Classic Tapers","Low · Mid · High Fades","Pompadours","Caesars","Flat Tops","Razor Lineups","Shape Ups","Blowouts","Mohawks","Shaving Techniques","Facial Massage"]
TECH_BX_ES = ["Tijera Sobre Peine","Corte con Clipper","Corte con Navaja","Point Cutting","Tijeras de Entresacado","Afeitado con Navaja","Mantenimiento de Barba","Diseño de Bigote y Barba","Degradados Clásicos","Fades Bajos · Medios · Altos","Pompadours","Caesars","Flat Tops","Líneas con Navaja","Shape Ups","Blowouts","Mohawks","Técnicas de Afeitado","Masaje Facial"]

ABOUT_MAN_EN = [
 "Our Master Barber Program offers a comprehensive curriculum designed to prepare students for success in the thriving barbering industry. Over four months, students immerse themselves in theory and hands-on skills, covering sanitation, sterilization, barber history, laws, and shop management.",
 "Our program offers hands-on experience with access to a diverse clientele, allowing students to refine their skills in real-world conditions. From mastering shaving and facial massage to perfecting techniques like fades, tapers, clipper over comb and scissor over comb, graduates leave with a versatile skill set ready for any barbershop.",
 "Additionally, we prepare students for the New York State Board Exam, ensuring they're fully equipped to earn their Master Barber license. Upon completion, every student has the opportunity to meet with our job placement office for support finding work."]
ABOUT_MAN_ES = [
 "Nuestro Programa de Barbero Maestro ofrece un plan de estudios integral diseñado para preparar a los estudiantes para el éxito en la próspera industria de la barbería. Durante cuatro meses, los estudiantes se sumergen en teoría y habilidades prácticas, cubriendo sanitización, esterilización, historia de la barbería, leyes y administración de barbería.",
 "Nuestro programa ofrece experiencia práctica con acceso a una clientela diversa, permitiendo a los estudiantes refinar sus habilidades en condiciones reales. Desde dominar el afeitado y masaje facial hasta perfeccionar técnicas como fades, tapers, clipper sobre peine, tijera sobre peine y mucho más, los graduados se gradúan con un conjunto de habilidades versátil listo para emplearse en cualquier barbería.",
 "Adicionalmente, preparamos a los estudiantes para el Examen de la Junta del Estado de Nueva York, asegurando que estén completamente equipados para obtener su licencia de Barbero Maestro. Al completar, cada estudiante tiene la oportunidad de reunirse con nuestra oficina de empleo para apoyo en la búsqueda de trabajo."]
ABOUT_BX_EN = [
 "Welcome to the Bronx campus of the American Barber Institute, where we offer a comprehensive Master Barber Program that prepares students for success in the thriving barbering industry. Our 4-month full-time program covers everything you need to excel in this dynamic field, including safety regulations, infection control, anatomy, chemistry, and hair care techniques.",
 "Students learn and master the art of haircutting, shaving, facial massage and hairstyling. We also offer training in artificial hair and hair coloring procedures, including semi-permanent and temporary color, as well as techniques for working with wigs and hairpieces. Additionally, students gain proficiency in hair replacement methods.",
 "Hands-on experience is central to our program — students work with a diverse clientele to refine their skills in real-world conditions. Graduates leave with a versatile skill set, ready to work in any barbershop, mastering techniques like fades, tapers, clipper over comb and scissor over comb.",
 "We prepare students for the New York State Board Exam, ensuring they're fully equipped to earn their Master Barber license and launch their careers — whether the goal is a traditional shop, freelance work, or opening their own business."]
ABOUT_BX_ES = [
 "Bienvenido a la sede del Bronx del American Barber Institute, donde ofrecemos un Programa integral de Barbero Maestro que prepara a los estudiantes para el éxito en la próspera industria de la barbería. Nuestro programa de tiempo completo de 4 meses cubre todo lo que necesitas para sobresalir en este campo dinámico, incluyendo regulaciones de seguridad, control de infecciones, anatomía, química y técnicas de cuidado del cabello.",
 "Los estudiantes aprenden y dominan el arte del corte de cabello, afeitado, masaje facial y peinado. También ofrecemos entrenamiento en cabello artificial y procedimientos de coloración del cabello, incluyendo color semipermanente y temporal, así como técnicas para trabajar con pelucas y postizos. Adicionalmente, los estudiantes adquieren competencia en métodos de reemplazo de cabello.",
 "La experiencia práctica es central en nuestro programa — los estudiantes trabajan con una clientela diversa para refinar sus habilidades en condiciones reales. Los graduados se gradúan con un conjunto de habilidades versátil, listos para trabajar en cualquier barbería.",
 "Preparamos a los estudiantes para el Examen de la Junta del Estado de Nueva York, asegurando que estén completamente equipados para obtener su licencia de Barbero Maestro y lanzar sus carreras. Al completar, los estudiantes se conectan con nuestra oficina de empleo — ya sea su meta una barbería tradicional, trabajo independiente o abrir su propio negocio."]

LOCATIONS = []  # SEO location landing pages removed per client request (keep only Manhattan + Bronx campuses)
_LOCATIONS_ARCHIVED = [
 {"slug":"barber-school-queens-ny","loc":"Queens, NY","h1":"Barber School for Queens Residents","campus":MANHATTAN,
  "title":"Barber School for Queens, NY | American Barber Institute",
  "desc":"Train as a licensed Master Barber at NYC's only dedicated barber school — a quick train ride from Queens to Midtown Manhattan. 500-hour program, flexible schedules, payment plans. Next class starts soon.",
  "intro":["From Astoria and Long Island City to Jackson Heights, Flushing and Jamaica — Queens residents train for a real career behind the chair at one of New York City's only dedicated barber schools, just a quick ride away in Midtown Manhattan.",
           "Earn your NYS Master Barber license in as little as 4 months with hands-on training, real clients, and schedules built around Queens commuters."],
  "getting":"A quick E, F, M, R, or 7 train into Midtown drops you blocks from our Manhattan campus on West 39th Street; the LIRR into Penn Station works too."},
 {"slug":"barber-school-brooklyn-new-york","loc":"Brooklyn, NY","h1":"Barber School for Brooklyn, NY","campus":MANHATTAN,
  "title":"Barber School for Brooklyn, NY | American Barber Institute",
  "desc":"Become a licensed Master Barber — our Midtown Manhattan campus is 20–40 minutes from most of Brooklyn. 500-hour hands-on program, flexible schedules, weekly payment plans.",
  "intro":["From Williamsburg and Bushwick to Bed-Stuy, Flatbush, Bay Ridge and Coney Island — Brooklyn students train for a real career behind the chair at New York's only dedicated barber school.",
           "Most Brooklyn neighborhoods reach our campus in 20–40 minutes, and our morning, afternoon and weekend schedules fit work and family."],
  "getting":"Most Brooklyn neighborhoods reach our West 39th Street campus in 20–40 minutes on the B, D, N, Q, R or 2/3/4/5 trains."},
 {"slug":"barber-school-yonkers-new-york","loc":"Yonkers, NY","h1":"Barber School for Yonkers, NY","campus":BRONX,
  "title":"Barber School for Yonkers, NY | American Barber Institute",
  "desc":"Yonkers sits right on the Bronx border — our Westchester Square campus is one of the closest dedicated barber schools to you. Bilingual instruction, payment plans, NYS license prep.",
  "intro":["Yonkers sits right on the Bronx border, making our Bronx campus one of the closest dedicated barber schools to the city — from Getty Square to Park Hill, your new career is minutes away.",
           "Train hands-on with real clients, with bilingual instruction (se habla español) and flexible payment plans."],
  "getting":"A short drive down the Major Deegan or Saw Mill, or a Metro-North + local bus hop from downtown Yonkers."},
 {"slug":"barber-school-westchester-ny","loc":"Westchester, NY","h1":"Barber School for Westchester County","campus":BRONX,
  "title":"Barber School for Westchester, NY | American Barber Institute",
  "desc":"Westchester County residents: train as a licensed Master Barber at our Bronx campus — easy via Metro-North or I-95. Hands-on clinic, flexible schedules, weekly payment plans.",
  "intro":["From Mount Vernon and New Rochelle to White Plains — Westchester students earn their NYS Master Barber license at our Bronx campus, an easy trip via Metro-North or I-95.",
           "Our program puts clippers in your hands early with real clinic clients, so you graduate shop-ready."],
  "getting":"Via Metro-North (Harlem line) plus a short connection, or straight down I-95 / the Hutchinson River Parkway."},
 {"slug":"barber-school-long-island-ny","loc":"Long Island, NY","h1":"Barber School for Long Island, NY","campus":MANHATTAN,
  "title":"Barber School for Long Island, NY | American Barber Institute",
  "desc":"One LIRR ride from Nassau & Suffolk: our Manhattan campus is just blocks from Penn Station. 500-hour Master Barber program with weekend and afternoon schedules that suit the commute.",
  "intro":["Nassau and Suffolk students: our Manhattan campus is just blocks from Penn Station, making the LIRR commute straightforward.",
           "Weekend and afternoon schedules suit a commute from the Island — earn your NYS Master Barber license in as little as 4 months."],
  "getting":"Take the LIRR straight into Penn Station; our West 39th Street campus is a short walk away."},
 {"slug":"barber-school-mount-vernon-ny","loc":"Mount Vernon, NY","h1":"Barber School for Mount Vernon, NY","campus":BRONX,
  "title":"Barber School for Mount Vernon, NY | American Barber Institute",
  "desc":"Mount Vernon borders the Bronx — our Westchester Square campus is right around the corner. Train hands-on for the NYS Master Barber license with flexible payment plans.",
  "intro":["Mount Vernon borders the Bronx, so our Westchester Square campus is right around the corner — minutes from home, with a real-client clinic on the floor.",
           "Train mornings, afternoons or weekends, with bilingual instruction and weekly payment plans."],
  "getting":"Minutes away by car, or a short 2/5 train plus local bus from Mount Vernon."},
 {"slug":"barber-school-port-chester-ny","loc":"Port Chester, NY","h1":"Barber School for Port Chester, NY","campus":BRONX,
  "title":"Barber School for Port Chester, NY | American Barber Institute",
  "desc":"The closest dedicated barber school heading south from eastern Westchester — reach our Bronx campus via Metro-North or I-95 in 30–40 minutes. NYS license prep, payment plans.",
  "intro":["Heading south from eastern Westchester, ABI's Bronx campus is the closest dedicated barber school — roughly 30–40 minutes from Port Chester.",
           "Hands-on training with real clients, bilingual instructors, and schedules that work around your job."],
  "getting":"Via Metro-North (New Haven line) or straight down I-95 — roughly 30–40 minutes south."},
 {"slug":"barber-school-connecticut","loc":"Connecticut","h1":"Barber School for Connecticut Commuters","campus":BRONX,
  "title":"Barber School Near Connecticut | American Barber Institute",
  "desc":"Greenwich, Stamford, Norwalk: train just over the state line at our Bronx campus. Note: our program prepares you for the New York State Master Barber license.",
  "intro":["From Greenwich, Stamford and Norwalk — Fairfield County commuters train just over the state line at our Bronx campus, one of the closest dedicated barber schools to Connecticut.",
           "Earn the New York State Master Barber license with hands-on clinic training and weekly payment plans."],
  "getting":"Via Metro-North (New Haven line) into the Bronx, or down I-95 — Fairfield County is just over the state line.",
  "disclaimer":"Please note: American Barber Institute is licensed by the New York State Department of Education, and our program prepares you for the New York State Master Barber license. Connecticut residents are welcome to train here; check Connecticut's own licensing requirements if you intend to work in CT."},
 {"slug":"barber-school-pennsylvania","loc":"Pennsylvania","h1":"Barber School for Pennsylvania Students","campus":MANHATTAN,
  "title":"Barber School Near Pennsylvania | American Barber Institute",
  "desc":"Eastern PA students moving to or commuting into NYC: our Manhattan campus is a short walk from Penn Station. Prepares you for the New York State Master Barber license.",
  "intro":["For students in eastern Pennsylvania who are moving to or commuting into the New York City area, ABI's Manhattan campus is a short walk from Penn Station.",
           "Train hands-on for the New York State Master Barber license, with morning, afternoon and weekend schedules."],
  "getting":"A short walk from Penn Station for those arriving by train or bus into the city.",
  "disclaimer":"Please note: American Barber Institute is licensed by the New York State Department of Education, and our program prepares you for the New York State Master Barber license. If you plan to work in PA, check Pennsylvania's own barber licensing requirements."},
]


NAV = {
 "en": [("About","about.html"),("Instructors","instructors.html"),("Programs","programs/index.html"),
        ("Admissions","admissions.html"),("$3 Haircuts","haircuts.html"),("Jobs","jobs.html"),
        ("Gallery","gallery.html"),("FAQs","faq.html"),("Contact","contact.html")],
 "es": [("Nosotros","about.html"),("Instructores","instructors.html"),("Programas","programs/index.html"),
        ("Admisiones","admissions.html"),("Cortes de $3","haircuts.html"),("Empleos","jobs.html"),
        ("Galería","gallery.html"),("Preguntas","faq.html"),("Contacto","contact.html")],
}
NAV_LOC_LABEL = {"en": "Locations", "es": "Ubicaciones"}
LOC_NAMES = [("Queens","barber-school-queens-ny"),("Brooklyn","barber-school-brooklyn-new-york"),
 ("Yonkers","barber-school-yonkers-new-york"),("Westchester","barber-school-westchester-ny"),
 ("Long Island","barber-school-long-island-ny"),("Mount Vernon","barber-school-mount-vernon-ny"),
 ("Port Chester","barber-school-port-chester-ny"),("Connecticut","barber-school-connecticut"),
 ("Pennsylvania","barber-school-pennsylvania")]

LOC_ES = {
 "barber-school-queens-ny": {"loc":"Queens, NY","h1":"Escuela de Barbería para Residentes de Queens",
  "title":"Escuela de Barbería en Queens, NY | American Barber Institute",
  "desc":"Fórmate como Barbero Maestro licenciado en la única escuela de barbería dedicada de NYC — a un corto viaje en tren desde Queens hasta Midtown Manhattan. Programa de 500 horas, horarios flexibles, planes de pago semanales.",
  "intro":["Desde Astoria y Long Island City hasta Jackson Heights, Flushing y Jamaica — los residentes de Queens se forman para una verdadera carrera detrás de la silla en una de las únicas escuelas de barbería dedicadas de Nueva York, a un corto viaje de Midtown Manhattan.",
           "Obtén tu licencia de Barbero Maestro del Estado de NY en tan solo 4 meses con entrenamiento práctico, clientes reales y horarios pensados para quienes viajan desde Queens."],
  "getting":"Un viaje rápido en los trenes E, F, M, R o 7 hasta Midtown te deja a pocas cuadras de nuestra sede de Manhattan en West 39th Street; el LIRR hasta Penn Station también funciona."},
 "barber-school-brooklyn-new-york": {"loc":"Brooklyn, NY","h1":"Escuela de Barbería para Brooklyn, NY",
  "title":"Escuela de Barbería en Brooklyn, NY | American Barber Institute",
  "desc":"Conviértete en Barbero Maestro licenciado — nuestra sede de Midtown Manhattan está a 20–40 minutos de la mayor parte de Brooklyn. Programa práctico de 500 horas, horarios flexibles, planes de pago semanales.",
  "intro":["Desde Williamsburg y Bushwick hasta Bed-Stuy, Flatbush, Bay Ridge y Coney Island — los estudiantes de Brooklyn se forman para una verdadera carrera detrás de la silla en la única escuela de barbería dedicada de Nueva York.",
           "La mayoría de los vecindarios de Brooklyn llegan a nuestra sede en 20–40 minutos, y nuestros horarios de mañana, tarde y fin de semana se adaptan al trabajo y la familia."],
  "getting":"La mayoría de los vecindarios de Brooklyn llegan a nuestra sede de West 39th Street en 20–40 minutos en los trenes B, D, N, Q, R o 2/3/4/5."},
 "barber-school-yonkers-new-york": {"loc":"Yonkers, NY","h1":"Escuela de Barbería para Yonkers, NY",
  "title":"Escuela de Barbería en Yonkers, NY | American Barber Institute",
  "desc":"Yonkers está justo en el límite con el Bronx — nuestra sede de Westchester Square es una de las escuelas de barbería dedicadas más cercanas. Instrucción bilingüe, planes de pago, preparación para la licencia de NY.",
  "intro":["Yonkers está justo en el límite con el Bronx, lo que hace de nuestra sede del Bronx una de las escuelas de barbería dedicadas más cercanas — desde Getty Square hasta Park Hill, tu nueva carrera está a minutos.",
           "Entrena de forma práctica con clientes reales, con instrucción bilingüe (se habla español) y planes de pago flexibles."],
  "getting":"Un corto trayecto por la Major Deegan o la Saw Mill, o Metro-North más un bus local desde el centro de Yonkers."},
 "barber-school-westchester-ny": {"loc":"Westchester, NY","h1":"Escuela de Barbería para el Condado de Westchester",
  "title":"Escuela de Barbería en Westchester, NY | American Barber Institute",
  "desc":"Residentes del Condado de Westchester: fórmate como Barbero Maestro licenciado en nuestra sede del Bronx — fácil por Metro-North o la I-95. Clínica práctica, horarios flexibles, planes de pago semanales.",
  "intro":["Desde Mount Vernon y New Rochelle hasta White Plains — los estudiantes de Westchester obtienen su licencia de Barbero Maestro del Estado de NY en nuestra sede del Bronx, un viaje fácil por Metro-North o la I-95.",
           "Nuestro programa pone las máquinas en tus manos desde el principio con clientes reales de la clínica, para que te gradúes listo para trabajar."],
  "getting":"Por Metro-North (línea Harlem) más una conexión corta, o directo por la I-95 / Hutchinson River Parkway."},
 "barber-school-long-island-ny": {"loc":"Long Island, NY","h1":"Escuela de Barbería para Long Island, NY",
  "title":"Escuela de Barbería en Long Island, NY | American Barber Institute",
  "desc":"A un viaje en LIRR desde Nassau y Suffolk: nuestra sede de Manhattan está a pocas cuadras de Penn Station. Programa de Barbero Maestro de 500 horas con horarios de tarde y fin de semana que se adaptan al viaje.",
  "intro":["Estudiantes de Nassau y Suffolk: nuestra sede de Manhattan está a pocas cuadras de Penn Station, lo que hace el viaje en LIRR muy sencillo.",
           "Los horarios de tarde y fin de semana se adaptan al viaje desde la Isla — obtén tu licencia de Barbero Maestro del Estado de NY en tan solo 4 meses."],
  "getting":"Toma el LIRR directo hasta Penn Station; nuestra sede de West 39th Street está a una corta caminata."},
 "barber-school-mount-vernon-ny": {"loc":"Mount Vernon, NY","h1":"Escuela de Barbería para Mount Vernon, NY",
  "title":"Escuela de Barbería en Mount Vernon, NY | American Barber Institute",
  "desc":"Mount Vernon limita con el Bronx — nuestra sede de Westchester Square está a la vuelta de la esquina. Entrena de forma práctica para la licencia de Barbero Maestro de NY con planes de pago flexibles.",
  "intro":["Mount Vernon limita con el Bronx, así que nuestra sede de Westchester Square está a la vuelta de la esquina — a minutos de casa, con una clínica de clientes reales.",
           "Entrena en mañanas, tardes o fines de semana, con instrucción bilingüe y planes de pago semanales."],
  "getting":"A minutos en auto, o un corto viaje en los trenes 2/5 más un bus local desde Mount Vernon."},
 "barber-school-port-chester-ny": {"loc":"Port Chester, NY","h1":"Escuela de Barbería para Port Chester, NY",
  "title":"Escuela de Barbería en Port Chester, NY | American Barber Institute",
  "desc":"La escuela de barbería dedicada más cercana hacia el sur desde el este de Westchester — llega a nuestra sede del Bronx por Metro-North o la I-95 en 30–40 minutos. Preparación para la licencia de NY, planes de pago.",
  "intro":["Bajando desde el este de Westchester, la sede del Bronx de ABI es la escuela de barbería dedicada más cercana — aproximadamente a 30–40 minutos de Port Chester.",
           "Entrenamiento práctico con clientes reales, instructores bilingües y horarios que se adaptan a tu trabajo."],
  "getting":"Por Metro-North (línea New Haven) o directo por la I-95 — aproximadamente 30–40 minutos al sur."},
 "barber-school-connecticut": {"loc":"Connecticut","h1":"Escuela de Barbería para Quienes Viajan desde Connecticut",
  "title":"Escuela de Barbería Cerca de Connecticut | American Barber Institute",
  "desc":"Greenwich, Stamford, Norwalk: entrena justo cruzando la línea estatal en nuestra sede del Bronx. Nota: nuestro programa te prepara para la licencia de Barbero Maestro del Estado de Nueva York.",
  "intro":["Desde Greenwich, Stamford y Norwalk — quienes viajan desde el Condado de Fairfield entrenan justo cruzando la línea estatal en nuestra sede del Bronx, una de las escuelas de barbería dedicadas más cercanas a Connecticut.",
           "Obtén la licencia de Barbero Maestro del Estado de Nueva York con entrenamiento práctico en clínica y planes de pago semanales."],
  "getting":"Por Metro-North (línea New Haven) hasta el Bronx, o por la I-95 — el Condado de Fairfield está justo cruzando la línea estatal.",
  "disclaimer":"Ten en cuenta: American Barber Institute está licenciado por el Departamento de Educación del Estado de Nueva York y nuestro programa te prepara para la licencia de Barbero Maestro del Estado de NY. Los residentes de Connecticut son bienvenidos; verifica los requisitos de licencia propios de Connecticut si planeas trabajar en CT."},
 "barber-school-pennsylvania": {"loc":"Pennsylvania","h1":"Escuela de Barbería para Estudiantes de Pennsylvania",
  "title":"Escuela de Barbería Cerca de Pennsylvania | American Barber Institute",
  "desc":"Estudiantes del este de PA que se mudan o viajan al área de NYC: nuestra sede de Manhattan está a una corta caminata de Penn Station. Te prepara para la licencia de Barbero Maestro del Estado de Nueva York.",
  "intro":["Para estudiantes del este de Pennsylvania que se mudan o viajan al área de la Ciudad de Nueva York, la sede de Manhattan de ABI está a una corta caminata de Penn Station.",
           "Entrena de forma práctica para la licencia de Barbero Maestro del Estado de Nueva York, con horarios de mañana, tarde y fin de semana."],
  "getting":"A una corta caminata de Penn Station para quienes llegan en tren o autobús a la ciudad.",
  "disclaimer":"Ten en cuenta: American Barber Institute está licenciado por el Departamento de Educación del Estado de Nueva York y nuestro programa te prepara para la licencia de Barbero Maestro del Estado de NY. Si planeas trabajar en PA, verifica los requisitos de licencia de barbero propios de Pennsylvania."},
}

PAGES = []
# program pages
PAGES.append({"type":"program","lang":"en","path":"500-hours-master-barber-program-landing-page/index.html",
 "url":"/500-hours-master-barber-program-landing-page","alt":"/es/500-hours-master-barber-program-landing-page",
 "title":"500 Hour Master Barber Program — Manhattan | American Barber Institute",
 "desc":"Become a licensed Master Barber in New York in as little as 4 months. Comprehensive 500-hour hands-on training in Manhattan with flexible schedules, job placement, and NY State Board Exam prep. Starting at $4,600.",
 "campus":MANHATTAN,"h1a":"500 Hours.","h1b":"Barber Program.","script":"Start Today.",
 "sub":"Become a licensed Barber in as little as <b>4 months</b>. Comprehensive hands-on training and full NY State Board Exam prep at our Manhattan campus.",
 "about":ABOUT_MAN_EN,"about_h":"About the Program","tech":TECH_MAN_EN,"curr":CURR_MAN_EN,
 "hero_img":"abi-students-107.jpg","dur":"~4 Months","tui":"$4,600"})
PAGES.append({"type":"program","lang":"es","path":"es/500-hours-master-barber-program-landing-page/index.html",
 "url":"/es/500-hours-master-barber-program-landing-page","alt":"/500-hours-master-barber-program-landing-page",
 "title":"Programa de Barbero Maestro de 500 Horas — Manhattan | American Barber Institute",
 "desc":"Conviértete en Barbero Maestro licenciado en Nueva York en tan solo 4 meses. Entrenamiento práctico de 500 horas en Manhattan, horarios flexibles, asistencia de empleo y preparación para el examen del Estado de NY. Desde $4,600.",
 "campus":MANHATTAN,"h1a":"500 Horas.","h1b":"Programa de Barbero.","script":"Empieza Hoy.",
 "sub":"Conviértete en Barbero Maestro licenciado en tan solo <b>cuatro meses</b>. Entrenamiento práctico integral y preparación completa para el examen del Estado de NY en nuestra sede de Manhattan.",
 "about":ABOUT_MAN_ES,"about_h":"Sobre el Programa","tech":TECH_MAN_ES,"curr":CURR_MAN_ES,
 "hero_img":"abi-students-107.jpg","dur":"~4 Meses","tui":"$4,600"})
PAGES.append({"type":"program","lang":"en","path":"master-barber-program-bronx/index.html",
 "url":"/master-barber-program-bronx","alt":"/es/master-barber-program-bronx",
 "title":"Master Barber Program — Bronx | American Barber Institute",
 "desc":"Become a licensed Master Barber in New York at our Bronx campus. 500-hour hands-on training with full-time and weekend schedules, flexible payment plans, and NY State Board Exam prep. Starting at $4,600. Se habla español.",
 "campus":BRONX,"h1a":"Barber Operator","h1b":"Program.","script":"Start Today.",
 "sub":"Become a licensed Master Barber with affordable payment plans, full-time and weekend schedules, and <b>bilingual instruction</b> at our Bronx campus. Se habla español.",
 "about":ABOUT_BX_EN,"about_h":"About the Program","tech":TECH_BX_EN,"curr":CURR_BX_EN,
 "hero_img":"abi-students-107.jpg","dur":"~4 Months","tui":"$4,600"})
PAGES.append({"type":"program","lang":"es","path":"es/master-barber-program-bronx/index.html",
 "url":"/es/master-barber-program-bronx","alt":"/master-barber-program-bronx",
 "title":"Programa de Barbero Maestro — Bronx | American Barber Institute",
 "desc":"Conviértete en Barbero Maestro licenciado en Nueva York en nuestra sede del Bronx. Entrenamiento práctico de 500 horas con horarios de tiempo completo y fines de semana, planes de pago flexibles y preparación para el examen del Estado de NY. Desde $4,600. Se habla español.",
 "campus":BRONX,"h1a":"Programa de Barbero","h1b":"Operador.","script":"Empieza Hoy.",
 "sub":"Conviértete en Barbero Maestro licenciado con planes de pago asequibles, horarios de tiempo completo y fines de semana, e <b>instrucción bilingüe</b> en nuestra sede del Bronx. Se habla español.",
 "about":ABOUT_BX_ES,"about_h":"Sobre el Programa","tech":TECH_BX_ES,"curr":CURR_BX_ES,
 "hero_img":"abi-students-107.jpg","dur":"~4 Meses","tui":"$4,600"})
# splash pages
for n, (h1a_en,h1b_en,h1a_es,h1b_es) in (
    (1,("Your Future.","Your Career.","Tu Futuro.","Tu Carrera.")),
    (2,("A New Career.","In 17 Weeks.","Una Nueva Carrera.","En 17 Semanas."))):
    PAGES.append({"type":"splash","lang":"en","path":"splash-page-%d/index.html"%n,
     "url":"/splash-page-%d"%n,"alt":"/es/splash-page-%d"%n,
     "title":"Become a Licensed Barber in NYC | American Barber Institute",
     "desc":"New York's only dedicated barber school — changing lives for over 30 years. Become a licensed barber in as little as 17 weeks. Hands-on training. Real skills. Real opportunities.",
     "campus":MANHATTAN,"h1a":h1a_en,"h1b":h1b_en,"script":"Start Today.",
     "sub":"Become a licensed barber in as little as <b>17 weeks</b>. Hands-on training. Real skills. Real opportunities.",
     "hero_img":"abi-students-107.jpg","dur":"~4 Months","tui":"$4,600","variant":n})
    PAGES.append({"type":"splash","lang":"es","path":"es/splash-page-%d/index.html"%n,
     "url":"/es/splash-page-%d"%n,"alt":"/splash-page-%d"%n,
     "title":"Conviértete en Barbero Licenciado en NYC | American Barber Institute",
     "desc":"La única escuela de barbería dedicada en Nueva York. Licenciada por el Departamento de Educación del Estado de NY. Cambiando vidas por más de 30 años.",
     "campus":MANHATTAN,"h1a":h1a_es,"h1b":h1b_es,"script":"Empieza Hoy.",
     "sub":"Conviértete en barbero licenciado en tan solo <b>17 semanas</b>. Entrenamiento práctico. Habilidades reales. Oportunidades reales.",
     "hero_img":"abi-students-107.jpg","dur":"~4 Meses","tui":"$4,600","variant":n})
PAGES.append({"type":"splash","lang":"en","path":"index.html",
 "url":"/","alt":"/es",
 "title":"Barber School NYC | American Barber Institute — Become a Licensed Barber in 4 Months",
 "desc":"NYC's only dedicated barber school, est. 1996. NYS-licensed 500-hour Master Barber program, financial aid, veterans GI Bill, ACCESS-VR and job placement. New classes start the first Monday of every month.",
 "campus":MANHATTAN,"h1a":"Your Future.","h1b":"Your Career.","script":"Start Today.",
 "sub":"Become a licensed barber in as little as <b>17 weeks</b>. Hands-on training. Real skills. Real opportunities.",
 "hero_img":"abi-students-107.jpg","dur":"~4 Months","tui":"$4,600","variant":1})
PAGES.append({"type":"splash","lang":"es","path":"es/index.html",
 "url":"/es","alt":"/",
 "title":"Escuela de Barbería en NYC | American Barber Institute — Conviértete en Barbero Licenciado",
 "desc":"La única escuela de barbería dedicada en Nueva York. Licenciada por el Departamento de Educación del Estado de NY. Cambiando vidas por más de 30 años. Clases nuevas el primer lunes de cada mes.",
 "campus":MANHATTAN,"h1a":"Tu Futuro.","h1b":"Tu Carrera.","script":"Empieza Hoy.",
 "sub":"Conviértete en barbero licenciado en tan solo <b>17 semanas</b>. Entrenamiento práctico. Habilidades reales. Oportunidades reales.",
 "hero_img":"abi-students-107.jpg","dur":"~4 Meses","tui":"$4,600","variant":1})
# location pages (EN + ES)
for L in LOCATIONS:
    PAGES.append({"type":"location","lang":"en","path":L["slug"]+"/index.html",
     "url":"/"+L["slug"],"alt":"/es/"+L["slug"],"title":L["title"],"desc":L["desc"],
     "campus":L["campus"],"h1a":L["h1"],"h1b":"","script":"Start Today.",
     "sub":L["intro"][0],"loc":L,"hero_img":"abi-students-107.jpg","dur":"~4 Months","tui":"$4,600"})
    E = LOC_ES[L["slug"]]
    LE = dict(L); LE.update(E)
    PAGES.append({"type":"location","lang":"es","path":"es/"+L["slug"]+"/index.html",
     "url":"/es/"+L["slug"],"alt":"/"+L["slug"],"title":E["title"],"desc":E["desc"],
     "campus":L["campus"],"h1a":E["h1"],"h1b":"","script":"Empieza Hoy.",
     "sub":E["intro"][0],"loc":LE,"hero_img":"abi-students-107.jpg","dur":"~4 Meses","tui":"$4,600"})

# ── GLOBAL HERO OVERRIDE: exact mockup content on every landing page ──
for _p in PAGES:
    _es = _p["lang"] == "es"
    _campus_en = "Manhattan" if _p["campus"] is MANHATTAN else "Bronx"
    _p["h1a"] = "500 Horas." if _es else "500 Hours."
    _p["h1b"] = "Programa de Barbero." if _es else "Barber Program."
    _p["script"] = "Empieza Hoy." if _es else "Start Today."
    if _es:
        _campus = "sede de Manhattan" if _campus_en == "Manhattan" else "sede del Bronx"
        _p["sub"] = ("Conviértete en Barbero licenciado en tan solo <b>4 meses</b>. "
                     "Entrenamiento práctico integral y preparación completa para el examen "
                     "del Estado de NY en nuestra %s." % _campus)
    else:
        _p["sub"] = ("Become a licensed Barber in as little as <b>4 months</b>. "
                     "Comprehensive hands-on training and full NY State Board Exam prep "
                     "at our %s campus." % _campus_en)

# ───────────────────────── template parts ─────────────────────────
def head(p, s, pre):
    alt = ""
    if p["alt"]:
        en_url = p["url"] if p["lang"] == "en" else p["alt"]
        es_url = p["alt"] if p["lang"] == "en" else p["url"]
        alt = ('<link rel="alternate" hreflang="en" href="%s%s">\n'
               '<link rel="alternate" hreflang="es" href="%s%s">\n'
               '<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE,en_url,SITE,es_url,SITE,en_url))
    jsonld = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"TradeSchool","name":"American Barber Institute",
"url":"%s%s","telephone":"%s","foundingDate":"1996",
"address":{"@type":"PostalAddress","streetAddress":"%s"},
"aggregateRating":{"@type":"AggregateRating","ratingValue":"4.3","reviewCount":"100"}}
</script>
<script type="application/ld+json">%s</script>
<script type="application/ld+json">%s</script>""" % (SITE, p["url"], p["campus"]["tel_disp"], p["campus"]["addr"],
        json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQS[p["lang"]]]}, ensure_ascii=False),
        json.dumps({"@context":"https://schema.org","@type":"Course","name":"500-Hour Master Barber Program",
            "description":p["desc"],"provider":{"@type":"TradeSchool","name":"American Barber Institute","sameAs":SITE},
            "offers":{"@type":"Offer","price":"4600","priceCurrency":"USD","category":"Tuition"},
            "hasCourseInstance":{"@type":"CourseInstance","courseMode":"Onsite","location":p["campus"]["addr"]}}, ensure_ascii=False))
    return """<!DOCTYPE html>
<html lang="%s">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s%s">
%s
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:type" content="website">
<meta property="og:url" content="%s%s">
<meta name="theme-color" content="#1b2fd9">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Caveat:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%sassets/css/landing.css?v=42">
<script>(function(){try{if(!localStorage.getItem('abi-theme-user')){localStorage.removeItem('abi-theme');}var t=localStorage.getItem('abi-theme');if(t&&t!=='blue')document.documentElement.setAttribute('data-theme',t);}catch(e){}})();</script>
%s
</head>
<body>""" % (p["lang"], p["title"], p["desc"], SITE, p["url"], alt,
             p["title"], p["desc"], SITE, p["url"], pre, jsonld)

def header(p, s, pre):
    lang = p["lang"]
    pills = "".join(
        '<a class="phone-pill" href="tel:%s">%s<span><span class="lbl">%s: </span>%s</span></a>'
        % (tel, icon("phone",16), lbl, disp) for lbl, disp, tel in s["en_es_phones"])
    home = pre + ("es/index.html" if lang == "es" else "index.html")
    # language toggle target
    alt = p.get("alt")
    if alt is not None:
        a = alt.strip("/")
        alt_href = pre + (a + "/" if a else "")
        if alt_href == "": alt_href = "./"
    else:
        alt_href = pre + ("index.html" if lang == "es" else "es/index.html")
    en_href = alt_href if lang == "es" else "#"
    es_href = alt_href if lang == "en" else "#"
    # main nav
    items = ""
    drawer = '<a href="%s">%s</a>' % (home, "Inicio" if lang == "es" else "Home")
    for label, target in NAV[lang]:
        if target is None:
            drop = "".join('<a href="%s%s%s/">%s</a>' % (pre, "es/" if lang == "es" else "", slug, name)
                           for name, slug in LOC_NAMES)
            items += ('<div class="mn-sub"><a href="%s%s%s/">%s %s</a><div class="mn-drop">%s</div></div>'
                      % (pre, "es/" if lang == "es" else "", LOC_NAMES[0][1], NAV_LOC_LABEL[lang], icon("chev",13), drop))
            drawer += '<a href="%s%s%s/">%s</a>' % (pre, "es/" if lang == "es" else "", LOC_NAMES[0][1], NAV_LOC_LABEL[lang])
        else:
            items += '<a href="%s%s">%s</a>' % (pre, target, label)
            drawer += '<a href="%s%s">%s</a>' % (pre, target, label)
    drawer += ('<a href="%s"><b>%s</b></a>' % (alt_href, "English" if lang == "es" else "Español"))
    if lang == "es":
        lt = '<div class="lang-toggle" role="group" aria-label="Idioma"><a href="%s">EN</a><a class="is-active" aria-current="true">ES</a></div>' % alt_href
    else:
        lt = '<div class="lang-toggle" role="group" aria-label="Language"><a class="is-active" aria-current="true">EN</a><a href="%s">ES</a></div>' % alt_href
    return """
<div class="topbar">%s<span class="theme-dots" role="group" aria-label="Color theme"><button class="tdot tdot-blue" data-set-theme="blue" aria-label="ABI Blue" title="ABI Blue"></button><button class="tdot tdot-midnight" data-set-theme="midnight" aria-label="Midnight Gold" title="Midnight Gold"></button><button class="tdot tdot-classic" data-set-theme="classic" aria-label="Classic Americana" title="Classic Americana"></button><button class="tdot tdot-emerald" data-set-theme="emerald" aria-label="Emerald" title="Emerald"></button><button class="tdot tdot-noir" data-set-theme="noir" aria-label="Crimson Noir" title="Crimson Noir"></button></span></div>
<header class="hdr">
  <div class="hdr-in">
    <a class="logo" href="%s" aria-label="American Barber Institute — home" title="American Barber Institute">
      <img class="logo-img" src="/assets/img/abi-logo.gif" alt="American Barber Institute" width="385" height="99" fetchpriority="high">
    </a>
    %s
    <div class="hdr-phones">%s</div>
    <button class="hamburger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
  <nav class="mainnav" aria-label="Main">%s
    <span class="mn-lang"><a href="%s" %s>EN</a> | <a href="%s" %s>ES</a></span>
  </nav>
  <nav class="nav-drawer"><div class="container">%s</div></nav>
</header>
<div class="urgency">
  <div class="urgency-flame">%s</div>
  <div class="urgency-sub">%s</div>
</div>
<div class="startpill-wrap">
  <span class="startpill">%s <span>%s</span> <span class="dot">•</span> <span>%s <b data-next-start>%s</b></span></span>
</div>""" % (s["topbar"], home, lt, pills, items,
             en_href, 'style="color:var(--blue)"' if lang == "en" else "",
             es_href, 'style="color:var(--blue)"' if lang == "es" else "", drawer,
             s["limited"], s["reserve"],
             icon("pin",16), p["campus"]["name_"+lang], s["next_start"],
             NEXT_START_ES if lang == "es" else NEXT_START_EN)

def lead_form(p, s):
    locs = "".join('<option>%s</option>' % o for o in s["locs"])
    fmts = "".join('<option>%s</option>' % o for o in s["fmts"])
    return """
<div class="formcard" id="reserve">
  <div class="formcard-head">
    <div class="formcard-ico">%s</div>
    <div>
      <div class="formcard-title">%s</div>
      <div class="formcard-sub">%s</div>
    </div>
  </div>
  <form class="leadform" novalidate>
    <input type="hidden" name="page" value="%s">
    <input type="hidden" name="language" value="%s">
    <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
    <input type="hidden" name="_subject" value="New ABI website lead">
    <div class="field"><label>%s <span class="req">*</span></label>
      <input type="text" name="first_name" placeholder="%s" required autocomplete="given-name"></div>
    <div class="field"><label>%s <span class="req">*</span></label>
      <input type="text" name="last_name" placeholder="%s" required autocomplete="family-name"></div>
    <div class="field has-ico"><label>%s <span class="req">*</span></label>
      %s<input type="tel" name="phone" placeholder="(917) 693-0872" required autocomplete="tel"></div>
    <div class="field has-ico"><label>%s <span class="req">*</span></label>
      %s<input type="email" name="email" placeholder="name@email.com" required autocomplete="email"></div>
    <div class="field select"><label>%s <span class="req">*</span></label>
      <select name="campus_preference" required><option value="" selected disabled>%s</option>%s</select></div>
    <div class="field select"><label>%s <span class="req">*</span></label>
      <select name="schedule_preference" required><option value="" selected disabled>%s</option>%s</select></div>
    <button class="btn btn-blue btn-submit" type="submit">%s</button>
    <div class="form-error">%s <a href="tel:%s"><b>%s</b></a></div>
    <p class="form-consent">%s</p>
  </form>
  <div class="form-success">%s<h3>%s</h3><p>%s</p></div>
</div>""" % (icon("user",20), s["reserve"], s["form_sub"], p["url"], p["lang"],
             s["fn"], s["fn"], s["ln"], s["ln"],
             s["ph"], icon("phone",15), s["em"], icon("mail",15),
             s["q_loc"], s["opt_loc"], locs, s["q_fmt"], s["opt_fmt"], fmts,
             s["submit"], s["form_err"], p["campus"]["tel"], p["campus"]["tel_disp"], s["consent"],
             icon("check",42), s["success_h"], s["success_p"])

def hero(p, s, pre):
    feats = "".join('<div class="feature">%s<span>%s</span></div>' % (icon(i,20), t) for i, t in s["features"])
    h1b = '<span class="accent">%s</span><br>' % p["h1b"] if p["h1b"] else ""
    return """
<section class="hero">
  <div class="hero-bg" style="background-image:url('/assets/img/%s'),url('/assets/img/about.jpg')"></div>
  <div class="hero-grad"></div>
  <div class="container hero-in">
    <div class="hero-copy">
      <h1 class="hero-h1">%s<br>%s<span class="hero-script">%s</span></h1>
      <p class="hero-sub">%s</p>
      <div class="features">%s</div>
    </div>
    %s
  </div>
</section>
<section class="trust"><div class="container trust-in">%s</div></section>""" % (
        p["hero_img"],
        p["h1a"], h1b, p["script"], p["sub"], feats, lead_form(p, s),
        "".join('<div class="trust-item">%s<span>%s</span></div>' % (icon(i,30), t) for i, t in s["trust"]))

TICKER = {
 "en": ["Classic Tapers","Low Fades","Mid Fades","High Fades","Razor Lineups","Hot Towel Shaves","Pompadours","Beard Trims","Shape Ups","Caesars","Flat Tops","High-Top Fades","Mohawks","Blowouts"],
 "es": ["Degradados Clásicos","Fades Bajos","Fades Medios","Fades Altos","Líneas con Navaja","Afeitado con Toalla Caliente","Pompadours","Recortes de Barba","Shape Ups","Caesars","Flat Tops","High-Top Fades","Mohawks","Blowouts"],
}
def sec_ticker(p, s):
    items = "".join('<span>%s</span><span class="sc">✂</span>' % t for t in TICKER[p["lang"]])
    return '<div class="ticker" aria-hidden="true"><div class="ticker-track">%s%s</div></div>' % (items, items)

def sec_stats(p, s):
    es = p["lang"] == "es"
    data = [(30,"+","Años en el Negocio" if es else "Years in Business"),
            (10000,"+","Graduados" if es else "Graduates"),
            (100,"+","Reseñas de Google" if es else "Google Reviews"),
            (4,"","Meses Para Tu Licencia" if es else "Months To Get Licensed")]
    cells = "".join('<div class="stat"><b data-count="%d" data-suffix="%s">%s</b><span>%s</span></div>' % (n, suf, "{:,}{}".format(n, suf), lbl) for (n, suf, lbl) in data)
    return '<section class="stats"><div class="container stats-in">%s</div></section>' % cells

def sec_about(p, s):
    paras = "".join("<p>%s</p>" % x for x in p["about"])
    return """
<section class="sec"><div class="container split">
  <div class="rv"><span class="eyebrow">%s</span><h2>%s</h2><div class="prose">%s</div></div>
  <div class="rv">
    <div class="campus">
      <h3>%s</h3><p>%s %s</p>
      <p><a href="tel:%s"><b>%s</b></a></p>
      <a class="maplink" href="https://maps.google.com/?q=%s" target="_blank" rel="noopener">Google Maps →</a>
      <hr style="border:none;border-top:1px solid var(--line);margin:1.1rem 0">
      <h3>%s</h3>
      <p><b>%s:</b> %s</p><p><b>%s:</b> %s %s</p><p><b>%s:</b> %s</p>
    </div>
  </div>
</div></section>""" % (s["about_eb"], p["about_h"], paras,
        p["campus"]["name_"+p["lang"]], icon("pin",15), p["campus"]["addr"],
        p["campus"]["tel"], p["campus"]["tel_disp"], p["campus"]["addr"].replace(" ","+"),
        s["details_h"], s["d_dur"], p["dur"], s["d_tui"], s["d_from"], p["tui"], s["d_sch"], s["d_sch_v"])

def sec_tech(p, s):
    chips = "".join('<span class="chip">%s</span>' % t for t in p["tech"])
    return """
<section class="sec sec-alt"><div class="container rv">
  <span class="eyebrow">%s</span><h2>%s</h2>
  <div class="chips">%s</div>
</div></section>""" % (s["tech_eb"], s["tech_h"], chips)

def sec_curr(p, s):
    items = ""
    for i, (name, lis) in enumerate(p["curr"], 1):
        body = "".join("<li>%s</li>" % x for x in lis)
        items += """<div class="acc-item%s">
  <button class="acc-btn" type="button"><span class="acc-num">0%d</span>%s<span class="chev">%s</span></button>
  <div class="acc-body"><ul>%s</ul></div></div>""" % (" open" if i == 1 else "", i, name, icon("chev",18), body)
    return """
<section class="sec"><div class="container rv" style="max-width:880px">
  <span class="eyebrow">%s</span><h2>%s</h2>
  <div class="acc">%s</div>
</div></section>""" % (s["curr_eb"], s["curr_h"], items)

def sec_tuition(p, s):
    cards = ""
    for pl in s["plans"]:
        cards += """<div class="plan%s rv">%s
  <div class="plan-name">%s</div>
  <div class="plan-sched">%s</div><div class="plan-hours">%s</div>
  <div class="plan-price">%s</div><div class="plan-terms">%s</div>
  <a class="btn btn-blue" href="#reserve">%s</a></div>""" % (
            " popular" if pl["pop"] else "",
            '<div class="plan-tag">%s</div>' % s["pop_tag"] if pl["pop"] else "",
            pl["name"], pl["sched"], pl["hours"], pl["price"], pl["terms"], s["plan_cta"])
    return """
<section class="sec sec-alt"><div class="container">
  <div class="rv"><span class="eyebrow">%s</span><h2>%s</h2><p class="lead">%s</p></div>
  <div class="plans">%s</div>
  <p class="plans-note">%s</p>
</div></section>""" % (s["tuition_eb"], s["tuition_h"], s["tuition_lead"], cards, s["plans_note"])

def sec_reqs(p, s):
    items = "".join('<div class="req-item">%s<span>%s</span></div>' % (icon("check",18), r) for r in s["reqs"])
    return """
<section class="sec"><div class="container rv">
  <span class="eyebrow">%s</span><h2>%s</h2>
  <div class="reqs">%s</div>
</div></section>""" % (s["req_eb"], s["req_h"], items)

def sec_testi(p, s):
    cards = ""
    for t in s["testi"]:
        ini = "".join(w[0] for w in t["n"].split()[:2])
        cards += """<div class="testi-card rv"><div class="stars">★★★★★</div><p>"%s"</p>
  <div class="testi-who"><div class="testi-av">%s</div><div><b>%s</b><span>%s</span></div></div></div>""" % (
            t["q"], ini, t["n"], t["r"])
    return """
<section class="sec sec-alt"><div class="container">
  <div class="rv"><span class="eyebrow">%s</span><h2>%s</h2><p class="lead">%s</p></div>
  <div class="testi">%s</div>
  <p><a class="greview" href="https://maps.google.com/?q=American+Barber+Institute+48+West+39th+Street+New+York" target="_blank" rel="noopener">★ %s</a></p>
</div></section>""" % (s["testi_eb"], s["testi_h"], s["testi_sub"], cards,
        "Ver todas las reseñas en Google →" if p["lang"]=="es" else "View all reviews on Google →")

def sec_countdown(p, s):
    cells = "".join('<div class="count-cell"><b data-cd-%s>0</b><span>%s</span></div>'
                    % (k, lbl) for k, lbl in zip("dhms", s["count_lbl"]))
    return """
<section class="sec" style="padding:2.6rem 0;text-align:center"><div class="container rv">
  <span class="eyebrow">%s</span>
  <div class="count" data-countdown>%s</div>
  <a class="btn btn-blue" style="padding:.85rem 2.2rem" href="#reserve">%s</a>
</div></section>""" % (s["count_h"], cells, s["reserve"])

def sec_steps(p, s):
    if p["lang"] == "es":
        steps = [("Comienza","Envía tu información para iniciar tu camino en la barbería."),
                 ("Habla con un Asesor","Un asesor de admisiones de ABI responderá tus preguntas y revisará las opciones de planes de pago que se ajusten a tu presupuesto."),
                 ("Comienza el Entrenamiento","Completa tu matrícula y comienza a construir tu carrera en la barbería.")]
        eb, h = "3 Pasos Sencillos", "Conviértete en Barbero Profesional en 3 Pasos"
    else:
        steps = [("Get Started","Submit your info to start your barbering journey."),
                 ("Speak With an Advisor","An ABI admissions advisor will answer your questions and review payment plan options that fit your budget."),
                 ("Start Training","Complete your enrollment and start building your barbering career.")]
        eb, h = "3 Easy Steps", "Become a Professional Barber in 3 Easy Steps"
    cards = "".join('<div class="step rv"><div class="step-num">0%d</div><b>%s</b><p>%s</p></div>'
                    % (i, t, d) for i, (t, d) in enumerate(steps, 1))
    return '<section class="sec"><div class="container"><div class="rv"><span class="eyebrow">%s</span><h2>%s</h2></div><div class="steps">%s</div></div></section>' % (eb, h, cards)

def sec_earnings(p, s):
    if p["lang"] == "es":
        eb, h = "Ingresos de Carrera", "Ingresos de una Carrera de Barbero"
        rows = [("AÑO 1 · Barbero Principiante","$35,000–$45,000","Empezando en una barbería, construyendo tu clientela y refinando tu técnica.",False),
                ("AÑOS 2–3 · Barbero Establecido","$50,000–$70,000","Clientela leal, servicio más rápido e ingresos mayores conforme crece tu reputación.",True),
                ("AÑO 3+ · Inquilino de Silla / Dueño","$75,000–$100,000+","Control total de tu horario y ganancias — el camino hacia el verdadero emprendimiento.",False)]
        note = "Las cifras de ingresos son solo estimaciones y no están garantizadas. El ingreso real variará según el esfuerzo individual, horas trabajadas, ubicación y condiciones del mercado."
    else:
        eb, h = "Career Earnings", "Barber Career Earnings"
        rows = [("YEAR 1 · Entry-Level","$35,000–$45,000","Starting out in a shop, building your clientele and refining your technique.",False),
                ("YEARS 2–3 · Established","$50,000–$70,000","Loyal clientele, faster service and higher earnings as your reputation grows.",True),
                ("YEAR 3+ · Booth Renter / Shop Owner","$75,000–$100,000+","Full control of your schedule and earnings — the path to true entrepreneurship.",False)]
        note = "Earnings figures are estimates only and are not guaranteed. Actual income will vary based on individual effort, hours worked, location and market conditions."
    cards = "".join('<div class="earn-card%s rv"><div class="earn-yr">%s</div><div class="earn-amt">%s</div><p>%s</p></div>'
                    % (" mid" if mid else "", yr, amt, d) for yr, amt, d, mid in rows)
    return '<section class="sec sec-alt"><div class="container"><div class="rv"><span class="eyebrow">%s</span><h2>%s</h2></div><div class="earn">%s</div><p class="earn-note">%s</p></div></section>' % (eb, h, cards, note)

def sec_location(p, s):
    L = p["loc"]; c = L["campus"]; es = p["lang"] == "es"
    if es:
        why = [("badge","Licenciada por NYSED (BPSS)","Plan de estudios, programas e instructores aprobados por el estado."),
               ("mic","Práctica desde las primeras semanas","Clientes reales en nuestra clínica profesional — no maniquíes."),
               ("cal","Mañanas · Tardes · Fines de Semana","Horarios pensados para el trabajo y la familia."),
               ("hand","Asistencia financiera","ACCES-VR, Post-9/11 GI Bill® y beneficios de VA aceptados."),
               ("people","Bilingüe — se habla español","Instrucción y apoyo de admisiones en inglés y español."),
               ("case","Colocación laboral + examen estatal","Gradúate listo para la licencia, con apoyo de empleo esperándote.")]
        h_why, h_near, h_get = "Por Qué Entrenar Con Nosotros", "Tu Sede Más Cercana", "Cómo Llegar"
    else:
        why = [("badge","Licensed by NYSED (BPSS)","State-approved curriculum, programs and instructors."),
               ("mic","Hands-on from the first weeks","Real clients in our professional barber clinic — not mannequins."),
               ("cal","Morning · Afternoon · Weekend","Schedules built around work and family."),
               ("hand","Financial assistance","ACCES-VR, Post-9/11 GI Bill® and VA benefits accepted."),
               ("people","Bilingual — se habla español","Instruction and admissions support in English and Spanish."),
               ("case","Job placement + Board Exam prep","Graduate license-ready, with placement support waiting.")]
        h_why, h_near, h_get = "Why Train With Us", "Your Nearest Campus", "Getting Here"
    whyhtml = "".join('<div class="why-item rv">%s<b>%s</b>%s</div>' % (icon(i2,24), t, d) for i2, t, d in why)
    disc = '<p class="plans-note" style="margin-top:1.6rem">%s</p>' % L["disclaimer"] if L.get("disclaimer") else ""
    return """
<section class="sec"><div class="container split">
  <div class="rv"><span class="eyebrow">%s</span><h2>%s</h2>
    <div class="prose"><p>%s</p></div></div>
  <div class="rv"><div class="campus">
    <h3>%s — %s</h3>
    <p>%s %s</p><p><a href="tel:%s"><b>%s</b></a></p>
    <a class="maplink" href="https://maps.google.com/?q=%s" target="_blank" rel="noopener">Google Maps →</a>
    <hr style="border:none;border-top:1px solid var(--line);margin:1.1rem 0">
    <h3>%s %s</h3><p>%s</p>
  </div></div>
</div>
<div class="container"><div class="why">%s</div>%s</div></section>""" % (
        L["loc"], h_why, L["intro"][1],
        h_near, c["name_" + p["lang"]], icon("pin",15), c["addr"], c["tel"], c["tel_disp"], c["addr"].replace(" ","+"),
        icon("train",18), h_get, L["getting"], whyhtml, disc)


FAQS = {
 "en": [
  ("How much does barber school cost in New York?",
   "At ABI, the 500-hour Master Barber program starts at $4,600 (afternoon or weekend plans) or $5,600 (morning plan) — $500–$550 down and weekly payments of $150–$300 while you study. Books and tools are extra. ACCES-VR funding, Post-9/11 GI Bill® and VA benefits are accepted."),
  ("How long is barber school in New York?",
   "New York State requires 500 hours of training. Full-time at ABI takes about 4 months (17 weeks at 30 hours per week); the weekend schedule takes about 6–7 months (27 weeks)."),
  ("How many hours per week will I be in school?",
   "Full-time students train 30 hours per week, Monday to Friday, in morning (8:00 AM–2:00 PM) or afternoon (2:00 PM–8:00 PM) sessions. Weekend students train 18 hours per week on Saturdays and Sundays."),
  ("Do I need a high school diploma to enroll?",
   "A high school diploma or GED is required — or you can pass the Ability-To-Benefit (ATB) entrance exam at ABI instead. You must be at least 17 years old."),
  ("Can I take barber school online?",
   "No. New York State requires in-person, hands-on training hours. At ABI you practice on real clients in our supervised barber clinic from your first weeks — not on mannequins."),
  ("What license will I get after the program?",
   "The program prepares you for the New York State Master Barber license, including full NY State Board Exam preparation. Our job placement office helps you find work after you pass."),
  ("Is financial aid available?",
   "Yes — ACCES-VR can cover tuition, tools and books for qualified New Yorkers with disabilities; Post-9/11 GI Bill® and VA benefits are accepted; NYS Department of Labor grants may apply; and every plan includes weekly payments."),
  ("When do classes start?",
   "New classes begin the first Monday of every month at both the Manhattan and Bronx campuses. Call (212) 290-2289 to reserve your seat — classes fill fast."),
 ],
 "es": [
  ("¿Cuánto cuesta la escuela de barbería en Nueva York?",
   "En ABI, el programa de Barbero Maestro de 500 horas comienza desde $4,600 (planes de tarde o fin de semana) o $5,600 (plan de mañana) — $500–$550 de pago inicial y pagos semanales de $150–$300 mientras estudias. Libros y herramientas aparte. Se acepta ACCES-VR, Post-9/11 GI Bill® y beneficios de VA."),
  ("¿Cuánto dura la escuela de barbería en Nueva York?",
   "El Estado de Nueva York exige 500 horas de entrenamiento. A tiempo completo en ABI toma unos 4 meses (17 semanas a 30 horas por semana); el horario de fin de semana toma de 6 a 7 meses (27 semanas)."),
  ("¿Cuántas horas por semana estaré en la escuela?",
   "Los estudiantes de tiempo completo entrenan 30 horas por semana, de lunes a viernes, en sesiones de mañana (8:00 AM–2:00 PM) o tarde (2:00 PM–8:00 PM). Los estudiantes de fin de semana entrenan 18 horas por semana, sábados y domingos."),
  ("¿Necesito diploma de preparatoria para inscribirme?",
   "Se requiere diploma de preparatoria (HSD) o GED — o puedes aprobar el examen de admisión ATB en ABI. Debes tener al menos 17 años."),
  ("¿Puedo estudiar barbería en línea?",
   "No. El Estado de Nueva York exige horas prácticas presenciales. En ABI practicas con clientes reales en nuestra clínica supervisada desde las primeras semanas — no con maniquíes."),
  ("¿Qué licencia obtendré al terminar el programa?",
   "El programa te prepara para la licencia de Barbero Maestro del Estado de Nueva York, incluyendo la preparación completa para el Examen de la Junta Estatal. Nuestra oficina de empleo te ayuda a encontrar trabajo después de aprobar."),
  ("¿Hay ayuda financiera disponible?",
   "Sí — ACCES-VR puede cubrir matrícula, herramientas y libros para neoyorquinos calificados con discapacidades; se aceptan Post-9/11 GI Bill® y beneficios de VA; pueden aplicar subvenciones del Departamento de Trabajo de NY; y todos los planes incluyen pagos semanales."),
  ("¿Cuándo comienzan las clases?",
   "Las clases nuevas comienzan el primer lunes de cada mes en las sedes de Manhattan y el Bronx. Llama al (212) 290-0278 para reservar tu lugar — los cupos se llenan rápido."),
 ],
}
VIDEOS = [
 ("TFpNNqsc_EA", {"en":"Train to be a Master Barber at New York's #1 barber school","es":"Fórmate como Barbero Maestro en la escuela #1 de Nueva York"}),
 ("iU0fUj3a8uw", {"en":"Our courses are hands-on, fun and engaging","es":"Nuestros cursos son prácticos, divertidos y motivadores"}),
 ("ozV_RcSk0P4", {"en":"Tour our two-floor, 3,000 sq ft Manhattan campus","es":"Recorre nuestro campus de 3,000 pies² en Manhattan"}),
]
GALLERY = ["abi-students-001.jpg","abi-students-008.jpg","abi-students-017.jpg","abi-students-095.jpg",
           "abi-nyc-005.jpg","abi-students-056.jpg","abi-students-065.jpg","abi-students-080.jpg"]

def sec_faq(p, s):
    es = p["lang"] == "es"
    eb = "Preguntas Frecuentes" if es else "FAQs"
    h = "Preguntas Frecuentes Sobre la Escuela de Barbería" if es else "Barber School Questions, Answered"
    items = ""
    for i, (q, a) in enumerate(FAQS[p["lang"]], 1):
        items += ('<div class="acc-item%s"><button class="acc-btn" type="button"><span class="acc-num">%02d</span>'
                  '<h3 style="font-size:1rem;font-weight:600;margin:0">%s</h3><span class="chev">%s</span></button>'
                  '<div class="acc-body"><p style="color:var(--ink-soft);font-size:.95rem">%s</p></div></div>'
                  % (" open" if i == 1 else "", i, q, icon("chev",18), a))
    return ('<section class="sec sec-alt" id="faq"><div class="container rv" style="max-width:880px">'
            '<span class="eyebrow">%s</span><h2>%s</h2><div class="acc">%s</div></div></section>' % (eb, h, items))

def sec_videos(p, s, pre):
    es = p["lang"] == "es"
    eb = "Míranos" if es else "Watch Us"
    h = "Mira a ABI en Acción" if es else "See ABI In Action"
    cards = ""
    for vid, cap in VIDEOS:
        cards += ('<div class="rv"><button class="yt" data-yt="%s" aria-label="Play video">'
                  '<img loading="lazy" src="https://i.ytimg.com/vi/%s/hqdefault.jpg" alt="%s">'
                  '<span class="play"></span></button><p class="yt-cap">%s</p></div>' % (vid, vid, cap[p["lang"]], cap[p["lang"]]))
    return ('<section class="sec"><div class="container"><div class="rv"><span class="eyebrow">%s</span><h2>%s</h2></div>'
            '<div class="videos">%s</div></div></section>' % (eb, h, cards))

def sec_gallery(p, s, pre):
    es = p["lang"] == "es"
    eb = "Galería" if es else "Gallery"
    h = "La Vida en ABI" if es else "Life At ABI"
    more = "Ver Galería Completa →" if es else "View Full Gallery →"
    _alts_en = ["ABI student giving a client a fresh haircut",
                "Student barber practicing a skin fade",
                "Hands-on training on the ABI clinic floor",
                "Instructor guiding a student through a cut",
                "Detailed lineup work by an ABI student",
                "Students learning clipper technique at ABI",
                "Client in the chair at the ABI barber clinic",
                "Barbering students at work in the Manhattan campus"]
    _alts_es = ["Estudiante de ABI dando un corte a un cliente",
                "Estudiante practicando un fade",
                "Entrenamiento práctico en la clínica de ABI",
                "Instructor guiando a un estudiante en un corte",
                "Trabajo de líneas por un estudiante de ABI",
                "Estudiantes aprendiendo técnica de máquina en ABI",
                "Cliente en la silla de la clínica de ABI",
                "Estudiantes de barbería en el campus de Manhattan"]
    _alts = _alts_es if es else _alts_en
    imgs = "".join('<a href="%sgallery.html"><img loading="lazy" src="%sassets/img/%s" alt="%s"></a>'
                   % (pre, pre, g, _alts[i % len(_alts)]) for i, g in enumerate(GALLERY))
    return ('<section class="sec sec-alt"><div class="container rv"><span class="eyebrow">%s</span><h2>%s</h2>'
            '<div class="gal">%s</div><p style="margin-top:1.4rem"><a class="greview" href="%sgallery.html">%s</a></p>'
            '</div></section>' % (eb, h, imgs, pre, more))

def sec_dates(p, s):
    es = p["lang"] == "es"
    eb = "Fechas de Inicio" if es else "Start Dates"
    h = "Próximas Fechas de Inicio de Clases" if es else "Upcoming Class Start Dates"
    sub = ("Las clases nuevas comienzan el primer lunes de cada mes. Reserva tu lugar para la próxima fecha." if es
           else "New classes begin the first Monday of every month. Reserve your seat for the next start.")
    return ('<section class="sec" style="padding:2.8rem 0"><div class="container rv">'
            '<span class="eyebrow">%s</span><h2>%s</h2><p class="lead">%s</p>'
            '<div class="dates" data-start-dates></div></div></section>' % (eb, h, sub))

def closing(p, s):
    return """
<section class="closing"><div class="container">
  <h2>%s</h2><p>%s</p>
  <a class="btn btn-blue" href="#reserve">%s</a>
  <a class="tel" href="tel:%s">%s %s</a>
</div></section>""" % (s["closing_h"], s["closing_p"], s["closing_cta"],
                       p["campus"]["tel"], s["closing_call"], p["campus"]["tel_disp"])

def footer(p, s, pre):
    links = "".join('<a href="%s">%s</a>' % (pre + u.lstrip("/"), t) for t, u in s["f_linkitems"])
    return """
<footer class="ftr"><div class="container">
  <div class="ftr-in">
    <div><h4>American Barber Institute</h4><p>%s</p>
      <div class="socials">
        <a href="https://www.facebook.com/Abi.Education/" target="_blank" rel="noopener" aria-label="Facebook"><svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.2c0-.9.2-1.5 1.5-1.5h1.4V5.1C16.1 5 15.2 5 14.2 5c-2.2 0-3.7 1.3-3.7 3.8V11H8v3h2.5v7h3z"/></svg></a>
        <a href="https://www.instagram.com/americanbarberinstitute/" target="_blank" rel="noopener" aria-label="Instagram"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.3" cy="6.7" r="1.1" fill="currentColor" stroke="none"/></svg></a>
        <a href="https://twitter.com/amerbarberedu" target="_blank" rel="noopener" aria-label="X (Twitter)"><svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M17.8 3h3l-6.6 7.6L22 21h-6.1l-4.8-6.3L5.6 21h-3l7.1-8.1L2 3h6.3l4.3 5.7L17.8 3zm-1 16.2h1.7L7.3 4.7H5.5l11.3 14.5z"/></svg></a>
        <a href="https://www.youtube.com/channel/UCy_pQUDfk2ldEp6_zyaIMhQ" target="_blank" rel="noopener" aria-label="YouTube"><svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.5 12 4.5 12 4.5s-7 0-8.9.6A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12 31 31 0 0 0 1 16.8a3 3 0 0 0 2.1 2.1c1.9.6 8.9.6 8.9.6s7 0 8.9-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 23.5 12 31 31 0 0 0 23 7.2zM9.8 15.3V8.7L15.9 12l-6.1 3.3z"/></svg></a>
        <a href="https://www.pinterest.com/alexzholendz/american-barber-institute/" target="_blank" rel="noopener" aria-label="Pinterest"><svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-3.6 19.3c-.1-.8-.2-2 0-2.9l1.3-5.4s-.3-.7-.3-1.6c0-1.5.9-2.6 2-2.6.9 0 1.4.7 1.4 1.5 0 .9-.6 2.3-.9 3.6-.3 1.1.5 2 1.6 2 1.9 0 3.4-2 3.4-4.9 0-2.6-1.9-4.4-4.5-4.4a4.7 4.7 0 0 0-4.9 4.7c0 .9.4 1.9.8 2.5l-.3 1.1c-.1.4-.3.5-.7.3-1.2-.6-2-2.4-2-3.9 0-3.2 2.3-6.1 6.7-6.1 3.5 0 6.2 2.5 6.2 5.8 0 3.5-2.2 6.3-5.2 6.3-1 0-2-.5-2.3-1.1l-.6 2.4c-.2.9-.8 1.9-1.2 2.6A10 10 0 1 0 12 2z"/></svg></a>
      </div></div>
    <div><h4>%s</h4>%s</div>
    <div><h4>%s</h4>
      <a href="https://maps.google.com/?q=48+West+39th+Street,+New+York,+NY+10018" target="_blank" rel="noopener">48 West 39th Street, New York, NY 10018</a>
      <a href="https://maps.google.com/?q=121+Westchester+Square,+Bronx,+NY+10461" target="_blank" rel="noopener">121 Westchester Square, Bronx, NY 10461</a>
      <a href="tel:+12122902289">(212) 290-2289 · English</a>
      <a href="tel:+12122900278">(212) 290-0278 · Español</a>
      <a href="tel:+17186760640">(718) 676-0640 · Bronx</a>
      <a href="mailto:admission@abi.edu">admission@abi.edu</a>
    </div>
  </div>
  <div class="ftr-legal">© American Barber Institute (ABI). All rights reserved. · %s · *$150/week refers to Plan C weekly payments.</div>
</div></footer>
<div class="mbar">
  <a class="mbar-call" href="tel:%s">%s %s</a>
  <a class="mbar-cta" href="#reserve">%s</a>
</div>
<div class="bubble-tip">%s<button class="tip-x" aria-label="Close">✕</button></div>
<button class="bubble" aria-label="%s">%s</button>
<div class="exit" role="dialog" aria-modal="true">
  <div class="exit-card">
    <button class="exit-x" aria-label="Close">✕</button>
    <h3>%s</h3><p>%s</p>
    <button class="btn btn-blue" data-exit-cta style="padding:.85rem 2rem">%s</button>
  </div>
</div>
<script src="/assets/js/effects.js?v=30" defer></script>
<script src="%sassets/js/landing.js?v=30" defer></script>
</body>
</html>""" % (s["f_about"], s["f_links"], links, s["f_visit"], s["gibill"],
              p["campus"]["tel"], icon("phone",17), s["mbar_call"], s["mbar_cta"],
              s["bubble_tip"], s["reserve"], icon("chat",26),
              s["exit_h"], s["exit_p"], s["exit_cta"], pre)

# ───────────────────────── assemble ─────────────────────────
def build(p):
    s = S[p["lang"]]
    depth = p["path"].count("/")
    pre = "../" * depth
    parts = [head(p, s, pre), header(p, s, pre), hero(p, s, pre), sec_ticker(p, s), sec_stats(p, s)]
    if p["type"] == "program":
        parts += [sec_about(p, s), sec_tech(p, s), sec_curr(p, s),
                  sec_tuition(p, s), sec_reqs(p, s), sec_dates(p, s), sec_videos(p, s, pre),
                  sec_gallery(p, s, pre), sec_testi(p, s), sec_faq(p, s), sec_countdown(p, s)]
    elif p["type"] == "splash":
        parts += [sec_steps(p, s), sec_earnings(p, s), sec_tuition(p, s),
                  sec_dates(p, s), sec_videos(p, s, pre), sec_gallery(p, s, pre),
                  sec_testi(p, s), sec_faq(p, s), sec_countdown(p, s)]
    elif p["type"] == "location":
        parts += [sec_location(p, s), sec_tuition(p, s), sec_dates(p, s), sec_videos(p, s, pre),
                  sec_testi(p, s), sec_faq(p, s), sec_countdown(p, s)]
    parts += [closing(p, s), footer(p, s, pre)]
    out = os.path.join(ROOT, p["path"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    return p["path"]

if __name__ == "__main__":
    for p in PAGES:
        print("✓", build(p))
    print("\n%d pages generated." % len(PAGES))
