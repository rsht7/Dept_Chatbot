# # import pdfplumber
# # import re
# # import os
# # import json

# # # ========== CONFIGURATION ==========
# # PDF_PATH = "data/8thsemdec.pdf"  # 🔥 Change this to your pdf path
# # OUTPUT_FOLDER = "Extracted_Courses"  # Where to save the extracted course details
# # os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# # # Helper to clean text
# # def clean_text(text):
# #     return ' '.join(text.split())

# # # Extract structured fields from a course block
# # def extract_course_data(text_block):
# #     data = {}

# #     # Extract simple fields
# #     data["course_name"] = re.search(r"Course Name\s*:\s*(.*)", text_block)
# #     data["course_code"] = re.search(r"Course Code\s*:\s*(.*)", text_block)
# #     data["credits"] = re.search(r"Credits\s*:\s*(.*)", text_block)
# #     data["ltp"] = re.search(r"LTP\s*:\s*(.*)", text_block)

# #     # Extract course objectives
# #     course_obj = re.search(r"Course Objectives:(.*?)Lecture Wise Breakup", text_block, re.DOTALL | re.IGNORECASE)
# #     data["course_objectives"] = clean_text(course_obj.group(1)) if course_obj else ""

# #     # Extract course outcomes
# #     outcomes = re.search(r"Course Outcomes:(.*?)Suggested Books:", text_block, re.DOTALL | re.IGNORECASE)
# #     if outcomes:
# #         outcome_text = outcomes.group(1)
# #         outcome_lines = re.findall(r"(CO\d+)\s*(.*)", outcome_text)
# #         data["course_outcomes"] = {code: clean_text(desc) for code, desc in outcome_lines}
# #     else:
# #         data["course_outcomes"] = {}

# #     # Extract suggested books
# #     books = []
# #     book_section = re.search(r"Suggested Books:(.*)", text_block, re.DOTALL | re.IGNORECASE)
# #     if book_section:
# #         book_lines = book_section.group(1).split("\n")
# #         for line in book_lines:
# #             parts = re.split(r'\s{2,}', line.strip())
# #             if len(parts) >= 3:
# #                 books.append({
# #                     "sr_no": parts[0],
# #                     "book_name_author": parts[1],
# #                     "year": parts[2]
# #                 })
# #     data["suggested_books"] = books

# #     # Clean all extracted text
# #     for key in ["course_name", "course_code", "credits", "ltp"]:
# #         if data[key]:
# #             data[key] = clean_text(data[key].group(1))

# #     return data

# # # ========== MAIN EXTRACTION ==========
# # with pdfplumber.open(PDF_PATH) as pdf:
# #     all_courses = []
# #     current_text = ""
# #     is_course_start = False

# #     for page in pdf.pages:
# #         text = page.extract_text()

# #         if not text:
# #             continue

# #         if "Course Name" in text:
# #             if current_text:
# #                 course_data = extract_course_data(current_text)
# #                 all_courses.append(course_data)
# #             current_text = text  # Start a new course
# #         else:
# #             current_text += "\n" + text  # Continue adding to current course

# #     # Add the last course
# #     if current_text:
# #         course_data = extract_course_data(current_text)
# #         all_courses.append(course_data)

# # # ========== SAVE ==========
# # for course in all_courses:
# #     filename = f"{course['course_code']}_{course['course_name'].replace(' ', '_')}.json"
# #     filepath = os.path.join(OUTPUT_FOLDER, filename)
# #     with open(filepath, "w", encoding="utf-8") as f:
# #         json.dump(course, f, indent=4)

# # print(f"✅ Extracted {len(all_courses)} courses into '{OUTPUT_FOLDER}' folder.")



# # import pdfplumber
# # import re
# # import os
# # import json

# # # CONFIGURATION
# # PDF_PATH = "data/8thsemdec.pdf"  # <-- Change to your PDF file name
# # OUTPUT_FOLDER = "Extracted_Courses"
# # os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# # # Helper function to clean extracted text
# # def clean(text):
# #     if text:
# #         return ' '.join(text.replace('\n', ' ').split())
# #     return None

# # # Function to extract course info from a block of text
# # def extract_course(text_block):
# #     course = {}

# #     course['course_name'] = clean(re.search(r"Course Name\s*:\s*(.*)", text_block).group(1))
# #     course['course_code'] = clean(re.search(r"Course Code\s*:\s*(.*)", text_block).group(1))
# #     course['credits'] = clean(re.search(r"Credits\s*:\s*(.*)", text_block).group(1))
# #     course['ltp'] = clean(re.search(r"LTP\s*:\s*(.*)", text_block).group(1))

# #     course['course_objectives'] = clean(
# #         re.search(r"Course Objectives\s*:(.*?)(Lecture Wise Breakup|Course Outcomes|Suggested Books|$)", text_block, re.DOTALL).group(1)
# #     )

# #     # Extract Course Outcomes
# #     course_outcomes = {}
# #     outcomes_section = re.search(r"Course Outcomes\s*:(.*?)(Suggested Books|$)", text_block, re.DOTALL)
# #     if outcomes_section:
# #         outcome_text = outcomes_section.group(1)
# #         outcome_matches = re.findall(r"(CO\d+)\s*(.*?)\n", outcome_text)
# #         for co_code, description in outcome_matches:
# #             course_outcomes[co_code] = clean(description)
# #     course['course_outcomes'] = course_outcomes

# #     # Extract Suggested Books
# #     suggested_books = []
# #     books_section = re.search(r"Suggested Books\s*:(.*)", text_block, re.DOTALL)
# #     if books_section:
# #         books_text = books_section.group(1).split('\n')
# #         for line in books_text:
# #             parts = re.split(r'\s{2,}', line.strip())
# #             if len(parts) >= 2:
# #                 book_entry = {
# #                     "sr_no": parts[0],
# #                     "book_name_author": parts[1],
# #                     "year": parts[2] if len(parts) > 2 else ""
# #                 }
# #                 suggested_books.append(book_entry)
# #     course['suggested_books'] = suggested_books

# #     return course

# # # Function to detect new course
# # def is_new_course(line):
# #     return "Course Name" in line and "Course Code" in line and "Credits" in line

# # # MAIN EXTRACTION
# # with pdfplumber.open(PDF_PATH) as pdf:
# #     all_courses = []
# #     current_text = ""

# #     for page in pdf.pages:
# #         text = page.extract_text()

# #         if not text:
# #             continue

# #         lines = text.split('\n')

# #         for line in lines:
# #             if is_new_course(line):
# #                 if current_text:
# #                     all_courses.append(extract_course(current_text))
# #                 current_text = line + "\n"
# #             else:
# #                 current_text += line + "\n"

# #     # Save last course
# #     if current_text:
# #         all_courses.append(extract_course(current_text))

# # # SAVE COURSES TO INDIVIDUAL JSON FILES
# # for idx, course in enumerate(all_courses):
# #     filename = f"{course['course_code']}_{course['course_name'].replace(' ', '_')}.json"
# #     filepath = os.path.join(OUTPUT_FOLDER, filename)
# #     with open(filepath, "w", encoding="utf-8") as f:
# #         json.dump(course, f, indent=4)

# # print(f"✅ Successfully extracted {len(all_courses)} courses!")



# import pdfplumber
# import os
# import json
# import re

# PDF_PATH = "data/8thsemdec.pdf"  # <-- your file
# OUTPUT_FOLDER = "Extracted_Courses"
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# # Helper to clean text
# def clean(text):
#     if text:
#         return ' '.join(text.replace('\n', ' ').split())
#     return ""

# # Extract course from text block
# def extract_course(text, tables):
#     course = {}

#     # Extract basic fields
#     course_name = re.search(r"Course Name\s*:\s*(.*)", text)
#     course_code = re.search(r"Course Code\s*:\s*(.*)", text)
#     credits = re.search(r"Credits\s*:\s*(.*)", text)
#     ltp = re.search(r"LTP\s*:\s*(.*)", text)

#     course['course_name'] = clean(course_name.group(1)) if course_name else None
#     course['course_code'] = clean(course_code.group(1)) if course_code else None
#     course['credits'] = clean(credits.group(1)) if credits else None
#     course['ltp'] = clean(ltp.group(1)) if ltp else None

#     # Extract course objectives
#     course_obj_match = re.search(r"Course Objectives\s*:(.*?)(Lecture Wise Breakup|Course Outcomes|Suggested Books|Total No. of Lectures|\Z)", text, re.S)
#     course['course_objectives'] = clean(course_obj_match.group(1)) if course_obj_match else None

#     # Extract course outcomes
#     outcomes = {}
#     co_section = re.search(r"Course Outcomes\s*:(.*?)(Suggested Books|Total No. of Lectures|\Z)", text, re.S)
#     if co_section:
#         co_text = co_section.group(1)
#         co_matches = re.findall(r"(CO\d+)\s*(.*?)\n", co_text)
#         for code, desc in co_matches:
#             outcomes[code] = clean(desc)
#     course['course_outcomes'] = outcomes

#     # Extract Suggested Books (from tables)
#     suggested_books = []
#     for table in tables:
#         headers = [clean(cell) for cell in table[0]]
#         if any('Book' in header for header in headers):
#             for row in table[1:]:
#                 if any(cell.strip() for cell in row):
#                     suggested_books.append({
#                         "sr_no": clean(row[0]),
#                         "book_name_author": clean(row[1]),
#                         "year": clean(row[2]) if len(row) > 2 else ""
#                     })
#     course['suggested_books'] = suggested_books

#     return course

# # Main
# with pdfplumber.open(PDF_PATH) as pdf:
#     current_course_text = ""
#     current_tables = []
#     courses = []

#     for page in pdf.pages:
#         text = page.extract_text()
#         tables = page.extract_tables()

#         if not text:
#             continue

#         if "Course Name" in text and "Course Code" in text:
#             if current_course_text:
#                 course_info = extract_course(current_course_text, current_tables)
#                 if course_info['course_name']:
#                     courses.append(course_info)
#             current_course_text = text
#             current_tables = tables
#         else:
#             current_course_text += "\n" + text
#             current_tables.extend(tables)

#     # Save last course
#     if current_course_text:
#         course_info = extract_course(current_course_text, current_tables)
#         if course_info['course_name']:
#             courses.append(course_info)

# # Save individual files
# for course in courses:
#     filename = f"{course['course_code']}_{course['course_name'].replace(' ', '_')}.json"
#     filepath = os.path.join(OUTPUT_FOLDER, filename)
#     with open(filepath, 'w', encoding='utf-8') as f:
#         json.dump(course, f, indent=4)

# print(f"✅ Done! Extracted {len(courses)} courses.")



import pdfplumber
import os
import json
import re

PDF_PATH = "data/8th.pdf"  # <-- your PDF file
OUTPUT_FOLDER = "Extracted_Courses_Premium"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def clean(text):
    if text:
        return ' '.join(text.replace('\n', ' ').split())
    return ""

def extract_course(text, tables):
    course = {}

    # Fix minor OCR errors
    text = text.replace("CourseObjectives", "Course Objectives").replace("CourseOutcomes", "Course Outcomes")

    # Extract basic fields
    course_name = re.search(r"Course Name\s*:\s*(.*)", text)
    course_code = re.search(r"Course Code\s*:\s*(.*)", text)
    credits = re.search(r"Credits\s*:\s*(.*)", text)
    ltp = re.search(r"LTP\s*:\s*(.*)", text)

    course['course_name'] = clean(course_name.group(1)) if course_name else None
    course['course_code'] = clean(course_code.group(1)) if course_code else None
    course['credits'] = clean(credits.group(1)) if credits else None
    course['ltp'] = clean(ltp.group(1)) if ltp else None

    # Extract course objectives
    course_obj_match = re.search(r"Course Objectives\s*:(.*?)(Lecture Wise Breakup|Course Outcomes|Suggested Books|Total No. of Lectures|\Z)", text, re.S)
    course['course_objectives'] = clean(course_obj_match.group(1)) if course_obj_match else None

    # Extract course outcomes
    outcomes = {}
    co_section = re.search(r"Course Outcomes\s*:(.*?)(Suggested Books|Total No. of Lectures|\Z)", text, re.S)
    if co_section:
        co_text = co_section.group(1)
        # Allow multi-line CO entries
        co_lines = co_text.split('\n')
        current_co = None
        for line in co_lines:
            line = clean(line)
            if re.match(r"CO\d+", line):
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    current_co = parts[0]
                    outcomes[current_co] = parts[1]
            elif current_co:
                outcomes[current_co] += ' ' + line
    course['course_outcomes'] = outcomes

    # Extract suggested books
    suggested_books = []
    for table in tables:
        headers = [clean(cell) for cell in table[0]]
        if any('Book' in header or 'Author' in header for header in headers):
            last_book = None
            for row in table[1:]:
                row = [clean(cell) for cell in row]
                if row and row[0].isdigit():
                    # New book
                    book = {
                        "sr_no": row[0],
                        "book_name_author": row[1],
                        "year": row[2] if len(row) > 2 else ""
                    }
                    suggested_books.append(book)
                    last_book = book
                else:
                    # Continuation of previous book
                    if last_book:
                        last_book["book_name_author"] += ' ' + ' '.join(row)
    course['suggested_books'] = suggested_books

    return course

# Main Extraction
with pdfplumber.open(PDF_PATH) as pdf:
    current_course_text = ""
    current_tables = []
    courses = []

    for page in pdf.pages:
        text = page.extract_text()
        tables = page.extract_tables()

        if not text:
            continue

        if "Course Name" in text and "Course Code" in text:
            if current_course_text:
                course_info = extract_course(current_course_text, current_tables)
                if course_info['course_name']:
                    courses.append(course_info)
            current_course_text = text
            current_tables = tables
        else:
            current_course_text += "\n" + text
            current_tables.extend(tables)

    # Save last course
    if current_course_text:
        course_info = extract_course(current_course_text, current_tables)
        if course_info['course_name']:
            courses.append(course_info)

# Save all courses in one file
with open(os.path.join(OUTPUT_FOLDER, "all_courses.json"), 'w', encoding='utf-8') as f:
    json.dump(courses, f, indent=4)

# Save individual course files
for course in courses:
    safe_course_name = course['course_name'].replace(' ', '_').replace('/', '_') if course['course_name'] else "Unknown"
    safe_course_code = course['course_code'] if course['course_code'] else "NA"
    filename = f"{safe_course_code}_{safe_course_name}.json"
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(course, f, indent=4)

print(f"🏆 Done! Successfully extracted {len(courses)} courses into {OUTPUT_FOLDER}")
