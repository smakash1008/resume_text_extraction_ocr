import pytesseract
from PIL import Image
from dotenv import load_dotenv
load_dotenv()
import cv2
import google.generativeai as genai
from google.api_core import retry
import json
import os
import time

file_path = input("Enter the File Path: ")
print(file_path)

def preprocess_image(file_path):
    image = cv2.imread(file_path)
    print(image.shape)
    print(type(image))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)
    return binary_image

preprocessed_image = preprocess_image(file_path)
cv2.imwrite('Preprocessed_image.png', preprocessed_image)

image_pil = Image.fromarray(preprocessed_image)
custom_config = r'--oem 3 --psm 11'
text = pytesseract.image_to_string(image_pil, config=custom_config,)
print(text)

with open("image_text_extraction7.txt","w") as file:
    file.write(text)
    print("File Written Successfully...")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY1"))

file_path = "image_text_extraction7.txt"

def upload_file_gemini(file_path):
    file = genai.upload_file(file_path)
    print(f"File Uploaded: {file.display_name} and File URI: {file.uri}")
    return file

file_uploaded = upload_file_gemini(file_path)
print(file_uploaded)

uploaded_file_name = file_uploaded.name
print(uploaded_file_name)

# Waiting If the File is Not Active:

def wait_for_active_file(file_uploaded):
    global file_get
    file_get = genai.get_file(uploaded_file_name)
    print(file_get)
    print(file_get.name, file_get.display_name)
    print(file_get.state.name)
    while file_get.state.name == 'PROCESSING':
        print("The file is still Processing.")
        time.sleep(20)
        file_get = genai.get_file(uploaded_file_name)
        print(file_get)
        print(file_get.name, file_get.display_name)
        print(file_get.state.name)
    if file_get.state.name != 'ACTIVE':
        raise Exception(f"File: {file_get.name} not processed till now.")
    

    return "The File is Active and it is ready for Data Scrapping..."

file_state = wait_for_active_file(file_uploaded)
print(file_state)

for file in genai.list_files():
    print(f"Name: {file.display_name} and Uri: {file.uri}")

# Getting the File Extension:

file_displayname = file_get.display_name
print(file_displayname)

def extract_file_extension(file_displayname):
    file_name_split = file_displayname.split(".",1)
    print(file_name_split)
    if len(file_name_split) == 2:
        file_extension = file_name_split[1]
        return file_extension
    else:
        return None
    
file_extension_extract = extract_file_extension(file_displayname)
print(file_extension_extract)

# Extracting the Text from the PDF Or Docx:

with open("image_text_extraction7.txt","r") as file:
    text = file.read()

print(text)

instruction = "Behave like the best resume data scrapper and give the data which I needed only. Give the data in indented form with an indent of 4. Give all the data without any fail. The final data should match with the text variable strictly. The final data should not have any unrelated data. You should not strictly assign data on your own. Complete the incomplete text by analyzing on your own. The final data should have a proper and completed and relevant data only."

model = genai.GenerativeModel(model_name="gemini-1.5-pro",generation_config=genai.GenerationConfig(
    temperature=0.9,
    top_p=0.95,
    top_k=64,
    max_output_tokens=8192,
    response_mime_type='application/json',
),system_instruction=instruction)

prompt = f"""
Text Extracted : {text}

Extract the Name, Email Address, Phone Number, Skills, Total Years Of Experience, Work Domain, Companies Worked, Date of Birth, Gender, Marital Status, Nationality, Languages, Educational Institution, Education Course, Education Branch, Graduation Year, Exam Percentage, Courses and Certifications, Project Name, Project Description, Project Roles, Project Duration, Project Domain, Project Technologies from the above Text Extracted. Remove the New line characters present in the Name, Email, Courses and Certifications. Name the key as Work Experience for Companies Worked and give only the Companies_Worked and Dont give the Project Names in the Work_Experience strictly. The Work Experience should have only Companies Worked and strictly dont take any details from the Project Sections. Name the key as Education Details for Educational Institution, Education Course, Education Branch, Graduation Year, Exam Percentage and give the Education Details based on Education Course. Dont assign Courses and Certifications in the Education Details. Name the key as Project Details for Project Name, Project Description, Project Roles, Project Duration, Project Domain, Project Technologies. The final order should be Name, Email Address, Phone Number, Skills, Total Years Of Experience, Work Domain, Work Experience, Date of Birth, Gender, Marital Status, Nationality, Languages, Education Details, Courses and Certification and Project Details. Inside the Education Details the final order should be Educational Institution, Education Course, Education Branch, Graduation Year, Exam Percentage. Inside the Project Details the final order should be Project Name, Project Description, Project Roles, Project Duration, Project Domain, Project Technologies. Dont add the Reference and Responsibilities in the Project Details. The Project Description should be summarized in a way that it should not exceed 2 lines strcitly. Dont assign any variable to the final data. Dont change the order at any time. If the Work Domain is present take that only from the text and dont add extra details in it. If there is no details related to Work Domain try to assign only the domain related detail present in the text to the Work Domain at that situation only and dont try to analyze on your own. Dont try to assign unrelated details in Work Domain. Dont assign Skills, Tools, Technologies and Roles Played such as java, html, python, Software Developer, Solution Developer, Team Lead etc, in the Work Domain. Strictly the Work Domain should not contain Roles Played in the Company, Skills and Tools names strictly. Strictly no tools and skills names should be present in Work Domain. Dont skip any skills if present in the text and give all the skills. Dont give the language proficiency and if it is attached to the language remove the language proficiency and give only the language. If there is no details about Courses and Certifications in the text dont assign anything. Dont try to assign extra details which is not present in the text and try to extract details from the text. Dont assign any extra keys which is not mentioned and dont extract any extra information that is not mentioned in the prompt. The Work Domain should have only the domain, it should not have technologies, skills, tools and roles played in it strictly dont assign those. The final data should not be changed. The final order needs to show all the keys. The final data should not have escape characters. Use the list datatype for multiple values only. Give the Final data in the indented form. If there is no domain in the extracted text at that time give only one work domain strictly from the text extracted, dont give more than one work domain strictly. The list is very important for multiple values so dont try to skip list datatypes for multiple values and the list datatypes is compulsory. Extract the work domain from the domain section of the text extracted only. Assign NOT AVAILABLE for empty details. Compulsorily assign list datatype for the keys having multiple values in the Project Technologies, Courses and Certification strictly if the Project section is present in the text extracted. Strictly dont assign anything if there is no Project related section in the text extracted. Assign only the work domain present in the text extracted not anything related to the Projects section. Strictly Complete the incomplete texts on your own compulsorily. The skills should contain only tool names, software names only. Dont change the final data for every iterations. It should be same for all the iterations strictly. The Work Domain should not contain roles like Automation Tester and those ending with tester, consultant, lead, etc and tools, technologies names also strictly. The Project Roles should have 4 to 5 words only. The Project Roles should not contain project description and responsibilities. Read the entire prompt command fully and strictly follow all those in the prompt. Dont assign anything unrelated in the final data strictly."""

def response_text(prompt):
    response = model.generate_content(prompt,request_options={"retry": retry.Retry(predicate=retry.if_transient_error)})
    return response.text

details = response_text(prompt)
print(details)

dict_data = json.loads(details)
print(dict_data)

with open("img_data7.json","w") as file1:
    file1.write(details)
    print("File Written Successfully...")

for file in genai.list_files():
    print(f"File Name: {file.name}")

print(f"File To Be Deleted: {file_uploaded.name}")
genai.delete_file(file_uploaded.name)
print("File Deleted Successfully...")

for file in genai.list_files():
    print(f"File Name: {file.name}")