from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from docx import Document
from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from langchain_ollama import ChatOllama


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://clarity-ai-two-eta.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract(file):

    document = Document(file)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text.strip())

    return "\n".join(paragraphs)


def simplify(text):

    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )

    prompt = f"""
        You are a job description translator.

        Your job is to turn the following job posting into something a normal person
        can understand quickly.

        RULES:
        - Be direct and honest.
        - Use plain English.
        - Remove corporate buzzwords and unnecessary fluff.
        - Do NOT make anything up.
        - Do NOT assume missing information.
        - Do NOT exaggerate the job.
        - Keep specific requirements, qualifications, years of experience,
        salary, location, schedule, and benefits exactly as stated.
        - If something is not mentioned, say "Not stated."
        - Explain technical or corporate terms in simple language.
        - Make the result easy to scan.
        - Use short bullet points.
        - Separate actual requirements from "nice to have" qualifications.
        - Clearly identify anything that sounds optional.
        - If the posting is vague about something important, say so.

        FORMAT:

        COMPANY
        [company name exactly as stated in the job description, or Not stated. This should be in uppercase.]
        
        JOB TITLE
        [job title]

        THE JOB IN ONE SENTENCE
        [Explain what this person actually does in one simple sentence.]

        WHAT YOU'LL ACTUALLY DO
        - [responsibility]
        - [responsibility]

        WHAT YOU NEED
        - [required qualification]
        - [required qualification]

        NICE TO HAVE
        - [optional qualification]

        SKILLS
        - [skill]
        - [skill]

        PAY & BENEFITS
        - [only include information actually stated]

        WHERE / WHEN
        - Location: [stated location or "Not stated"]
        - Work arrangement: [remote/hybrid/in-office or "Not stated"]
        - Schedule: [stated schedule or "Not stated"]

        JARGON TRANSLATED
        - "[term]" → [plain-English explanation]

        RED FLAGS / THINGS TO NOTICE
        - [Only mention genuine issues such as vague requirements,
        unrealistic combinations, missing salary information, or
        unusually broad responsibilities.]
        - If there are no obvious issues, say "Nothing obvious."

        FORMATTING RULES:
        - Do not use Markdown.
        - Do not use ** for bold.
        - Do not use # headings.
        - Use the section names exactly as provided.
        - Use "-" for bullet points.

        JOB DESCRIPTION:

        {text}
        """

    response = llm.invoke(prompt)

    return response.content


@app.post("/simplify")
async def simplify_job(file: UploadFile = File(...)):

    file_data = await file.read()

    text = extract(BytesIO(file_data))

    simplified = simplify(text)

    lines = simplified.splitlines()

    company = lines[0].strip()

    return {
        "simplified": simplified,
        "company": company
    }


@app.post("/export-pdf")
async def export_pdf(data: dict):

    text = data["text"]
    company = data["company"]

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()

    heading_style = styles["Heading2"]
    heading_style.fontName = "Helvetica-Bold"
    heading_style.fontSize = 13
    heading_style.leading = 16
    heading_style.spaceBefore = 14
    heading_style.spaceAfter = 8

    body_style = styles["BodyText"]
    body_style.fontSize = 10.5
    body_style.leading = 15
    body_style.spaceAfter = 6
    

    story = []

    sections = [
        "COMPANY",
        "JOB TITLE",
        "THE JOB IN ONE SENTENCE",
        "WHAT YOU'LL ACTUALLY DO",
        "WHAT YOU NEED",
        "NICE TO HAVE",
        "SKILLS",
        "PAY & BENEFITS",
        "WHERE / WHEN",
        "JARGON TRANSLATED",
        "RED FLAGS / THINGS TO NOTICE"
    ]
    
    for line in text.split("\n") :

        if not line:
            story.append(Spacer(1, 6))
            continue

        line = line.replace("**", "")

        if line.upper() in sections:
            story.append(
                Paragraph(line, heading_style)
            )

        elif line.startswith("-"):

            bullet_text = line[1:].strip()

            story.append(
                Paragraph(
                    f"• {bullet_text}",
                    body_style
                )
            )

        elif line.startswith("•"):

            bullet_text = line[1:].strip()

            story.append(
                Paragraph(
                    f"• {bullet_text}",
                    body_style
                )
            )

        else:

            if line == company:
                story.append(
                    Paragraph(line, heading_style)
                )
            else:
                story.append(
                    Paragraph(line, body_style)
                )

    document.build(story)

    pdf = buffer.getvalue()


    return Response(
        content=pdf,
        media_type="application/pdf"
    )