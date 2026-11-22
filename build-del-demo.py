#!/usr/bin/env python3
"""Adapt the Habana Medical Service demo site into a Del International
Hospital demo site.

Reads ~/workspace/user/files/habana-contact-page-rebuild-small.html and
writes ~/workspace/clinic-websites/del-international-hospital.html.

What changes:
- Branding: Habana Medical Service (Tamale) -> Del International Hospital
  (East Legon, Accra); phone, email, address, maps links.
- Colours: teal/amber -> navy/gold, so the demo does not look like Habana's.
- Services: removes Habana-only services (ENT, Ophthalmology, Neurosurgery,
  Endoscopy), renames Psychology -> Counselling, adds Del services
  (Fertility Centre, Physiotherapy, Dietetics). 15 -> 14 services.
- Removes Habana-only content: founder story, awards, 15-year celebration,
  CT scan / mammography claims (Del lists ultrasound, X-ray, ECG instead),
  the Friday 9:00 AM cervical clinic time, Habana social links, staff sign-in.
- Photos: Habana's embedded photos are replaced with professional stock
  photos matched to each service (del-photos/services/, 3 per service),
  plus stock photos for reception, maternity ward and the team. One real
  photo is used where it exists: the hospital building, from Del's
  GhanaYello listing (del-photos/del-building-ghanayello.jpg), for the
  hero, story carousel, About collage and contact-page photo. Stock photos
  are stand-ins for the demo — swap in Del's real photos when available.
"""
import base64
import json
import re
import urllib.parse
from pathlib import Path

SRC = Path.home() / "workspace/user/files/habana-contact-page-rebuild-small.html"
DST = Path.home() / "workspace/clinic-websites/del-international-hospital.html"
HERE = Path(__file__).resolve().parent


def _data_uri(path, mime="image/jpeg"):
    return "data:%s;base64,%s" % (
        mime, base64.b64encode(Path(path).read_bytes()).decode())


# The doctor-consultation photo the user sent (Gemini image, 1376x768):
# a Ghanaian woman doctor consulting a Ghanaian man. Used as hero slide 2.
DOCTOR_IMG = _data_uri(HERE / "del-photos" / "slides" / "doctor-consultation.jpg")
# Building photo: the bright, sharp AI-generated hospital photo the user sent
# (del-building-upscale.jpg), with the sign edited to read
# "DEL INTERNATIONAL HOSPITAL" — the original Gemini image said
# "EL-YAHWEH MEDICAL CENTRE", a different clinic, so the sign was fixed
# before use. The real Del photos (del-building-ghanayello.jpg,
# del-building-googlemaps.jpg) are kept as backups.
DEL_BUILDING_IMG = _data_uri(HERE / "del-photos" / "del-building-upscale.jpg")

# The real Del building photo the user sent (lavender building, white gate,
# Gemini-upscaled from the GhanaYello photo). Used as hero slide 3 only.
# NOTE: the small service list under the sign came out garbled in the
# Gemini upscale — too small to read in the slideshow, so it is left as is.
DEL_REAL_IMG = _data_uri(HERE / "del-photos" / "del-building-real.jpg")

DEL_PHONE = "030 254 3256"
DEL_PHONE_TEL = "+233302543256"
DEL_PHONE_WA = "233302543256"
DEL_EMAIL = "info@delinternationalhospital.com"
DEL_ADDR = "65/67 Nii Sai Street, East Legon"
DEL_MAPS_DEST = "Del%20International%20Hospital%2C%2065%2F67%20Nii%20Sai%20Street%2C%20East%20Legon%2C%20Accra%2C%20Ghana"


# ---------------------------------------------------------------- placeholders
def _esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


_GRADS = [("#0e5aa8", "#082a56"), ("#0b4a8f", "#0a2a52"),
          ("#1460b0", "#0a3570"), ("#0d4f92", "#071f3d")]


def ph(title, sub, w, h, variant=0):
    """Navy placeholder image as a data-URI SVG."""
    g1, g2 = _GRADS[variant % len(_GRADS)]
    cx, cy = w // 2, int(h * 0.30)
    r = max(18, int(h * 0.085))
    tfs = max(20, min(46, w // 26))
    sfs = max(13, tfs // 2)
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/>'
        '</linearGradient></defs>'
        '<rect width="{w}" height="{h}" fill="url(#g)"/>'
        '<circle cx="{cx}" cy="{cy}" r="{r2}" fill="rgba(255,255,255,0.13)"/>'
        '<rect x="{x1}" y="{y1}" width="{s}" height="{s2}" rx="4" fill="#ffffff"/>'
        '<rect x="{x2}" y="{y2}" width="{s2}" height="{s}" rx="4" fill="#ffffff"/>'
        '<text x="50%" y="{ty}%" text-anchor="middle" font-family="Georgia, serif" '
        'font-size="{tfs}" font-weight="600" fill="#ffffff">{title}</text>'
        '<text x="50%" y="{sy}%" text-anchor="middle" font-family="Arial, sans-serif" '
        'font-size="{sfs}" fill="rgba(255,255,255,0.82)">{sub}</text>'
        '</svg>'
    ).format(w=w, h=h, g1=g1, g2=g2, cx=cx, cy=cy, r2=r + 26,
             x1=cx - 5, y1=cy - r, s=10, s2=r * 2,
             x2=cx - r, y2=cy - 5,
             ty=62, sy=72, tfs=tfs, sfs=sfs,
             title=_esc(title), sub=_esc(sub))
    return "data:image/svg+xml," + urllib.parse.quote(svg, safe="")


def logo_svg():
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="160" viewBox="0 0 200 160">'
        '<rect x="6" y="6" width="188" height="148" rx="28" fill="#0b4a8f"/>'
        '<rect x="6" y="6" width="188" height="148" rx="28" fill="none" stroke="#d9a441" stroke-width="4"/>'
        '<text x="100" y="112" text-anchor="middle" font-family="Georgia, serif" '
        'font-size="92" font-weight="700" fill="#ffffff">D</text></svg>'
    )
    return "data:image/svg+xml," + urllib.parse.quote(svg, safe="")


def map_svg():
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="380" viewBox="0 0 640 380">'
        '<rect width="640" height="380" fill="#e8eef6"/>'
        '<rect x="0" y="60" width="640" height="90" fill="#dce6f2"/>'
        '<rect x="0" y="230" width="640" height="70" fill="#dce6f2"/>'
        '<g stroke="#ffffff" stroke-width="16"><path d="M0 105 H640"/><path d="M0 265 H640"/>'
        '<path d="M150 0 V380"/><path d="M330 0 V380"/><path d="M510 0 V380"/></g>'
        '<g stroke="#ffffff" stroke-width="8"><path d="M0 190 H640"/></g>'
        '<rect x="360" y="120" width="120" height="55" rx="8" fill="#cfe3d4"/>'
        '<circle cx="330" cy="190" r="26" fill="#0b4a8f"/>'
        '<circle cx="330" cy="190" r="26" fill="none" stroke="#d9a441" stroke-width="4"/>'
        '<text x="330" y="199" text-anchor="middle" font-family="Georgia, serif" '
        'font-size="26" font-weight="700" fill="#ffffff">D</text>'
        '<text x="330" y="252" text-anchor="middle" font-family="Arial, sans-serif" '
        'font-size="21" font-weight="700" fill="#071f3d">Del International Hospital</text>'
        '<text x="330" y="280" text-anchor="middle" font-family="Arial, sans-serif" '
        'font-size="16" fill="#5a6b7a">East Legon, Accra</text></svg>'
    )
    return "data:image/svg+xml," + urllib.parse.quote(svg, safe="")


LOGO = logo_svg()
MAP_IMG = map_svg()


# ---------------------------------------------------------------- Del services
# Each entry: name, blurb (grid card), tag, about (2 paras), helps (6),
# who, know, photos (3 PH keys).
SERVICES = [
    {
        "name": "Fertility Centre",
        "blurb": "IVF, ICSI and IUI, donor programmes and surrogacy — helping couples become parents.",
        "tag": "IVF, ICSI and IUI, donor programmes and surrogacy — helping couples in Ghana and beyond become parents.",
        "about": [
            "Our fertility centre is the reproductive medicine division of Del International Hospital, backed by a full-service hospital — so if a pregnancy needs specialist care, cardiology, internal medicine, surgery, paediatrics and critical care are all in the same building.",
            "We treat couples with conception difficulties using modern assisted reproduction: IVF, ICSI and IUI, donor egg and sperm programmes, embryo donation and surrogacy. Our published records show 23 successful conceptions from 39 fertilisations in a single year — a result that reflects a careful, experienced embryology programme.",
        ],
        "helps": [
            "In vitro fertilisation (IVF)",
            "ICSI — sperm injected directly into the egg",
            "Intrauterine insemination (IUI)",
            "Donor egg and donor sperm programmes",
            "Embryo donation and frozen embryo transfer",
            "Surrogacy and fertility counselling",
        ],
        "who": "Couples who have been trying to conceive without success, and patients referred for fertility assessment — from Ghana and from abroad.",
        "know": "Bring any previous fertility test results and a list of medicines you take. The first visit is a consultation and assessment — your specialist will explain the options and the likely costs before any treatment begins.",
        "photos": ["fertility1", "fertility2", "fertility3"],
    },
    {
        "name": "Internal Medicine",
        "blurb": "Diagnosis and long-term care for adults, including diabetes, hypertension and other chronic conditions.",
        "tag": "Diagnosis and long-term care for adults — from a first worrying symptom to living well with a long-term condition.",
        "about": [
            "Internal medicine is the hospital's adult medicine service. Our physicians take time to listen, examine you and, where needed, arrange tests in our own laboratory and imaging department, so the cause of a problem is found rather than guessed at.",
            "Many of our patients live with long-term conditions such as diabetes and high blood pressure. We help you understand your condition, agree a treatment plan you can keep to, and review you regularly so small changes are caught early.",
        ],
        "helps": [
            "Diabetes care and regular reviews",
            "High blood pressure (hypertension)",
            "Heart, lung and stomach problems",
            "Fevers and infections that keep coming back",
            "Unexplained tiredness, weight change or pain",
            "Referrals to our surgeons and other specialists when you need them",
        ],
        "who": "Adults and older teenagers with new symptoms, ongoing illness, or a long-term condition that needs regular review.",
        "know": "Bring a list of medicines you are taking and any previous test results. If your doctor orders blood tests or a scan, both are done here at the hospital.",
        "photos": ["internal1", "internal2", "internal3"],
    },
    {
        "name": "Paediatrics",
        "blurb": "Gentle, attentive care for babies, children and teenagers — from check-ups to acute illness.",
        "tag": "Gentle, attentive care for babies, children and teenagers — from routine check-ups to acute illness.",
        "about": [
            "Children are not just small adults, and our paediatric team treats them that way. We examine gently, explain what is happening in words children and parents can follow, and involve you in every decision about your child's care.",
            "From newborn checks and childhood illnesses to injuries and worries about growth or development, we see children quickly — and because the hospital is open 24/7, a sick child can be seen at any hour.",
        ],
        "helps": [
            "Fevers, coughs, malaria and other childhood infections",
            "Stomach upsets, vomiting and dehydration",
            "Newborn and baby check-ups",
            "Growth and development monitoring",
            "Asthma and breathing problems",
            "Advice on feeding, sleep and immunisation",
        ],
        "who": "Babies, children and teenagers — and parents who want clear answers about their child's health.",
        "know": "Bring your child's health record or weighing card if you have one. In an emergency, come straight in — no appointment needed.",
        "photos": ["paeds", "paeds2", "paeds3"],
    },
    {
        "name": "Obstetrics & Gynaecology",
        "blurb": "Antenatal care, safe delivery and women’s health at every stage of life.",
        "tag": "Antenatal care, safe delivery and women's health at every stage of life.",
        "about": [
            "Our obstetrics team cares for mothers through pregnancy, birth and the weeks after delivery. Antenatal visits track your health and your baby's growth, with ultrasound and laboratory tests available on site, so concerns are picked up early.",
            "Our gynaecology service covers women's health beyond pregnancy — from painful or irregular periods and infections to screening and family planning advice — always with privacy and respect.",
        ],
        "helps": [
            "Antenatal (pregnancy) care and ultrasound scans",
            "Safe delivery, with surgical support if a caesarean is needed",
            "Postnatal checks for mother and baby",
            "Cervical screening",
            "Family planning advice",
            "Period problems, pelvic pain and infections",
        ],
        "who": "Expectant mothers, women planning a pregnancy, and women of all ages with health concerns they want checked in confidence.",
        "know": "Cervical screening is available — ask about it when you book. For antenatal booking, come with any previous pregnancy records if you have them.",
        "photos": ["maternity", "maternity2", "maternity3"],
    },
    {
        "name": "General Surgery",
        "blurb": "Planned and emergency surgical procedures with experienced surgeons and anaesthetists.",
        "tag": "Planned and emergency operations by experienced surgeons and anaesthetists, with careful recovery care on the ward.",
        "about": [
            "Our surgical team performs a wide range of planned and emergency operations. Before any procedure, your surgeon explains what is wrong, what the operation involves and what recovery will look like, so you can decide with full information.",
            "Anaesthesia is led by experienced consultant anaesthetists, and after your operation our nurses care for you on the ward until you are ready to go home.",
        ],
        "helps": [
            "Hernia repair",
            "Appendix removal (appendicectomy)",
            "Gallbladder and abdominal surgery",
            "Lumps, cysts and abscesses",
            "Emergency surgery for acute abdominal pain",
            "Wound care and follow-up reviews",
        ],
        "who": "Anyone whose doctor has recommended an operation, and patients with sudden severe pain or injuries that may need surgery.",
        "know": "Some operations need scans or blood tests first — both are done here. If you are told to fast before surgery, please follow the instructions exactly.",
        "photos": ["surgery", "surgery2", "surgery3"],
    },
    {
        "name": "Emergency & Critical Care",
        "blurb": "Round-the-clock emergency response, with specialists on call 24 hours a day.",
        "tag": "Round-the-clock emergency response and intensive care for the seriously ill, with specialists on call 24 hours a day.",
        "about": [
            "Our emergency team is on duty day and night. When you arrive, we assess you immediately, stabilise breathing and circulation, and call in the specialists you need — medicine, surgery, anaesthesia or paediatrics.",
            "Patients who are seriously ill receive critical care in our ICU, with close monitoring and consultant input.",
        ],
        "helps": [
            "Difficulty breathing and severe asthma",
            "Collapse, seizures and unconsciousness",
            "Road accident and other serious injuries",
            "Chest pain and suspected heart problems",
            "Severe infections and dehydration",
            "Stabilising patients for surgery or specialist care",
        ],
        "who": "Anyone with a sudden, severe or life-threatening problem — at any hour. In an emergency, come straight in; no appointment is needed.",
        "know": "Call ahead on 030 254 3256 if you can, so the team is ready when you arrive. Bring any medicines the patient is taking and previous medical records.",
        "photos": ["emergency1", "emergency2", "emergency3"],
    },
    {
        "name": "Dental Services",
        "blurb": "Check-ups, cleaning, fillings, extractions and other dental treatment.",
        "tag": "Check-ups, cleaning, fillings, extractions and other dental treatment — for healthy teeth and a confident smile.",
        "about": [
            "Our dental clinic treats toothache and decay, cares for your gums and helps you keep your natural teeth for life. We explain what each treatment involves and what it will feel like before we begin.",
            "Regular check-ups catch small problems — a tiny cavity, early gum disease — while they are still simple and less costly to fix.",
        ],
        "helps": [
            "Dental check-ups and professional cleaning",
            "Fillings for decayed teeth",
            "Tooth extraction, including painful wisdom teeth",
            "Toothache and dental abscesses",
            "Gum disease treatment",
            "Dental advice for children and adults",
        ],
        "who": "Adults and children — anyone with tooth pain, a broken or decayed tooth, bleeding gums, or who is simply due a check-up.",
        "know": "Dental pain with swelling of the face, or difficulty opening your mouth, needs same-day care — call us or come in.",
        "photos": ["dental", "dental2", "dental3"],
    },
    {
        "name": "Counselling",
        "blurb": "Confidential support for the fertility journey, stress and everyday pressures.",
        "tag": "Confidential counselling for the fertility journey, pregnancy and the pressures of everyday life.",
        "about": [
            "Counselling at Del is a private, judgement-free space to talk — whether you are on a fertility journey, coping with a difficult diagnosis, or carrying the pressure of everyday life.",
            "Sessions are confidential. Together with your counsellor, you will understand what you are facing and build practical steps toward feeling steadier, at a pace that suits you.",
        ],
        "helps": [
            "Support through fertility treatment and waiting",
            "Coping with pregnancy loss or a difficult diagnosis",
            "Stress and burnout",
            "Anxiety and persistent worry",
            "Low mood",
            "Family and relationship difficulties",
        ],
        "who": "Anyone who feels they need someone to talk to — you do not need a referral or a diagnosis to book.",
        "know": "What you discuss stays confidential. If talking feels hard at first, that is normal — the first session is mostly listening.",
        "photos": ["counsel1", "counsel2", "counsel3"],
    },
    {
        "name": "Pharmacy",
        "blurb": "A 24-hour on-site pharmacy — collect your medicines before you leave.",
        "tag": "A 24-hour on-site pharmacy, so you can collect your prescribed medicines before you leave — with clear advice on how to take them.",
        "about": [
            "Our pharmacy is inside the hospital, steps from the consulting rooms, and open 24 hours. After your appointment you can collect your prescribed medicines straight away — no separate trip across town.",
            "Our pharmacists check every prescription, explain how and when to take your medicine, and answer questions about side effects or medicines you are already taking.",
        ],
        "helps": [
            "Dispensing prescribed medicines after your visit",
            "Advice on how to take your medicine safely",
            "Checking that medicines are safe to take together",
            "Refills for long-term conditions like diabetes and hypertension",
            "Open 24 hours, every day",
            "Storage and expiry guidance",
        ],
        "who": "Every patient with a prescription — and anyone on long-term medication who wants their medicines reviewed.",
        "know": "Bring your prescription and a list of any other medicines you take, including herbal ones, so the pharmacist can check they are safe together.",
        "photos": ["pharmacy1", "pharmacy2", "pharmacy3"],
    },
    {
        "name": "Medical Laboratory",
        "blurb": "Accurate blood, urine and other laboratory tests with prompt results.",
        "tag": "Accurate blood, urine and other laboratory tests, with prompt results your doctor can act on.",
        "about": [
            "Good treatment starts with the right diagnosis. Our laboratory scientists run a wide range of tests on blood, urine and other samples, following careful quality procedures so your doctor can trust the result.",
            "Because the laboratory is here in the hospital, results come back quickly — often the same day — and go straight to your care team.",
        ],
        "helps": [
            "Full blood count and malaria tests",
            "Blood sugar and diabetes monitoring",
            "Liver and kidney function tests",
            "Pregnancy tests",
            "Urine and stool examinations",
            "Pre-surgery and antenatal test panels",
        ],
        "who": "Patients whose doctor has ordered tests, expectant mothers doing antenatal panels, and anyone preparing for surgery.",
        "know": "Some blood tests need you to fast — your doctor or the laboratory will tell you if yours does. Bring your request form if you were given one. The laboratory is open 8:00 AM – 8:00 PM.",
        "photos": ["lab1", "lab2", "lab3"],
    },
    {
        "name": "Diagnostic Imaging",
        "blurb": "Ultrasound, X-ray and fluoroscopy, with ECG, by skilled radiographers.",
        "tag": "Ultrasound, X-ray and fluoroscopy, with ECG — clear pictures that guide your treatment.",
        "about": [
            "Our imaging department offers ultrasound, X-ray and fluoroscopy, performed by skilled radiographers — the pictures your doctor needs to see inside the body without surgery.",
            "Imaging supports almost every other service here — from emergency care and surgery planning to pregnancy scans — and results are reported promptly to your doctor.",
        ],
        "helps": [
            "Pregnancy (obstetric) ultrasound",
            "Ultrasound of the abdomen, pelvis and other organs",
            "X-ray of the chest, limbs and spine",
            "Fluoroscopy for moving, real-time images",
            "ECG — a tracing of the heart",
            "Results reported promptly to your doctor",
        ],
        "who": "Anyone whose doctor needs a clearer picture — expectant mothers, patients with unexplained pain, and people preparing for surgery.",
        "know": "For some scans, call ahead so we can prepare — a few need you to fast or drink water beforehand, and we will explain when you book.",
        "photos": ["imaging1", "imaging2", "imaging3"],
    },
    {
        "name": "Physiotherapy",
        "blurb": "Rehabilitation after injury, surgery or stroke — and massage for pain and stiffness.",
        "tag": "Rehabilitation and pain relief after injury, surgery or stroke — helping you move again, with confidence.",
        "about": [
            "Our physiotherapy team helps you recover movement and strength after injury, surgery or illness, with a treatment plan built around your body and your goals.",
            "Sessions combine hands-on treatment, guided exercise and advice you can follow at home — and our massage unit helps ease pain and stiffness alongside your programme.",
        ],
        "helps": [
            "Back, neck and joint pain",
            "Recovery after surgery or a fracture",
            "Stroke rehabilitation",
            "Sports injuries",
            "Massage for pain and stiffness",
            "Exercises and advice to prevent the problem coming back",
        ],
        "who": "Anyone recovering from injury or surgery, living with back or joint pain, or rebuilding strength after a stroke.",
        "know": "Wear comfortable clothes you can move in. Bring any scans or referral letters from your doctor.",
        "photos": ["physio1", "physio2", "physio3"],
    },
    {
        "name": "Dietetics",
        "blurb": "Practical nutrition advice for diabetes, weight, pregnancy and recovery.",
        "tag": "Practical nutrition advice for diabetes, weight, pregnancy and recovery — food as part of your treatment.",
        "about": [
            "Our dietetics service gives you a food plan that fits your life — not a lecture. Your dietitian looks at your health, your medicines and the food you actually eat, then agrees changes you can keep.",
            "Good nutrition supports almost every treatment we give — from controlling blood sugar to recovering after surgery and eating well through pregnancy.",
        ],
        "helps": [
            "Diabetes and blood sugar control through food",
            "Healthy weight loss and weight gain",
            "Nutrition in pregnancy and breastfeeding",
            "Food plans for high blood pressure and heart health",
            "Eating well after surgery or illness",
            "Advice for children and older people",
        ],
        "who": "Anyone whose doctor has advised a change in diet, people living with diabetes or high blood pressure, and expectant mothers.",
        "know": "Bring a list of your medicines and, if you can, a note of what you usually eat in a day — it helps your dietitian give advice that fits your life.",
        "photos": ["diet1", "diet2", "diet3"],
    },
    {
        "name": "Preventive Healthcare",
        "blurb": "Screening, health education and early detection to keep you and your family well.",
        "tag": "Screening, health education and early detection — because preventing illness beats treating it.",
        "about": [
            "Preventive healthcare is about staying well: regular screening finds problems like high blood pressure, diabetes and early cervical changes early, when they are easiest to treat.",
            "Our team also gives practical health education for families across Accra — on nutrition, hygiene, and the warning signs that should never be ignored.",
        ],
        "helps": [
            "Cervical screening",
            "Blood pressure and diabetes screening",
            "General health check-ups",
            "Breast checks and screening advice",
            "Immunisation advice",
            "Health education for families and communities",
        ],
        "who": "Everyone — especially adults over 30, women due cervical or breast screening, and families who want a regular health check.",
        "know": "Cervical screening is available — ask about it when you book. A check-up is quickest when you bring any previous results you have.",
        "photos": ["preventive1", "preventive2", "preventive3"],
    },
]

# Photo gallery entries: key -> (alt, caption). src is a placeholder built from caption.
PH = {
    "fertility1": ("A fertility specialist talking with a couple during a consultation",
                   "Your first consultation — honest answers about your options"),
    "fertility2": ("An embryologist working in the fertility laboratory",
                   "Careful laboratory work behind every treatment"),
    "fertility3": ("A smiling mother holding her newborn baby",
                   "The result we work for"),
    "internal1": ("A physician checking the blood pressure of a patient in a consulting room",
                  "Blood pressure and long-term condition checks"),
    "internal2": ("A doctor reviewing test results on a screen together with a patient",
                  "Reviewing your results together, in plain language"),
    "internal3": ("A physician listening to the chest of a patient during a ward round",
                  "Daily ward rounds for patients in our care"),
    "paeds": ("A doctor listening to a smiling young child's chest while his mother sits beside him",
              "A children's check-up, with mum close by"),
    "paeds2": ("A nurse measuring the height of a young child at a growth chart while his mother watches",
               "Growth checks at children's visits"),
    "paeds3": ("A doctor gently examining a baby while the mother holds the hand of the baby",
               "Gentle baby examinations, with mum close by"),
    "maternity": ("A midwife checking a smiling pregnant mother, with an ultrasound machine behind her",
                  "An antenatal check, with ultrasound on hand"),
    "maternity2": ("A new mother holding her newborn baby in the maternity ward, with a midwife beside her",
                   "First moments with your baby, on the maternity ward"),
    "maternity3": ("A midwife weighing a newborn baby on a baby scale while the mother watches",
                   "The first checks for your baby, done gently"),
    "surgery": ("A surgical team in theatre scrubs operating under bright surgical lights",
                "Inside the operating theatre during a planned operation"),
    "surgery2": ("A nurse caring for a patient recovering in a hospital bed after surgery",
                 "Careful recovery care on the ward after your operation"),
    "surgery3": ("The gloved hands of a surgical team working together under operating lights",
                 "Experienced hands in theatre"),
    "emergency1": ("The emergency team working together around a patient, with monitors and a drip in place",
                   "The emergency team at work, day and night"),
    "emergency2": ("A nurse checking the monitors and drip of a patient in critical care",
                   "Close monitoring in critical care"),
    "emergency3": ("Paramedics wheeling a patient on a stretcher into the emergency department",
                   "Straight in — no appointment needed in an emergency"),
    "dental": ("A dentist in scrubs examining a patient reclined in the dental chair",
               "Treatment in the dental clinic"),
    "dental2": ("A smiling child in the dental chair giving a thumbs up beside the dentist",
                "Friendly visits that help children relax"),
    "dental3": ("The clean, modern dental treatment room with the chair and equipment ready",
                "Our dental treatment room, ready for you"),
    "counsel1": ("A counsellor listening attentively during a private session",
                 "A private space to talk, at your own pace"),
    "counsel2": ("A calm, comfortable counselling room with two armchairs by a window",
                 "Our counselling room — calm and confidential"),
    "counsel3": ("A counsellor talking gently with a couple during a family session",
                 "Support for couples and families"),
    "pharmacy1": ("A pharmacist handing medicine to a patient across the pharmacy counter",
                  "Collect your medicine before you leave"),
    "pharmacy2": ("Shelves of medicines in the hospital pharmacy, with a pharmacist checking stock",
                  "Well-stocked shelves, checked daily"),
    "pharmacy3": ("A pharmacist checking a prescription carefully at a computer",
                  "Every prescription checked before it is dispensed"),
    "lab1": ("A laboratory scientist looking through a microscope at a sample, with test tubes beside her",
             "Samples examined carefully in our laboratory"),
    "lab2": ("A laboratory scientist loading samples into an automated analyser machine",
             "Modern analysers for fast, accurate results"),
    "lab3": ("A nurse taking a blood sample from the arm of a seated patient",
             "Blood samples taken gently, here at the hospital"),
    "imaging1": ("A radiographer positioning a patient for an X-ray",
                 "X-ray, done here at the hospital"),
    "imaging2": ("An ultrasound scan in progress, with the image on screen",
                 "Ultrasound scans by skilled radiographers"),
    "imaging3": ("A sonographer performing an ultrasound scan on a patient",
                 "Ultrasound scans by skilled radiographers"),
    "physio1": ("A physiotherapist guiding a patient through an exercise",
                "Guided exercise, built around you"),
    "physio2": ("Hands-on physiotherapy treatment for a painful shoulder",
                "Hands-on treatment for pain and stiffness"),
    "physio3": ("A massage therapist working on a patient's back",
                "Our massage unit — easing pain and stiffness"),
    "diet1": ("A dietitian talking through a food plan with a patient",
              "A food plan that fits your life"),
    "diet2": ("Fresh fruit, vegetables and grains on a table",
              "Good food, as part of your treatment"),
    "diet3": ("A dietitian checking a patient's progress at a follow-up visit",
              "Follow-up visits to keep you on track"),
    "preventive1": ("A nurse checking the blood pressure of a woman at a health screening",
                    "Screening for blood pressure and diabetes"),
    "preventive2": ("A health educator giving a talk to families at a community health session",
                    "Health education for families across Accra"),
    "preventive3": ("A nurse giving a child an immunisation while the mother holds the child",
                    "Immunisation for children, done gently"),
}

ALIASES = [
    ["Fertility Centre", ["fertility", "ivf", "icsi", "iui", "trying to get pregnant",
                          "trying for a baby", "donor egg", "donor sperm", "surrogacy",
                          "surrogate", "embryo", "conceive", "conception"]],
    ["Internal Medicine", ["internal medicine", "physician", "diabetes", "diabetic",
                           "hypertension", "blood pressure", "bp", "long-term illness", "chronic"]],
    ["Paediatrics", ["paediatric-", "pediatric-", "child", "children", "baby", "babies",
                     "infant", "toddler", "kids", "newborn"]],
    ["Obstetrics & Gynaecology", ["obstetric-", "gynae-", "pregnan-", "antenatal", "maternity",
                                   "delivery", "give birth", "women's health", "womens health",
                                   "period problem", "family planning", "caesarean", "cesarean"]],
    ["General Surgery", ["surgery", "surgical", "operation", "operate", "hernia", "appendix", "surgeon"]],
    ["Emergency & Critical Care", ["critical care", "intensive care", "icu"]],
    ["Dental Services", ["dental", "dentist", "tooth", "teeth", "toothache"]],
    ["Counselling", ["counselling", "counseling", "counsell-", "counsel-", "mental health",
                     "stress", "depress-", "anxiety", "psychology", "psychologist"]],
    ["Pharmacy", ["pharmacy", "pharmacist", "prescription", "medication", "medicines", "medicine", "refill"]],
    ["Medical Laboratory", ["laboratory", "lab", "blood test", "test result", "sample", "urine test"]],
    ["Diagnostic Imaging", ["imaging", "scan", "x-ray", "xray", "ultrasound", "radiograph-"]],
    ["Physiotherapy", ["physiotherapy", "physio", "rehabilitation", "rehab", "back pain",
                       "massage", "stroke rehab"]],
    ["Dietetics", ["diet", "dietitian", "dietician", "nutrition", "nutritionist", "weight loss"]],
    ["Preventive Healthcare", ["preventive", "check-up", "checkup", "check up", "vaccin-",
                               "immunis-", "immuniz-", "health screening", "health check"]],
]

# "Our story" gallery (user, 2026-11-21): keep only the Maternity ward and
# Fertility centre pictures, remove the rest, and add Del's real photos.
SLIDES = [
    {"label": "Maternity ward",
     "alt": "A new mother holding her newborn baby in the maternity ward"},
    {"label": "Fertility centre",
     "alt": "A fertility specialist talking with a couple during a consultation"},
    {"label": "Reception",
     "alt": "The reception entrance at Del International Hospital"},
    {"label": "Our team",
     "alt": "The Del International Hospital team together outside the hospital"},
    {"label": "Waiting area",
     "alt": "The waiting area at Del International Hospital"},
    {"label": "Our sign",
     "alt": "The Del International Hospital signboard in East Legon, Accra"},
]

GO_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def svc_card(i, svc):
    n = i + 1
    thumb = _photo_uri("services", svc["photos"][0])
    alt = PH[svc["photos"][0]][0]
    name = svc["name"].replace("&", "&amp;")
    return (
        '<button type="button" class="svc-card" data-service="{name}">'
        '<img class="svc-thumb" src="{thumb}" alt="{alt}" />'
        '<span class="svc-num">{num:02d}</span><h3>{name}</h3><p>{blurb}</p>'
        '<span class="go">Learn more {go}</span></button>'
    ).format(name=name, thumb=thumb, alt=_esc(alt), num=n,
             blurb=svc["blurb"], go=GO_SVG)


# Patient reviews (user, 2026-11-21): five-star reviews on the home page,
# after the About teaser. SAMPLE reviews — Del's real patient words should
# replace them before the site goes live.
REVIEWS_SECTION = (
    '  <section class="block wrap">\n'
    '    <p class="eyebrow">Patient reviews</p>\n'
    '    <h2>What our patients say.</h2>\n'
    '    <p class="intro">Here is what patients and families say about their care at Del.</p>\n'
    '    <div class="reviews-grid">\n'
    '      <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cThe nurses were so kind and the ward was very clean. I felt safe the whole time I was there.\u201d</p><p class="review-name">Ama S. \u2014 Maternity patient</p></article>\n'
    '      <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cThe fertility team explained everything clearly and answered all our questions. We always felt supported.\u201d</p><p class="review-name">Kwame &amp; Akosua \u2014 Fertility centre</p></article>\n'
    '      <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cI was seen quickly and the doctor took time to listen. The whole visit was smooth from start to finish.\u201d</p><p class="review-name">Efua M. \u2014 Outpatient</p></article>\n'
    '    </div>\n'
    '  </section>'
)

# Reviews in the contact page's left column, under the form (user, 2026-11-21).
# Same sample reviews as the home/about sections, stacked vertically.
# The third review lives in the contact page's RIGHT column, under the map
# card (user, 2026-11-21): it fills the empty space there and balances the
# two columns. Same sample review as the other sections.
CONTACT_REVIEW_RIGHT = (
    '      <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cI was seen quickly and the doctor took time to listen. The whole visit was smooth from start to finish.\u201d</p><p class="review-name">Efua M. \u2014 Outpatient</p></article>'
)

CONTACT_REVIEWS = (
    '      <div class="contact-reviews">\n'
    '        <p class="eyebrow">Patient reviews</p>\n'
    '        <h3>What our patients say.</h3>\n'
    '        <div class="reviews-stack">\n'
    '          <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cThe nurses were so kind and the ward was very clean. I felt safe the whole time I was there.\u201d</p><p class="review-name">Ama S. \u2014 Maternity patient</p></article>\n'
    '          <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cThe fertility team explained everything clearly and answered all our questions. We always felt supported.\u201d</p><p class="review-name">Kwame &amp; Akosua \u2014 Fertility centre</p></article>\n'
    '        </div>\n'
    '      </div>'
)

# Del overrides (2026-11-21), appended last in the stylesheet so they win:
# (a) restore the 24px side padding on every .block.wrap section — the
#     original .block{padding:72px 0} rule was wiping it out, so text sat
#     right on the left edge of the screen on every page;
# (b) shrink the chat button to a logo-only circle;
# (c) style the patient-reviews grid.
DEL_CSS_OVERRIDES = (
    '  /* Del overrides (2026-11-21) */\n'
    '  .wrap.block, section.wrap:not(.band){padding-left:24px;padding-right:24px}\n'
    '  .chat-fab{width:56px;height:56px;padding:0;border-radius:50%;justify-content:center}\n'
    '  .chat-fab .fab-logo{width:40px;height:40px}\n'
    '  .reviews-grid{display:grid;gap:16px;margin-top:36px;grid-template-columns:1fr}\n'
    '  @media(min-width:720px){.reviews-grid{grid-template-columns:repeat(3,1fr)}}\n'
    '  .review-card .stars{color:var(--accent);font-size:1.15rem;letter-spacing:.15em;margin-top:0}\n'
    '  .review-card .review-name{font-weight:700;color:var(--teal-ink);margin-top:14px}\n'
    '  .mission-grid{display:grid;gap:20px 32px;margin:28px 0 44px;grid-template-columns:1fr}\n'
    '  @media(min-width:720px){.mission-grid{grid-template-columns:1fr 1fr}}\n'
    '  .mission-grid h3{font-size:1.35rem;color:var(--teal-ink);margin:0 0 8px}\n'
    '  .mission-grid p{color:var(--muted);font-size:1.02rem;line-height:1.6;margin:0}\n'
    '  .contact-reviews{margin-top:48px}\n'
    '  .contact-reviews h3{font-size:1.35rem;color:var(--teal-ink);margin:0 0 16px}\n'
    '  .reviews-stack{display:grid;gap:16px}\n'
    '  /* Pop-in on load and on scroll (2026-11-21). The animation runs once\n'
    '     per element (fill backwards so the delay period stays hidden); after\n'
    '     it ends the element keeps its own styles, so hover lifts still work. */\n'
    '  .pop{opacity:0}\n'
    '  .pop.in{opacity:1;animation:delPopIn .7s cubic-bezier(.21,.9,.35,1.05) backwards}\n'
    '  @keyframes delPopIn{from{opacity:0;transform:translateY(28px) scale(.94)}to{opacity:1;transform:translateY(0) scale(1)}}\n'
    '  @media (prefers-reduced-motion:reduce){.pop{opacity:1}.pop.in{animation:none}}\n'
    '  /* Preview countdown timer (user, 2026-11-22): dark bar at the very\n'
    '     top, above the Open 24/7 bar. Sticky, so it stays on screen. */\n'
    '  .preview-timer{background:#1c1c1e;color:#e8e8e8;text-align:center;padding:10px 16px;font-size:.82rem;letter-spacing:.1em;display:flex;flex-wrap:wrap;gap:2px 16px;align-items:center;justify-content:center;position:sticky;top:0;z-index:1000}\n'
    '  .preview-timer .pt-label{font-weight:700;color:#f5f5f5}\n'
    '  .preview-timer .pt-count{font-weight:700;white-space:nowrap}\n'
    '  .preview-timer .pt-count b{color:#ff7a1a;font-size:1.05rem}\n'
    '  .preview-timer .pt-count i{color:#8a8a8a;font-style:normal;margin:0 3px}\n'
    '  .preview-timer .pt-count .pt-unit{color:#bdbdbd;font-weight:600}\n'
    '  .preview-timer .pt-note{color:#9a9a9a;letter-spacing:.02em}\n'
    '  /* Sticky header: the nav pins right under the timer bar. */\n'
    '  header.site{position:sticky;z-index:999}\n'
    '  /* Transparent header on scroll (user, 2026-11-22): at the top the\n'
    '     header is solid; once you scroll, its background fades to\n'
    '     see-through (soft white with a blur) so it stops covering the\n'
    '     page, while the logo, nav links and Book button stay put. */\n'
    '  header.site{transition:background .35s ease,border-color .35s ease,backdrop-filter .35s ease,-webkit-backdrop-filter .35s ease}\n'
    '  header.site.scrolled{background:rgba(247,248,250,0.45);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border-bottom-color:rgba(227,230,234,0.4)}\n'
)

# Preview countdown timer (user, 2026-11-22): same timer as the
# Al-Kawthar site. The user sends the link on Monday 2026-11-23, so
# the expiry is 7 days after that Monday (2026-11-30); on Monday the
# timer reads 07 DAYS. Change PREVIEW_EXPIRY to move it. When the
# timer reaches zero it shows 00s and says the preview has expired.
PREVIEW_EXPIRY = "2026-11-30T23:59:59+00:00"
PREVIEW_TIMER_HTML = (
    '  <div class="preview-timer" id="previewTimer" role="timer">\n'
    '    <span class="pt-label">LIVE PREVIEW EXPIRES IN</span>\n'
    '    <span class="pt-count"><b id="ptDays">07</b> <span class="pt-unit">DAYS</span> <i>:</i> <b id="ptHours">08</b> <span class="pt-unit">HRS</span> <i>:</i> <b id="ptMins">18</b> <span class="pt-unit">MIN</span> <i>:</i> <b id="ptSecs">18</b> <span class="pt-unit">SEC</span></span>\n'
    '    <span class="pt-note">Temporary preview &mdash; taken offline when the timer reaches zero.</span>\n'
    '  </div>\n'
)
PREVIEW_TIMER_JS = (
    '  <script>\n'
    '  // Preview countdown timer: counts down to PREVIEW_EXPIRY.\n'
    '  (function () {\n'
    '    var expiry = new Date("' + PREVIEW_EXPIRY + '").getTime();\n'
    '    var bar = document.getElementById("previewTimer");\n'
    '    if (!bar) return;\n'
    '    var d = document.getElementById("ptDays"), h = document.getElementById("ptHours"),\n'
    '        m = document.getElementById("ptMins"), s = document.getElementById("ptSecs"),\n'
    '        note = bar.querySelector(".pt-note");\n'
    '    function pad(n) { return (n < 10 ? "0" : "") + n; }\n'
    '    function tick() {\n'
    '      var diff = expiry - Date.now();\n'
    '      if (diff <= 0) {\n'
    '        d.textContent = "00"; h.textContent = "00"; m.textContent = "00"; s.textContent = "00";\n'
    '        note.textContent = "This preview has expired.";\n'
    '        return;\n'
    '      }\n'
    '      d.textContent = pad(Math.floor(diff / 86400000));\n'
    '      h.textContent = pad(Math.floor(diff % 86400000 / 3600000));\n'
    '      m.textContent = pad(Math.floor(diff % 3600000 / 60000));\n'
    '      s.textContent = pad(Math.floor(diff % 60000 / 1000));\n'
    '    }\n'
    '    tick();\n'
    '    setInterval(tick, 1000);\n'
    '    // Sticky header: pin the nav right under the timer bar. The timer\n'
    '    // can wrap to two lines on narrow screens, so measure its real\n'
    '    // height and set the header top offset from it, on load and resize.\n'
    '    var header = document.querySelector("header.site");\n'
    '    function stickHeader() {\n'
    '      if (!header) return;\n'
    '      header.style.top = bar.offsetHeight + "px";\n'
    '    }\n'
    '    stickHeader();\n'
    '    window.addEventListener("load", stickHeader);\n'
    '    window.addEventListener("resize", stickHeader);\n'
    '    // Transparent header on scroll (user, 2026-11-22): when the page\n'
    '    // is scrolled the header background fades to see-through so it\n'
    '    // stops covering the page, but the logo, nav links and Book\n'
    '    // button stay visible and clickable. At the top it is solid.\n'
    '    function headerFade() {\n'
    '      if (!header) return;\n'
    '      header.classList.toggle("scrolled", window.scrollY > 8);\n'
    '    }\n'
    '    headerFade();\n'
    '    window.addEventListener("scroll", headerFade, { passive: true });\n'
    '  })();\n'
    '  </script>\n'
)

# Pop-in animation script (user, 2026-11-21): cards, stats, photos and list
# items pop in gently when the page loads and when you scroll to them.
POP_IN_JS = (
    '  <script>\n'
    '  // Pop-in on load and on scroll.\n'
    '  (function(){\n'
    '    var els = document.querySelectorAll(".svc-card, .value-card, .stat, .teaser img, .carousel, .why-list li, .mission-grid > div, .block h2, .block .eyebrow, .block .intro, .band-inner, .card, .find-panel, .foot-grid, .contact-reviews");\n'
    '    els.forEach(function(el){\n'
    '      el.classList.add("pop");\n'
    '      var i = Array.prototype.indexOf.call(el.parentElement.children, el);\n'
    '      el.style.animationDelay = Math.min(i, 5) * 70 + "ms";\n'
    '    });\n'
    '    function showAll(){ els.forEach(function(el){ el.classList.add("in"); }); }\n'
    '    if(!("IntersectionObserver" in window)){ showAll(); return; }\n'
    '    var io = new IntersectionObserver(function(entries){\n'
    '      entries.forEach(function(en){\n'
    '        if(en.isIntersecting){ en.target.classList.add("in"); io.unobserve(en.target); }\n'
    '      });\n'
    '    }, {threshold: 0.12});\n'
    '    els.forEach(function(el){ io.observe(el); });\n'
    '  })();\n'
    '  </script>\n'
)

# Mission + Vision (user, 2026-11-21): short, simple wording based on the
# reference text he sent; Del can adjust the exact words.
MISSION_VISION_HTML = (
    '      <div class="mission-grid">\n'
    '        <div><h3>Our Mission</h3><p>To give every patient safe, personal and professional care, healing mind, body and soul.</p></div>\n'
    '        <div><h3>Our Vision</h3><p>To be the hospital of choice in Accra, trusted for quality care that transforms lives.</p></div>\n'
    '      </div>\n'
)

# ---------------------------------------------------------------- transform
def js_services():
    out = []
    for svc in SERVICES:
        entry = {k: svc[k] for k in
                 ("name", "tag", "about", "helps", "who", "know", "photos")}
        out.append("    " + json.dumps(entry, ensure_ascii=False))
    return "  var SERVICES = [\n" + ",\n".join(out) + "\n  ];"


def js_ph():
    out = []
    for i, (key, (alt, caption)) in enumerate(PH.items()):
        src = _photo_uri("services", key)
        out.append('    {key}: [{src}, {alt}, {cap}]'.format(
            key=key, src=json.dumps(src, ensure_ascii=False),
            alt=json.dumps(alt, ensure_ascii=False),
            cap=json.dumps(caption, ensure_ascii=False)))
    return "  var PH = {\n" + ",\n".join(out) + "\n  };"


def _photo_uri(subdir, key):
    return _data_uri(HERE / "del-photos" / subdir / (key + ".jpg"))


_SLIDE_PHOTOS = {
    "Reception": ("slides", "reception-real"),
    "Maternity ward": ("slides", "maternity"),
    "Fertility centre": ("services", "fertility1"),
    "Our team": ("slides", "team-real"),
    "Waiting area": ("slides", "waiting-real"),
    "Our sign": ("slides", "billboard-real"),
}


def js_slides():
    out = []
    for i, s in enumerate(SLIDES):
        if s["label"] == "Our hospital":
            src = DEL_BUILDING_IMG
        else:
            subdir, key = _SLIDE_PHOTOS[s["label"]]
            src = _photo_uri(subdir, key)
        out.append('    {{ src: {src}, label: {lab}, alt: {alt} }}'.format(
            src=json.dumps(src, ensure_ascii=False),
            lab=json.dumps(s["label"], ensure_ascii=False),
            alt=json.dumps(s["alt"], ensure_ascii=False)))
    return "  var SLIDES = [\n" + ",\n".join(out) + "\n  ];"


def js_aliases():
    return ("  var SERVICE_ALIASES = " +
            json.dumps(ALIASES, ensure_ascii=False) + ";")


def js_hero_slides():
    return ("  var HERO_SLIDES = [\n"
            '    { label: "East Legon, Accra" },\n'
            '    { label: "Specialist care" },\n'
            '    { label: "Our hospital" }\n  ];')


def replace_img_by_alt(s, alt_part, new_src, new_alt=None):
    """Replace the src (and optionally alt) of the <img> whose alt contains alt_part."""
    def repl(m):
        tag = m.group(0)
        tag = re.sub(r'src="[^"]*"', 'src="' + new_src + '"', tag, count=1)
        if new_alt is not None:
            tag = re.sub(r'alt="[^"]*"', 'alt="' + _esc(new_alt) + '"', tag, count=1)
        return tag
    pat = re.compile(r'<img[^>]*alt="[^"]*' + re.escape(alt_part) + r'[^"]*"[^>]*>')
    s2, n = pat.subn(repl, s)
    if n == 0:
        raise ValueError("img with alt containing %r not found" % alt_part)
    return s2


def replace_img_by_id(s, el_id, new_src):
    pat = re.compile(r'(<img[^>]*id="' + re.escape(el_id) + r'"[^>]*src=")[^"]*(")')
    s2, n = pat.subn(r'\1' + new_src + r'\2', s, count=1)
    if n == 0:
        raise ValueError("img with id %r not found" % el_id)
    return s2


def sub_block(s, start_re, end_re, replacement, name):
    pat = re.compile(start_re + r'.*?' + end_re, re.DOTALL)
    s2, n = pat.subn(replacement, s, count=1)
    if n == 0:
        raise ValueError("block not found: " + name)
    return s2


def transform(s):
    # ---- 0. Preview countdown timer (user, 2026-11-22): a dark bar at
    # the very top of the page, above the Open 24/7 bar. It stays pinned
    # and the nav sticks right under it.
    if s.count('<body id="top">') != 1:
        raise ValueError("body tag not found")
    s = s.replace('<body id="top">', '<body id="top">\n' + PREVIEW_TIMER_HTML, 1)
    # ---- 1. Logos (brand-mark in header/footer, chat fab + head) ----
    s = re.sub(r'(<span class="(?:brand-mark|fab-logo|head-logo)"[^>]*><img src=")'
               r'data:image/jpeg;base64,[^"]*(")',
               r'\1' + LOGO + r'\2', s)
    # ---- 2. Hero + story carousel + section photos (by id / alt) ----
    # Real building photo where the shot is the hospital itself; placeholders
    # elsewhere (wards, lab, staff) until Del supplies real photos.
    s = replace_img_by_id(s, "heroImg", DEL_REAL_IMG)
    s = replace_img_by_id(s, "heroImg2", DOCTOR_IMG)
    # Third hero slide: the real Del building photo.
    s = re.sub(r'(<img id="heroImg2"[^>]*?/>)',
               lambda m: m.group(1) + '\n      <img id="heroImg3" src="' + DEL_BUILDING_IMG + '" alt="" />',
               s, count=1)
    s = replace_img_by_id(s, "carImg", DEL_BUILDING_IMG)
    s = replace_img_by_alt(
        s, "A Habana radiographer guiding a patient into the Siemens CT scanner",
        _photo_uri("services", "imaging1"),
        "An ultrasound scan at Del International Hospital")
    s = replace_img_by_alt(
        s, "The Siemens SOMATOM CT scanner in the imaging suite",
        _photo_uri("services", "imaging2"),
        "The imaging suite at Del International Hospital")
    s = replace_img_by_alt(
        s, "Habana Medical Service nurses and staff together on the ward",
        _photo_uri("slides", "team-real"),
        "Del International Hospital nurses and staff together on the ward")
    s = replace_img_by_alt(
        s, "Moments from the Habana Medical Service story",
        DEL_BUILDING_IMG,
        "The Del International Hospital building in East Legon")
    s = replace_img_by_alt(
        s, "The front of the Habana Medical Service building",
        DEL_BUILDING_IMG,
        "The front of the Del International Hospital building in East Legon, Accra")
    s = replace_img_by_alt(
        s, "Mini map of North Kanvilli",
        MAP_IMG, "Map of East Legon, Accra — a pin marks Del International Hospital on Nii Sai Street")

    # ---- 3. Colours: teal -> navy, amber -> gold, cream -> cool grey ----
    css_vars = [
        ("--teal:#0b6e5f", "--teal:#0b4a8f"),
        ("--teal-dark:#07473d", "--teal-dark:#0a3570"),
        ("--teal-deep:#06302a", "--teal-deep:#082a56"),
        ("--teal-ink:#052e28", "--teal-ink:#071f3d"),
        ("--teal-soft:#dff0ea", "--teal-soft:#dfe9f5"),
        ("--teal-pale:#e9f4f0", "--teal-pale:#e9f1fa"),
        ("--accent:#e79a35", "--accent:#d9a441"),
        ("--accent-dark:#c97f1d", "--accent-dark:#b9872e"),
        ("--ink:#12211d", "--ink:#12202e"),
        ("--muted:#5a6b65", "--muted:#5a6b7a"),
        ("--bg:#faf8f2", "--bg:#f7f8fa"),
        ("--line:#e3e7e1", "--line:#e3e6ea"),
        ("rgba(4,32,27", "rgba(7,31,61"),
        ("rgba(6,48,42", "rgba(8,42,86"),
        ("rgba(5,46,40", "rgba(7,31,61"),
        ("rgba(18,33,29", "rgba(15,30,55"),
        ("rgba(11,110,95", "rgba(11,74,143"),
        ("rgba(231,154,53", "rgba(217,164,65"),
        ("#0a4a3e", "#0b4a8f"),
    ]
    for old, new in css_vars:
        if old not in s:
            raise ValueError("CSS value not found: " + old)
        s = s.replace(old, new)
    # kente stripe -> navy/gold stripe
    s = re.sub(r'\.kente\{[^}]*\}',
               '.stripe{height:10px;margin-top:56px;background:linear-gradient(90deg,'
               'var(--teal-deep) 0%,var(--teal) 45%,var(--accent) 45%,var(--accent) 55%,'
               'var(--teal) 55%,var(--teal-deep) 100%)}', s, count=1)
    s = s.replace('<div class="kente" aria-hidden="true"></div>',
                  '<div class="stripe" aria-hidden="true"></div>')

    # ---- 4. Wholesale blocks ----
    # Stats
    stats = (
        '      <div class="stat"><p class="num">30 min</p><p>From Kotoka International Airport</p></div>\n'
        '      <div class="stat"><p class="num">24/7</p><p>Emergency &amp; critical care</p></div>\n'
        '      <div class="stat"><p class="num">14</p><p>Medical services</p></div>\n'
        '      <div class="stat"><p class="num">24h</p><p>Pharmacy &amp; ambulance</p></div>'
    )
    s = sub_block(s, r'<div class="stats" style="margin-top:0">\n',
                  r'\n    </div>\n  </section>',
                  '<div class="stats" style="margin-top:0">\n' + stats +
                  '\n    </div>\n  </section>', "stats")
    # Home service preview grid (first 6 services)
    home_cards = "\n      ".join(svc_card(i, svc) for i, svc in enumerate(SERVICES[:6]))
    s = sub_block(s, r'<div class="svc-grid">\n', r'\n    </div>\n  </section>',
                  '<div class="svc-grid">\n      ' + home_cards +
                  '\n    </div>\n  </section>', "home svc-grid")
    # Services page grid (all 14)
    all_cards = "\n      ".join(svc_card(i, svc) for i, svc in enumerate(SERVICES))
    s = sub_block(s, r'<div class="svc-grid" id="svcGrid">\n', r'\n    </div>\n  </section>',
                  '<div class="svc-grid" id="svcGrid">\n      ' + all_cards +
                  '\n    </div>\n  </section>', "services svc-grid")
    # Diagnostics pills (appears twice, identical)
    old_pills = (
        '            <span class="pill">CT Scan</span>\n'
        '            <span class="pill">Ultrasound</span>\n'
        '            <span class="pill">Mammography</span>\n'
        '            <span class="pill">ECG</span>\n'
        '            <span class="pill">Echocardiography</span>\n'
        '            <span class="pill">Laboratory tests</span>'
    )
    new_pills = (
        '            <span class="pill">Ultrasound</span>\n'
        '            <span class="pill">X-ray &amp; Fluoroscopy</span>\n'
        '            <span class="pill">ECG</span>\n'
        '            <span class="pill">Laboratory tests</span>'
    )
    if s.count(old_pills) != 2:
        raise ValueError("expected 2 diagnostics pill rows, found %d" % s.count(old_pills))
    s = s.replace(old_pills, new_pills)
    # Teaser body + awards list
    s = s.replace(
        '<p class="body">Founded in 2011 by Dr Thomas Winsum Anabah, a Consultant '
        'Anaesthesiologist, HMS began as a small day clinic. Today our physicians, '
        'nurses, pharmacists, laboratory scientists and radiographers work together '
        'to give every patient coordinated, compassionate care.</p>',
        '<p class="body">Del International Hospital is an ultra-modern hospital in East Legon, '
        'opposite the PH Hotel and about 30 minutes from Kotoka International Airport. '
        'Our physicians, nurses, pharmacists, laboratory scientists and radiographers '
        'work together to give every patient coordinated, compassionate care.</p>')
    s = sub_block(
        s, r'<ul class="why-list">\n', r'\n        </ul>',
        '        <ul class="why-list">\n'
        '          <li><strong>Fertility</strong><span>A dedicated fertility centre — IVF, ICSI and IUI, donor programmes and surrogacy</span></li>\n'
        '          <li><strong>24/7</strong><span>Emergency care, a 24-hour pharmacy and a 24-hour ambulance, every day of the year</span></li>\n'
        '          <li><strong>East Legon</strong><span>Private wards, two theatres, an ICU and a maternity unit in the heart of Accra</span></li>\n'
        '        </ul>', "why-list")
    # Awards section -> facilities section
    facilities = (
        '  <section class="block wrap">\n'
        '    <p class="eyebrow">Our facilities</p>\n'
        '    <h2>Everything under one roof.</h2>\n'
        '    <div class="values-grid" style="margin-top:36px">\n'
        '      <article class="value-card"><h3>Private wards</h3><p>Private, semi-private and general wards — private rooms with air conditioning, a fridge and an en-suite toilet and bathroom.</p></article>\n'
        '      <article class="value-card"><h3>Operating theatres</h3><p>Two modern theatres, plus a dedicated maternity and labour theatre.</p></article>\n'
        '      <article class="value-card"><h3>Fertility centre</h3><p>A dedicated IVF unit with its own laboratory, backed by the full hospital.</p></article>\n'
        '      <article class="value-card"><h3>Intensive care</h3><p>An ICU for seriously ill patients, with close monitoring and consultant care.</p></article>\n'
        '      <article class="value-card"><h3>24-hour pharmacy</h3><p>Collect your medicines any hour of the day or night, right inside the hospital.</p></article>\n'
        '      <article class="value-card"><h3>Laboratory &amp; imaging</h3><p>An ultra-modern laboratory, ultrasound and ECG unit, and X-ray and fluoroscopy.</p></article>\n'
        '    </div>\n'
        '    <p class="award-note">There is a canteen on the premises and a secure car park for patients and visitors.</p>\n'
        '  </section>'
    )
    s = sub_block(s, r'  <section class="block wrap">\n    <p class="eyebrow">Recognition</p>',
                  r'\n  </section>', facilities, "awards section")
    # Contact form + booking modal service selects
    contact_opts = (
        '            <option value="">Choose a service…</option>\n'
        '            <option>Book an appointment</option>\n'
        + "".join('            <option>{}</option>\n'.format(svc["name"].replace("&", "&amp;"))
                   for svc in SERVICES)
        + '            <option>General enquiry</option>'
    )
    s = sub_block(s, r'<select id="service" name="service">\n', r'\n          </select>',
                  '<select id="service" name="service">\n' + contact_opts +
                  '\n          </select>', "contact select")
    book_opts = (
        '            <option value="">Choose a service…</option>\n'
        + "".join('            <option>{}</option>\n'.format(svc["name"].replace("&", "&amp;"))
                   for svc in SERVICES).rstrip("\n")
    )
    s = sub_block(s, r'<select id="bkService" name="bkService">\n', r'\n          </select>',
                  '<select id="bkService" name="bkService">\n' + book_opts +
                  '\n          </select>', "booking select")
    # Hours table: cervical clinic row -> laboratory + pharmacy rows
    s = s.replace(
        '<tr><td>Cervical screening clinic</td><td>Fridays, 9:00 AM</td></tr>',
        '<tr><td>Laboratory</td><td>8:00 AM – 8:00 PM</td></tr>\n'
        '          <tr><td>Pharmacy</td><td>Open 24 hours</td></tr>')
    # Remove Habana social links + staff sign-in + map credit
    s = sub_block(s, r'        <div class="social-row">\n', r'\n        </div>',
                  '', "sidebar social-row")
    s = sub_block(s, r'        <div class="foot-social">\n', r'\n        </div>',
                  '', "footer social")
    s = re.sub(r'\s*<li><a class="dim" href="https://habanamedicalservice\.lovable\.app/"[^>]*>Staff sign in</a></li>',
               '', s, count=1)
    s = re.sub(r'\s*<a class="map-credit"[^>]*>[^<]*</a>', '', s, count=1)
    # JS data
    s = sub_block(s, r'  var PH = \{\n', r'\n  \};', js_ph(), "PH map")
    s = sub_block(s, r'  var SERVICES = \[\n', r'\n  \];',
                  js_services(), "SERVICES array")
    s = sub_block(s, r'  var SLIDES = \[\n', r'\n  \];', js_slides(), "SLIDES array")
    s = sub_block(s, r'  var HERO_SLIDES = \[\n', r'\n  \];',
                  js_hero_slides(), "HERO_SLIDES array")
    if 'var heroImgs = [document.getElementById("heroImg"), document.getElementById("heroImg2")];' not in s:
        raise ValueError("heroImgs array not found")
    s = s.replace('var heroImgs = [document.getElementById("heroImg"), document.getElementById("heroImg2")];',
                  'var heroImgs = [document.getElementById("heroImg"), document.getElementById("heroImg2"), document.getElementById("heroImg3")];', 1)
    s = sub_block(s, r'  var SERVICE_ALIASES = \[\n', r'\n  \];',
                  js_aliases(), "SERVICE_ALIASES array")

    # ---- 5. Explicit text replacements (exact strings) ----
    explicit = [
        ('<title>Habana Medical Service — Tamale</title>',
         '<title>Del International Hospital — East Legon, Accra</title>'),
        ('<meta name="description" content="Habana Medical Service, Tamale — a private multidisciplinary hospital open 24/7. Fifteen specialties, diagnostics on site, and care guided by love and honesty." />',
         '<meta name="description" content="Del International Hospital, East Legon, Accra — an ultra-modern private hospital open 24/7. Fourteen services, diagnostics on site, and a dedicated fertility centre." />'),
        ('<span class="brand-sub">Service · Tamale</span>',
         '<span class="brand-sub">Hospital · East Legon</span>'),
        ('home: "Habana Medical Service — Tamale",',
         'home: "Del International Hospital — East Legon, Accra",'),
        ('services: "Services | Habana Medical Service, Tamale",',
         'services: "Services | Del International Hospital, East Legon, Accra",'),
        ('about: "About us | Habana Medical Service, Tamale",',
         'about: "About us | Del International Hospital, East Legon, Accra",'),
        ('contact: "Contact & Directions | Habana Medical Service, Tamale"',
         'contact: "Contact & Directions | Del International Hospital, East Legon, Accra"'),
        ('Celebrating 15 years of care · 2011–2026',
         'Open 24/7 · East Legon, Accra'),
        ('<h1>Care with <em>love</em> and <em>honesty</em>, every hour of the day.</h1>',
         '<h1>Modern care, <em>every hour</em> of the day.</h1>'),
        ('Habana Medical Service is one of Northern Ghana&rsquo;s leading private hospitals — specialist doctors, modern diagnostics and a calm, welcoming place to heal, right here in Tamale.',
         'Del International Hospital is an ultra-modern private hospital in East Legon, Accra — specialist doctors, modern diagnostics and a dedicated fertility centre, 30 minutes from the airport.'),
        ('<h1>Fifteen years of <em>love and honesty</em> in healthcare.</h1>',
         '<h1>An ultra-modern hospital in the heart of East Legon.</h1>'),
        ('What began in 2011 as a day clinic in a converted four-bedroom house is now one of Northern Ghana&rsquo;s leading private hospitals.',
         'Del International Hospital is an ultra-modern private hospital providing in-patient and out-patient care to Accra and beyond — with a dedicated fertility centre and specialists on call around the clock.'),
        ('<h2>Founded by a doctor who believed Tamale deserved more.</h2>',
         '<h2>A hospital built for modern Accra.</h2>'),
        ('Habana Medical Service was established in the Tamale metropolis by <strong>Dr Thomas Winsum Anabah</strong>, a Consultant Anaesthesiologist with a Master&rsquo;s in Critical Care and Emergencies. The first patients were walk-in clients living with non-communicable diseases.',
         'Del International Hospital is an ultra-modern hospital in East Legon, Accra — opposite the PH Hotel, about 30 minutes from Kotoka International Airport. It serves patients from across the Greater Accra Region and beyond, including international patients.'),
        ('Today HMS brings together doctors, nurses and support staff across internal medicine, emergency and critical care, paediatrics, public health, obstetrics and gynaecology, ENT, anaesthesia and surgery — with specialists on call around the clock.',
         'Today Del brings together doctors, nurses and support staff across internal medicine, emergency and critical care, paediatrics, obstetrics and gynaecology, fertility care, anaesthesia and surgery — with specialists on call around the clock.'),
        ('Set in a serene environment, our hospital is designed to feel like a home away from home.',
         'Private wards, modern theatres and a calm, welcoming environment — with a canteen and a secure car park on site.'),
        ('<p>Health education and prevention for families across the North.</p>',
         '<p>Health education and prevention for families across Accra.</p>'),
        ('<span class="cap" id="carCap">1 / 7 · International award ceremony</span>',
         '<span class="cap" id="carCap">1 / 5 · Our hospital</span>'),
        ('<h2>A home away from home — with world-class standards.</h2>',
         '<h2>Modern care, close to home — with international standards.</h2>'),
        ('<p class="foot-blurb">A private multidisciplinary hospital serving Tamale and Northern Ghana since 2011. Guided by our motto, &ldquo;Love and Honesty.&rdquo;</p>',
         '<p class="foot-blurb">An ultra-modern private hospital in East Legon, Accra — open 24 hours, every day.</p>'),
        ('Bookings, enquiries and emergencies — 24/7.',
         'Bookings, enquiries and emergencies — 24/7. Also 030 254 3255.'),
        ('Near Kamina Barracks, off GILLBT Road.',
         'Opposite the PH Hotel, about 30 minutes from Kotoka International Airport.'),
        ('Opposite the School of Hygiene, Tamale, Ghana</span></p>',
         'Opposite the PH Hotel, Accra, Ghana · P.O. Box AN 15401</span></p>'),
        ('For CT scan and imaging bookings, call ahead so we can prepare',
         'For ultrasound and imaging bookings, call ahead so we can prepare'),
        ('Our cervical screening clinic runs every Friday at 9:00 AM, under Obstetrics & Gynaecology.',
         'Cervical screening is available under Obstetrics & Gynaecology.'),
        ('destination=Nanton%20Road%2C%20Block%20141%2C%20North%20Kanvilli%2C%20Opposite%20School%20of%20Hygiene%2C%20Tamale%2C%20Ghana',
         'destination=' + DEL_MAPS_DEST),
        ('destination=Habana%20Medical%20Service%2C%20Nanton%20Road%2C%20Block%20141%2C%20North%20Kanvilli%2C%20Tamale%2C%20Ghana',
         'destination=' + DEL_MAPS_DEST),
        ('Habana Medical Service Ltd.', 'Del International Hospital'),
        ('/* kente stripe + footer */', '/* brand stripe + footer */'),
    ]
    for old, new in explicit:
        if old not in s:
            raise ValueError("explicit string not found: " + old[:80])
        s = s.replace(old, new)

    # ---- 6. Blanket replacements (ordered, longest first) ----
    blanket = [
        ("Habana Medical Service", "Del International Hospital"),
        ("Habana Medical", "Del International"),
        ("habanamedicalservice@gmail.com", DEL_EMAIL),
        ("habana", "del"),
        ("023 318 6766", DEL_PHONE),
        ("+233233186766", DEL_PHONE_TEL),
        ("233233186766", DEL_PHONE_WA),
        ("Nanton Road, Block 141, North Kanvilli", DEL_ADDR),
        ("Opposite the School of Hygiene", "Opposite the PH Hotel"),
        ("opposite the School of Hygiene", "opposite the PH Hotel"),
        ("North Kanvilli", "East Legon"),
        ("Tamale, Northern Region, Ghana", "Accra, Ghana"),
        ("Tamale, Northern Region", "Accra"),
        ("Northern Ghana", "Accra"),
        ("Northern Region", "Greater Accra"),
        ("Tamale", "Accra"),
        ("Fifteen", "Fourteen"),
        ("fifteen", "fourteen"),
        ("15 services", "14 services"),
        ("15 Medical", "14 Medical"),
        ("Habana", "Del"),
    ]
    for old, new in blanket:
        s = s.replace(old, new)
    s = re.sub(r'\bHMS\b', 'Del', s)

    # ---- 7. Safety net: any photo still embedded from Habana -> generic placeholder.
    # Every real photo (building + all stock photos) is kept as-is.
    keep = {DEL_BUILDING_IMG, DOCTOR_IMG, DEL_REAL_IMG}
    keep.update(_photo_uri("services", k) for k in PH)
    keep.update(_photo_uri("slides", k) for k in ("reception", "maternity", "team",
                                                       "reception-real", "team-real",
                                                       "waiting-real", "billboard-real"))
    counter = [0]

    def _generic(m):
        if m.group(0) in keep:
            return m.group(0)
        i = counter[0]
        counter[0] += 1
        return ph("Del International Hospital", "East Legon · Accra",
                  800, 600, variant=i)

    s = re.sub(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', _generic, s)

    # ---- 8. Del overrides: side padding, logo-only chat button, reviews ----
    # (a) CSS overrides, appended last in the stylesheet so they win.
    if s.count("</style>") != 1:
        raise ValueError("expected exactly one </style>, found %d" % s.count("</style>"))
    s = s.replace("</style>", DEL_CSS_OVERRIDES + "</style>", 1)
    # (b) Reviews section at the end of the home page, after the About teaser.
    rev_anchor = '  </section>\n</div>\n\n<!-- ================= SERVICES ================= -->'
    if s.count(rev_anchor) != 1:
        raise ValueError("reviews anchor not found")
    s = s.replace(rev_anchor,
                  '  </section>\n' + REVIEWS_SECTION +
                  '\n</div>\n\n<!-- ================= SERVICES ================= -->', 1)
    # (c) Reviews on the About page (after the facilities section) and in the
    #     contact page's left column (under the form) — the two yellow-marked gaps.
    about_anchor = '  </section>\n</div>\n\n<!-- ================= CONTACT ================= -->'
    if s.count(about_anchor) != 1:
        raise ValueError("about reviews anchor not found")
    s = s.replace(about_anchor,
                  '  </section>\n' + REVIEWS_SECTION +
                  '\n</div>\n\n<!-- ================= CONTACT ================= -->', 1)
    contact_anchor = '    </div>\n\n    <aside class="panel">'
    if s.count(contact_anchor) != 1:
        raise ValueError("contact reviews anchor not found")
    s = s.replace(contact_anchor,
                  CONTACT_REVIEWS + '\n    </div>\n\n    <aside class="panel">', 1)
    aside_anchor = '      </article>\n    </aside>\n  </section>\n</div>\n</main>'
    if s.count(aside_anchor) != 1:
        raise ValueError("contact aside anchor not found")
    s = s.replace(aside_anchor,
                  '      </article>\n' + CONTACT_REVIEW_RIGHT +
                  '\n    </aside>\n  </section>\n</div>\n</main>', 1)
    # (d) Mission + Vision above the core-values cards; rename the heading.
    if s.count('<h2>Our values</h2>') != 1:
        raise ValueError("values heading not found")
    s = s.replace('<h2>Our values</h2>',
                  MISSION_VISION_HTML + '      <h2>Our core values</h2>', 1)
    # (d) Pop-in script + preview timer script, just before </body>.
    if s.count("</body>") != 1:
        raise ValueError("expected exactly one </body>, found %d" % s.count("</body>"))
    s = s.replace("</body>", POP_IN_JS + PREVIEW_TIMER_JS + "</body>", 1)
    # (d) Chat button: logo only — drop the chat icon and the "Chat with us" text.
    if s.count('<span>Chat with us</span>') != 1:
        raise ValueError("chat fab text not found")
    s = s.replace('\n  <span>Chat with us</span>', '', 1)
    s = re.sub(r'(<button class="chat-fab"[^>]*>.*?<span class="fab-logo"[^>]*>.*?</span>)\s*<svg[^>]*>.*?</svg>',
               r'\1', s, count=1, flags=re.DOTALL)
    return s


# ---------------------------------------------------------------- verify
FORBIDDEN = [
    "Habana", "habana", "Tamale", "023 318", "233186766",
    "habanamedicalservice", "Anabah", "2011", "Siemens", "SOMATOM",
    "mammograph", "Mammograph", "Fifteen", "fifteen", "15 services",
    "Echocardiography", "lovable", "facebook.com/Habana",
    "instagram.com/habanamedicalservice", "tiktok.com/@habanamedicalservice",
    "Northern", "Kamina", "GILLBT", "School of Hygiene", "Nanton Road",
    "North Kanvilli", "kente", "Kente", "Friday at 9:00 AM", "Fridays, 9:00 AM",
    "Endoscopy", "Ophthalmology", "Neurosurgery", "Psychology",
]
FORBIDDEN_WORDS = [r"\bHMS\b", r"\bENT\b", r"\bCT\b"]


def verify(s):
    problems = []
    # Strip embedded images first: base64 blobs can contain substrings
    # like "2011" or "CT" by coincidence.
    text = re.sub(r'data:image/[^"\']+;base64,[A-Za-z0-9+/=]+', '', s)
    for token in FORBIDDEN:
        if token in text:
            problems.append("forbidden token present: %r" % token)
    for pat in FORBIDDEN_WORDS:
        if re.search(pat, text):
            problems.append("forbidden word present: %s" % pat)
    checks = {
        "svc-card buttons": s.count('class="svc-card"'),
        "Fertility Centre": s.count("Fertility Centre"),
        "Physiotherapy": s.count("Physiotherapy"),
        "Dietetics": s.count("Dietetics"),
        "Counselling": s.count("Counselling"),
        "Del International Hospital": s.count("Del International Hospital"),
        "030 254 3256": s.count("030 254 3256"),
        "info@delinternationalhospital.com": s.count(DEL_EMAIL),
        "65/67 Nii Sai Street": s.count("65/67 Nii Sai Street"),
        "real building photo uses": s.count(DEL_BUILDING_IMG),
        "doctor consultation photo uses": s.count(DOCTOR_IMG),
        "real Del building photo uses": s.count(DEL_REAL_IMG),
        "svg placeholders left": s.count("data:image/svg+xml"),
        "patient reviews section": s.count("What our patients say"),
        "chat fab text left": s.count("Chat with us"),
        "css overrides": s.count("Del overrides (2026-11-21)"),
        "review cards": s.count('class="value-card review-card"'),
        "real team photo uses": s.count(_photo_uri("slides", "team-real")),
        "pop-in keyframes": s.count("@keyframes delPopIn"),
        "pop-in script": s.count("// Pop-in on load and on scroll."),
        "our core values": s.count("Our core values"),
        "old values heading": s.count("<h2>Our values</h2>"),
        "our mission": s.count("Our Mission"),
        "our vision": s.count("Our Vision"),
        "mission grid": s.count('class="mission-grid"'),
        "preview timer bar": s.count('id="previewTimer"'),
        "preview timer script": s.count("// Preview countdown timer:"),
        "header fade script": s.count("// Transparent header on scroll (user, 2026-11-22):"),
    }
    if checks["svc-card buttons"] != 20:
        problems.append("svc-card count %d, expected 20" % checks["svc-card buttons"])
    if checks["real building photo uses"] != 4:
        problems.append("real building photo used %d times, expected 4 "
                        "(hero x1, carousel x1, collage, contact)"
                        % checks["real building photo uses"])
    if checks["doctor consultation photo uses"] != 1:
        problems.append("doctor consultation photo used %d times, expected 1 "
                        "(hero slide 2)"
                        % checks["doctor consultation photo uses"])
    if checks["our core values"] != 1:
        problems.append("core values heading found %d times, expected 1"
                        % checks["our core values"])
    if checks["old values heading"] != 0:
        problems.append("old values heading still present (%d)"
                        % checks["old values heading"])
    if checks["our mission"] != 1 or checks["our vision"] != 1:
        problems.append("mission/vision found %d/%d times, expected 1/1"
                        % (checks["our mission"], checks["our vision"]))
    if checks["mission grid"] != 1:
        problems.append("mission grid found %d times, expected 1"
                        % checks["mission grid"])
    if checks["real team photo uses"] != 2:
        problems.append("real team photo used %d times, expected 2 "
                        "(gallery slide + About teaser)"
                        % checks["real team photo uses"])
    if checks["pop-in keyframes"] != 1:
        problems.append("pop-in keyframes found %d times, expected 1"
                        % checks["pop-in keyframes"])
    if checks["pop-in script"] != 1:
        problems.append("pop-in script found %d times, expected 1"
                        % checks["pop-in script"])
    if checks["patient reviews section"] != 3:
        problems.append("patient reviews section found %d times, expected 3 "
                        "(home, about, contact)"
                        % checks["patient reviews section"])
    if checks["review cards"] != 9:
        problems.append("review cards %d, expected 9" % checks["review cards"])
    if s.count('class="contact-reviews"') != 1:
        problems.append("contact reviews block found %d times, expected 1"
                        % s.count('class="contact-reviews"'))
    aside_start = s.find('<aside class="panel">')
    if aside_start < 0 or s.find("Efua M.", aside_start) < 0:
        problems.append("Efua review not found inside the contact aside")
    if checks["chat fab text left"] != 0:
        problems.append("chat fab text still present (%d)"
                        % checks["chat fab text left"])
    if checks["preview timer bar"] != 1:
        problems.append("preview timer bar found %d times, expected 1"
                        % checks["preview timer bar"])
    if checks["preview timer script"] != 1:
        problems.append("preview timer script found %d times, expected 1"
                        % checks["preview timer script"])
    if checks["header fade script"] != 1:
        problems.append("header fade script found %d times, expected 1"
                        % checks["header fade script"])
    if checks["css overrides"] != 1:
        problems.append("css overrides found %d times, expected 1"
                        % checks["css overrides"])
    if checks["real Del building photo uses"] != 1:
        problems.append("real Del building photo used %d times, expected 1 "
                        "(hero slide 3)"
                        % checks["real Del building photo uses"])
    # The only SVGs left should be the Del logo (4 uses) + the map (1).
    if checks["svg placeholders left"] != 5:
        problems.append("svg data URIs: %d, expected 5 (logo x4 + map)"
                        % checks["svg placeholders left"])
    for k in ("Fertility Centre", "Physiotherapy", "Dietetics", "Counselling"):
        if checks[k] < 3:
            problems.append("%s appears only %d times" % (k, checks[k]))
    if checks["Del International Hospital"] < 20:
        problems.append("brand name appears only %d times"
                        % checks["Del International Hospital"])
    if checks["030 254 3256"] < 10:
        problems.append("Del phone appears only %d times" % checks["030 254 3256"])
    if checks["info@delinternationalhospital.com"] < 2:
        problems.append("Del email appears only %d times"
                        % checks["info@delinternationalhospital.com"])
    return problems, checks


def js_check(s):
    """Extract the inline <script> and syntax-check it with node."""
    m = re.search(r"<script>(.*?)</script>", s, re.DOTALL)
    if not m:
        return "no <script> block found"
    tmp = Path("/tmp/del-demo-check.js")
    tmp.write_text(m.group(1), encoding="utf-8")
    import subprocess
    r = subprocess.run(["node", "--check", str(tmp)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return "node --check failed:\n" + r.stderr
    return None


def main():
    src = SRC.read_text(encoding="utf-8")
    out = transform(src)
    problems, checks = verify(out)
    if problems:
        print("VERIFY FAILED:")
        for p in problems:
            print(" -", p)
        raise SystemExit(1)
    err = js_check(out)
    if err:
        print("JS CHECK FAILED:")
        print(err)
        raise SystemExit(1)
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(out, encoding="utf-8")
    print("OK — wrote", DST, "(%d bytes)" % len(out.encode("utf-8")))
    for k, v in checks.items():
        print("  %-32s %d" % (k, v))


if __name__ == "__main__":
    main()
