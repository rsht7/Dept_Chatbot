

import json
import random

# Load your JSON
with open('faculty_data_all_tabs.json', 'r', encoding='utf-8') as f:
    faculty_data = json.load(f)

paragraphs = []

for faculty in faculty_data:
    name = faculty.get('Name', 'Unknown Name')
    department = faculty.get('Department', 'Unknown Department')
    designation = faculty.get('Designation', 'Faculty Member')
    qualification = faculty.get('Qualification', '')
    research_interests = faculty.get('Research Interests', '')
    email = faculty.get('Email', '')
    personal_webpage = faculty.get('Personal Webpage', '')
    
    publications = faculty.get('Publications', [])
    projects = faculty.get('Projects', [])
    memberships = faculty.get('Memberships', [])
    books = faculty.get('Books Published', [])

    first_reference = name
    second_reference = random.choice(["the faculty member", "this professor"])

    para = f"{first_reference} is a {designation} in the Department of {department} at PEC University of Technology. "

    if qualification:
        para += f"{first_reference} holds qualifications such as {qualification}. "
    
    if research_interests:
        para += f"Their research interests include {research_interests}. "
    
    if email:
        para += f"Their email address is {email}. "

    if personal_webpage:
        para += f"More information can also be found on their personal webpage at {personal_webpage}. "

    if publications:
        pubs_text = '; '.join(publications[:2])
        para += f"{first_reference} has authored important publications such as {pubs_text}. "

    if projects:
        proj_text = '; '.join(projects[:2])
        para += f"{second_reference.capitalize()} has contributed to projects like {proj_text}. "

    if memberships:
        mem_text = '; '.join(memberships[:2])
        para += f"{second_reference.capitalize()} is a member of organizations including {mem_text}. "

    if books:
        # filter out empty book titles
        books = [b for b in books if b.strip()]
        if books:
            books_text = '; '.join(books[:2])
            para += f"{second_reference.capitalize()} has also co-authored books such as {books_text}. "

    # Add final CTA
    profile_url = f"https://pec.ac.in/ee/faculty/{name.lower().replace(' ', '-').replace('_', '-')}"
    para += f"For more detailed information about {name}, please visit their faculty profile page at {profile_url}."

    paragraphs.append(para.strip())

# Save to text file
with open('faculty_paragraphs_full2.txt', 'w', encoding='utf-8') as f:
    for p in paragraphs:
        f.write(p + '\n\n')

print("✅ Faculty paragraphs created successfully! Saved to faculty_paragraphs_full.txt")
