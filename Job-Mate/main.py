import os  # Used for file handling
import pdfplumber  # Used for extracting text from PDF files
import re  # Used for regular expressions in text processing
import pandas as pd  # Used for data manipulation and analysis
from tkinter import *  # Used for creating the GUI
from tkinter import filedialog, font, messagebox  # Additional Tkinter widgets
from tkinter.scrolledtext import ScrolledText  # Provides a scrollable text widget
from PIL import ImageGrab, Image, ImageDraw, ImageTk  # Used for image handling, including screenshot capture
import matplotlib.pyplot as plt  # Used for creating visualizations
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Embeds Matplotlib plots in Tkinter
import numpy as np  # Used for numerical operations
from tkinter import ttk, Toplevel  # Provides additional Tkinter widgets
import webbrowser  # Used to open LinkedIn profiles in a web browser
from tkinter import Canvas, Scrollbar, Frame # For scrollable frames
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.font import Font
# Global variable for resume path
resume_path = None

# Configuration data for skill extraction
config_data = {
    "experience_keywords": [
        "Experience", "Work Experience", "Professional Experience", "Role", "Position"
    ],
    "certification_keywords": [
        "Certifications", "Certificates", "Achievements", "Awards", "Honors"
    ],
    "skill_keywords": [
        # Technical Skills (Data Science, AI & ML)
        "Python", "SQL", "Machine Learning", "Deep Learning", "Data Science",
        "Data Analysis", "Natural Language Processing", "Statistics",
        "TensorFlow", "Keras", "PyTorch", "Pandas", "NumPy", "Scikit-learn",
        "Matplotlib", "Seaborn", "Big Data", "Hadoop", "Spark", "Data Visualization",
        "Power BI", "Tableau", "MATLAB", "SAS", "SPSS", "Jupyter", "Google Colab",
        "Cloud Computing", "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes",
        "Git", "GitHub", "Bitbucket", "CI/CD", "Linux", "Unix",
        "Data Engineering", "ETL", "PostgreSQL", "NoSQL", "MongoDB",
        "Data Wrangling", "Feature Engineering", "Model Deployment", "ML Ops",
        "REST API", "Time Series Analysis", "Anomaly Detection",
        "Recommendation Systems", "Clustering", "Classification", "Regression",
        "Dimensionality Reduction", "PCA", "Hyperparameter Tuning",

        # Business & Management Skills
        "Team Management", "Communication", "Project Management", "Agile",
        "Scrum", "Kanban", "Business Analysis", "Process Improvement",
        "Change Management", "Supply Chain Management", "Financial Analysis",
        "Accounting", "Budgeting", "Forecasting", "Risk Management",
        "Strategic Planning", "Marketing Strategy", "Content Marketing",
        "Digital Marketing", "Social Media Marketing", "Email Marketing",
        "Google Analytics", "Market Research", "Customer Relationship Management",
        "CRM", "Public Relations", "Negotiation", "Salesforce", "HubSpot",
        "Event Planning", "Product Management", "Operations Management",
        "Logistics", "Vendor Management", "Procurement", "Inventory Management",

        # Creative & Design Skills
        "Graphic Design", "UI/UX Design", "Photoshop", "Illustrator", "InDesign",
        "Figma", "Sketch", "Adobe XD", "3D Modeling", "Animation", "Video Editing",
        "After Effects", "Final Cut Pro", "Lightroom", "Canva", "Digital Illustration",
        "Photography", "Content Creation", "Copywriting", "Blogging", "Creative Writing",
        "Storytelling", "Script Writing", "Branding",

        # Data & Analytical Tools
        "Econometrics", "Quantitative Analysis", "Qualitative Analysis", "Excel",
        "Pivot Tables", "Power Pivot", "VBA", "Stata", "SQL Queries", "Data Mining",
        "Predictive Analytics", "Business Intelligence", "Survey Analysis",
        "Hypothesis Testing", "A/B Testing",

        # Soft Skills
        "Leadership", "Critical Thinking", "Problem Solving", "Adaptability",
        "Time Management", "Decision Making", "Conflict Resolution",
        "Emotional Intelligence", "Empathy", "Stress Management", "Collaboration",
        "Active Listening", "Flexibility", "Resilience", "Creativity",
        "Attention to Detail", "Self-Motivation", "Work Ethic", "Teamwork",
        "Networking", "Interpersonal Skills", "Persuasion", "Public Speaking",
        "Presentation Skills",

        # Tools & Miscellaneous
        "MS Office", "Google Workspace", "Microsoft Excel", "Microsoft Word",
        "Microsoft PowerPoint", "Microsoft Project", "Microsoft Access", "QuickBooks",
        "Trello", "Slack", "Notion", "Airtable", "Zoom", "Web Development",
        "Mobile Development", "Customer Service", "Technical Support",
        "Quality Assurance", "Lean Six Sigma", "Sales", "Event Coordination",
        "E-commerce", "Retail Management", "SAP ERP", "Human Resources",
        "Recruiting", "Training and Development", "Legal Research",
        "Contract Negotiation", "Telecommunications", "Healthcare Management",
        "Clinical Research", "Pharmaceuticals"
    ]
}

# Job roles and their required skills for matching
job_roles = {
    "Data Scientist": [
        "Python", "R", "SQL", "Machine Learning", "Deep Learning", "Data Analysis",
        "Statistics", "TensorFlow", "Keras", "Scikit-learn", "Big Data", "Spark",
        "Data Visualization", "Pandas", "NumPy", "Data Wrangling", "Cloud Computing",
        "Model Deployment", "ML Ops", "Git", "Linux"
    ],
    "Business Analyst": [
        "Business Analysis", "Process Improvement", "SQL", "Excel", "Power BI",
        "Tableau", "Data Visualization", "Market Research", "Google Analytics",
        "Communication", "Stakeholder Management", "Requirements Gathering",
        "Problem Solving", "Hypothesis Testing", "A/B Testing"
    ],
    "Machine Learning Engineer": [
        "Python", "TensorFlow", "Keras", "PyTorch", "Machine Learning",
        "Deep Learning", "Model Deployment", "Cloud Computing", "Docker",
        "Kubernetes", "Data Engineering", "Feature Engineering", "Statistics",
        "ML Ops", "REST API", "Big Data", "Spark", "Git", "CI/CD"
    ],
    "UI/UX Designer": [
        "UI/UX Design", "Figma", "Adobe XD", "Sketch", "InDesign", "Photoshop",
        "Illustrator", "Wireframing", "Prototyping", "User Research",
        "Graphic Design", "Branding", "Communication", "Attention to Detail",
        "Creative Thinking"
    ],
    "Project Manager": [
        "Project Management", "Agile", "Scrum", "Kanban", "Leadership",
        "Communication", "Team Management", "Risk Management", "Strategic Planning",
        "Stakeholder Management", "Problem Solving", "Budgeting", "Change Management",
        "Decision Making", "Time Management"
    ],
    "DevOps Engineer": [
        "Linux", "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud",
        "CI/CD", "Git", "Jenkins", "Terraform", "Python", "Bash", "Monitoring",
        "Cloud Computing", "Automation", "Scripting"
    ],
    "Digital Marketer": [
        "Digital Marketing", "Social Media Marketing", "Content Marketing",
        "Email Marketing", "SEO", "Google Analytics", "Marketing Strategy",
        "Copywriting", "Public Relations", "Content Creation", "Campaign Management",
        "Graphic Design", "Communication", "Creative Thinking"
    ]
}

# Global variable to store multiple resume paths
resume_files = []

# Toggle custom skills entry state
def toggle_custom_skills(var, entry):
    if var.get():
        entry.config(state=NORMAL)
    else:
        entry.config(state=DISABLED)

# Add resume file
def add_resume_file(listbox):
    files = filedialog.askopenfilenames(
        initialdir="/", 
        title="Select Resume Files", 
        filetypes=(("PDF files", "*.pdf"), ("Word files", "*.docx"))
    )
    
    if files:
        for file in files:
            # Check if file already exists in the list
            if file not in resume_files:
                resume_files.append(file)
                listbox.insert(END, os.path.basename(file))

# Remove selected file
def remove_selected_file(listbox):
    selected = listbox.curselection()
    if selected:
        # Remove from display and global list
        for index in selected[::-1]:  # Reverse to avoid index shifting issues
            file_to_remove = resume_files[index]
            resume_files.pop(index)
            listbox.delete(index)


def analyze_multiple_resumes(job_role, use_custom_skills, custom_skills_text, files_listbox):
    # Check if any files are uploaded
    if not resume_files:
        messagebox.showerror("Error", "Please upload at least one resume file.")
        return
    
    # Get skills for comparison
    if use_custom_skills and custom_skills_text.strip():
        # Parse custom skills (comma separated)
        benchmark_skills = [skill.strip() for skill in custom_skills_text.split(',') if skill.strip()]
    else:
        # Use predefined skills for selected job role
        benchmark_skills = job_roles.get(job_role, [])
    
    if not benchmark_skills:
        messagebox.showerror("Error", "No skills defined for comparison.")
        return
    
    # Parse all resumes and calculate matches
    candidate_matches = []
    
    for resume_file in resume_files:
        try:
            parsed_data = parse_resume(resume_file)
            candidate_name = os.path.basename(resume_file).split('.')[0]  # Use filename as name
            skills = parsed_data.get('skills', [])
            experience = parsed_data.get('experience', 'No experience details found')
            certifications = parsed_data.get('certifications', 'No certifications found')
            
            # Calculate match percentage
            match_percentage = calculate_job_role_match(skills, benchmark_skills)
            
            # Calculate interview readiness
            readiness_score = calculate_interview_readiness(experience, certifications, skills)
            if isinstance(readiness_score, str) and '%' in readiness_score:
                readiness_score = float(readiness_score.replace('%', ''))
            
            candidate_matches.append({
                'name': candidate_name,
                'file': resume_file,
                'match_percentage': match_percentage,
                'skills': skills,
                'readiness_score': readiness_score
            })
            
        except Exception as e:
            print(f"Error processing {os.path.basename(resume_file)}: {e}")
    
    # Sort candidates by match percentage (descending)
    candidate_matches.sort(key=lambda x: x['match_percentage'], reverse=True)
    
    # Display results
    show_candidate_comparison(candidate_matches, job_role, benchmark_skills)


def show_candidate_comparison(candidates, job_role, benchmark_skills):
    if not candidates:
        messagebox.showerror("Error", "No valid candidate data to display.")
        return
    
    # Create comparison window
    results = Tk()
    results.title(f"Candidate Comparison for {job_role}")
    results.geometry("1200x700")
    results.configure(bg='#f5f5f5')
    
    # Banner
    banner_frame = Frame(results, height=100, bg='#1976D2')
    banner_frame.pack(fill="x", pady=(0, 20))
    
    banner_label = Label(banner_frame, text=f"Top Candidates for {job_role}", 
                       foreground='white', bg='#1976D2', font=("Helvetica", 24, "bold"))
    banner_label.place(relx=0.5, rely=0.5, anchor='center')
    
    # Main content frame with scrolling
    container = Frame(results)
    container.pack(fill="both", expand=True, padx=20, pady=10)
    
    canvas = Canvas(container, bg='#f5f5f5')
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    
    scrollable_frame = Frame(canvas, bg='#f5f5f5')
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Summary stats frame
    stats_frame = Frame(scrollable_frame, bg='white', relief="raised", bd=1)
    stats_frame.pack(fill="x", pady=10, padx=10)
    
    # Number of candidates label
    Label(stats_frame, text=f"Total Candidates: {len(candidates)}", 
        bg='white', font=("Helvetica", 12, "bold"), fg='#333').pack(anchor='w', padx=20, pady=10)
    
    # Average match percentage
    avg_match = sum(c['match_percentage'] for c in candidates) / len(candidates)
    Label(stats_frame, text=f"Average Match: {avg_match:.1f}%", 
        bg='white', font=("Helvetica", 12, "bold"), fg='#333').pack(anchor='w', padx=20, pady=5)
    
    # Top candidate label with green highlight
    if candidates:
        top_candidate_frame = Frame(stats_frame, bg='#E8F5E9', relief="raised", bd=0)
        top_candidate_frame.pack(fill="x", padx=20, pady=10)
        Label(top_candidate_frame, text=f"Top Candidate: {candidates[0]['name']} ({candidates[0]['match_percentage']:.1f}%)", 
            bg='#E8F5E9', font=("Helvetica", 14, "bold"), fg='#2E7D32').pack(anchor='w', padx=10, pady=10)
    
    # Grid layout for candidate comparison
    comparison_frame = Frame(scrollable_frame, bg='white', relief="raised", bd=1)
    comparison_frame.pack(fill="both", expand=True, pady=10, padx=10)
    
    # Headers
    headers = ["Rank", "Candidate", "Match %", "Skills Match", "Interview Readiness"]
    header_bg = '#E3F2FD'
    header_fg = '#0D47A1'
    
    for col, header in enumerate(headers):
        Label(comparison_frame, text=header, bg=header_bg, fg=header_fg, 
            font=("Helvetica", 12, "bold"), padx=10, pady=5).grid(row=0, column=col, sticky="ew")
    
    # Set column weights
    comparison_frame.grid_columnconfigure(0, weight=1)  # Rank
    comparison_frame.grid_columnconfigure(1, weight=3)  # Candidate
    comparison_frame.grid_columnconfigure(2, weight=2)  # Match %
    comparison_frame.grid_columnconfigure(3, weight=4)  # Skills Match
    comparison_frame.grid_columnconfigure(4, weight=2)  # Interview Readiness
    comparison_frame.grid_columnconfigure(5, weight=2)  # Actions
    
    # Add candidate rows
    row_colors = ['#FFFFFF', '#F5F5F5']  # Alternating row colors
    
    for i, candidate in enumerate(candidates):
        row = i + 1
        bg_color = row_colors[i % 2]
        
        # Style match percentage based on value
        if candidate['match_percentage'] >= 75:
            match_color = '#4CAF50'  # Green
        elif candidate['match_percentage'] >= 50:
            match_color = '#FF9800'  # Orange
        else:
            match_color = '#F44336'  # Red
        
        # Rank
        Label(comparison_frame, text=f"{row}", bg=bg_color, fg='#333',
            font=("Helvetica", 12), padx=10, pady=8).grid(row=row, column=0, sticky="ew")
        
        # Candidate name
        Label(comparison_frame, text=candidate['name'], bg=bg_color, fg='#333',
            font=("Helvetica", 12), padx=10, pady=8).grid(row=row, column=1, sticky="ew")
        
        # Match percentage
        Label(comparison_frame, text=f"{candidate['match_percentage']:.1f}%", bg=bg_color, fg=match_color,
            font=("Helvetica", 12, "bold"), padx=10, pady=8).grid(row=row, column=2, sticky="ew")
        
        # Skills match info
        matched_skills = set(candidate['skills']) & set(benchmark_skills)
        missing_skills = set(benchmark_skills) - set(candidate['skills'])
        
        skills_text = f"{len(matched_skills)} of {len(benchmark_skills)} required skills"
        Label(comparison_frame, text=skills_text, bg=bg_color, fg='#333',
            font=("Helvetica", 12), padx=10, pady=8).grid(row=row, column=3, sticky="ew")
        
        # Interview readiness
        readiness_text = f"{candidate['readiness_score']:.1f}%" if isinstance(candidate['readiness_score'], (int, float)) else candidate['readiness_score']
        Label(comparison_frame, text=readiness_text, bg=bg_color, fg='#333',
            font=("Helvetica", 12), padx=10, pady=8).grid(row=row, column=4, sticky="ew")
        
        # # View button
        # action_frame = Frame(comparison_frame, bg=bg_color)
        # action_frame.grid(row=row, column=5, sticky="ew", padx=5)
        
        # view_button = Button(action_frame, text="View Details", 
        #                    command=lambda c=candidate, j=job_role, b=benchmark_skills: view_candidate_details(c, j, b),
        #                    bg='#E3F2FD', fg='#1976D2', font=("Helvetica", 10),
        #                    relief="flat", padx=5, pady=2)
        # view_button.pack(pady=3)
    
    # Button frame
    button_frame = Frame(results, bg='#f5f5f5')
    button_frame.pack(pady=15)
    
    # Export results button
    # export_button = Button(button_frame, text="Export Results", 
    #                      command=lambda: export_comparison_results(candidates, job_role, benchmark_skills),
    #                      bg='#1976D2', fg='white', font=("Helvetica", 12, "bold"),
    #                      padx=15, pady=8, relief="flat")
    # export_button.pack(side=LEFT, padx=10)
    
    # View charts button
    charts_button = Button(button_frame, text="View Analytics", 
                         command=lambda: show_comparison_charts(candidates, job_role, benchmark_skills),
                         bg='#4CAF50', fg='black', font=("Helvetica", 12, "bold"),
                         padx=15, pady=8, relief="flat")
    charts_button.pack(side=LEFT, padx=10)
    
    # Back button
    back_button = Button(button_frame, text="Back", 
                       command=results.destroy,
                       bg='#F5F5F5', fg='#555555', font=("Helvetica", 12),
                       padx=15, pady=8, relief="flat")
    back_button.pack(side=LEFT, padx=10)
    
    # Center the window
    results.update_idletasks()
    width = results.winfo_width()
    height = results.winfo_height()
    x = (results.winfo_screenwidth() // 2) - (width // 2)
    y = (results.winfo_screenheight() // 2) - (height // 2)
    results.geometry(f'{width}x{height}+{x}+{y}')
    
    results.mainloop()

def view_candidate_details(candidate, job_role, benchmark_skills):
    # Create a new window for candidate details
    detail_window = Toplevel()
    detail_window.title(f"Candidate Details: {candidate['name']}")
    detail_window.geometry("800x600")
    detail_window.configure(bg='white')
    
    # Similar to job_recommendation function but tailored for a single candidate
    # from the recruiter's perspective
    # ...
    # (implement similar to job_recommendation but for a single candidate)

def show_comparison_charts(candidates, job_role, benchmark_skills):
    # Create a window with comparative analytics
    chart_window = Toplevel()
    chart_window.title(f"Candidate Comparison Analytics for {job_role}")
    chart_window.geometry("1000x700")
    chart_window.configure(bg='#f5f5f5')
    
    # Canvas for scrolling if needed
    # ...
    
    # Chart 1: Match percentage comparison
    fig1 = plt.figure(figsize=(10, 5))
    ax1 = fig1.add_subplot(111)
    
    names = [c['name'] for c in candidates[:10]]  # Top 10
    matches = [c['match_percentage'] for c in candidates[:10]]
    
    bars = ax1.bar(names, matches, color='skyblue')
    
    # Highlight the top candidate
    if bars:
        bars[0].set_color('#4CAF50')
    
    ax1.set_xlabel('Candidates')
    ax1.set_ylabel('Match Percentage')
    ax1.set_title('Top Candidates by Job Role Match')
    ax1.set_ylim(0, 100)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    chart1_frame = Frame(chart_window, bg='white', relief="raised", bd=1)
    chart1_frame.pack(fill="x", padx=20, pady=20)
    
    canvas1 = FigureCanvasTkAgg(fig1, master=chart1_frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill="both", expand=True)
    
    # Chart 2: Skills distribution among candidates
    # ...
    
    # Chart 3: Interview readiness comparison
    # ...
    
    # Button to close
    Button(chart_window, text="Close", command=chart_window.destroy,
         bg='#F5F5F5', fg='#555555', font=("Helvetica", 12),
         padx=15, pady=8, relief="flat").pack(pady=15)


from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

def show_recruiter_form():
    form = Tk()
    form.geometry("750x700")
    form.configure(background='#f5f5f5')
    form.title("Recruiter Mode - Job Role Match Finder")
    form.option_add("*Font", "Helvetica 12")

    # Create canvas and scrollbar for scrolling
    canvas = Canvas(form, bg="#f5f5f5", highlightthickness=0)
    scrollbar = Scrollbar(form, orient=VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Create a frame inside canvas
    main_frame = Frame(canvas, bg="#f5f5f5")
    canvas.create_window((0, 0), window=main_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    main_frame.bind("<Configure>", on_configure)

    # Now pack all your UI components inside main_frame
    # --- Below here is exactly your code, unchanged, except "form" → "main_frame" ---

    banner_frame = Frame(main_frame, height=120, bg='#1976D2')
    banner_frame.pack(fill="x", pady=(0, 25))

    logo_frame = Frame(banner_frame, bg='#1976D2', width=80, height=80)
    logo_frame.place(relx=0.1, rely=0.5, anchor='center')
    Label(logo_frame, text="JM", font=("Helvetica", 28, "bold"), fg='white', bg='#2196F3',
          width=3, height=1, relief="raised", borderwidth=2).pack(padx=5, pady=5)

    banner_label = Label(banner_frame, text="RECRUITER DASHBOARD", foreground='white', bg='#1976D2',
                         font=("Helvetica", 28, "bold"))
    banner_label.place(relx=0.5, rely=0.5, anchor='center')

    tagline = Label(main_frame, text="Find the best candidate match for your job role",
                    fg='#555555', bg='#f5f5f5', font=("Helvetica", 12, "italic"))
    tagline.pack(pady=(0, 10))

    card_frame = Frame(main_frame, bg='white', relief="raised", borderwidth=1)
    card_frame.pack(fill="both", expand=True, padx=40, pady=20)

    input_frame = Frame(card_frame, background='white', padx=30, pady=25)
    input_frame.pack(fill="both", expand=True)

    form_title = Label(input_frame, text="Job Requirements", foreground='#1976D2', bg='white',
                       font=("Helvetica", 18, "bold"))
    form_title.grid(row=0, column=0, columnspan=2, pady=(0, 8), sticky="w")

    separator = Frame(input_frame, height=2, bg='#2196F3')
    separator.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 25))

    Label(input_frame, text="Select Job Role", foreground='#555555', bg='white',
          font=("Helvetica", 12, "bold")).grid(row=2, column=0, sticky="w", pady=12)

    job_role_var = StringVar()
    job_roles_list = list(job_roles.keys())
    job_role_var.set(job_roles_list[0])

    job_dropdown_frame = Frame(input_frame, bg='white')
    job_dropdown_frame.grid(row=2, column=1, sticky="w", pady=12)

    job_dropdown = ttk.Combobox(job_dropdown_frame, textvariable=job_role_var,
                                values=job_roles_list, font=("Helvetica", 12),
                                width=30, state="readonly")
    job_dropdown.pack(fill="x", ipady=4)

    custom_skills_var = BooleanVar()
    custom_skills_var.set(False)

    custom_frame = Frame(input_frame, bg='white')
    custom_frame.grid(row=3, column=0, columnspan=2, sticky="w", pady=12)

    custom_check = Checkbutton(custom_frame, text="Add Custom Skills", variable=custom_skills_var,
                               command=lambda: toggle_custom_skills(custom_skills_var, custom_skills_entry),
                               bg='white', fg='#555555', font=("Helvetica", 12, "bold"),
                               activebackground='white', activeforeground='#1976D2')
    custom_check.pack(side=LEFT)

    custom_skills_entry = ScrolledText(input_frame, height=3, width=40, font=("Helvetica", 12),
                                       state=DISABLED)
    custom_skills_entry.grid(row=4, column=0, columnspan=2, sticky="ew", pady=12)

    upload_title = Label(input_frame, text="Upload Candidate Resumes", foreground='#1976D2', bg='white',
                         font=("Helvetica", 16, "bold"))
    upload_title.grid(row=5, column=0, columnspan=2, pady=(20, 8), sticky="w")

    upload_separator = Frame(input_frame, height=2, bg='#2196F3')
    upload_separator.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 15))

    uploaded_files_frame = Frame(input_frame, bg='white', relief="groove", bd=1)
    uploaded_files_frame.grid(row=7, column=0, columnspan=2, sticky="ew", pady=12)
    uploaded_files_frame.grid_columnconfigure(0, weight=1)

    uploaded_files_listbox = Listbox(uploaded_files_frame, height=8, width=70,
                                     font=("Helvetica", 10), selectbackground='#BBDEFB')
    uploaded_files_listbox.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

    listbox_scrollbar = Scrollbar(uploaded_files_frame)
    listbox_scrollbar.pack(side=RIGHT, fill=Y)
    uploaded_files_listbox.config(yscrollcommand=listbox_scrollbar.set)
    listbox_scrollbar.config(command=uploaded_files_listbox.yview)

    upload_buttons_frame = Frame(input_frame, bg='white')
    upload_buttons_frame.grid(row=8, column=0, columnspan=2, pady=15)

    upload_button = Button(upload_buttons_frame, text="Add Resume",
                           command=lambda: add_resume_file(uploaded_files_listbox),
                           font=("Helvetica", 12), bg='#E3F2FD', fg='#1976D2',
                           activebackground='#BBDEFB', activeforeground='#1976D2',
                           padx=15, pady=8, relief="flat", borderwidth=0)
    upload_button.pack(side=LEFT, padx=(0, 10))

    remove_button = Button(upload_buttons_frame, text="Remove Selected",
                           command=lambda: remove_selected_file(uploaded_files_listbox),
                           font=("Helvetica", 12), bg='#FFEBEE', fg='#D32F2F',
                           activebackground='#FFCDD2', activeforeground='#D32F2F',
                           padx=15, pady=8, relief="flat", borderwidth=0)
    remove_button.pack(side=LEFT)

    button_frame = Frame(input_frame, bg='white')
    button_frame.grid(row=9, column=0, columnspan=2, pady=25)

    analyze_button = Button(button_frame, text="Analyze Candidates",
                            command=lambda: analyze_multiple_resumes(job_role_var.get(),
                                                                     custom_skills_var.get(),
                                                                     custom_skills_entry.get("1.0", END),
                                                                     uploaded_files_listbox),
                            font=("Helvetica", 14, "bold"), bg='#1976D2', fg='black',
                            activebackground='#0D47A1', activeforeground='white',
                            padx=20, pady=10, relief="flat", borderwidth=0)
    analyze_button.pack(side=LEFT, padx=(0, 15))

    back_button = Button(button_frame, text="Back",
                         command=lambda: [form.destroy(), show_entrance_screen()],
                         font=("Helvetica", 14), bg='#F5F5F5', fg='#555555',
                         activebackground='#E0E0E0', activeforeground='#333333',
                         padx=20, pady=10, relief="flat", borderwidth=0)
    back_button.pack(side=LEFT)

    upload_button.bind("<Enter>", lambda e: e.widget.config(background='#BBDEFB'))
    upload_button.bind("<Leave>", lambda e: e.widget.config(background='#E3F2FD'))
    remove_button.bind("<Enter>", lambda e: e.widget.config(background='#FFCDD2'))
    remove_button.bind("<Leave>", lambda e: e.widget.config(background='#FFEBEE'))
    analyze_button.bind("<Enter>", lambda e: e.widget.config(background='#1565C0'))
    analyze_button.bind("<Leave>", lambda e: e.widget.config(background='#1976D2'))
    back_button.bind("<Enter>", lambda e: e.widget.config(background='#E0E0E0'))
    back_button.bind("<Leave>", lambda e: e.widget.config(background='#F5F5F5'))

    # footer = Label(main_frame, text="©️ 2025 Resume Analyzer - All Rights Reserved",
    #                fg='#777777', bg='#f5f5f5', font=("Helvetica", 10))
    # footer.pack(pady=15)

    form.mainloop()

from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

def show_recruiter_form():
    form = Tk()
    form.geometry("750x700")
    form.configure(background='#f5f5f5')
    form.title("Recruiter Mode - Job Role Match Finder")
    form.option_add("*Font", "Helvetica 12")

    # Create canvas and scrollbar
    canvas = Canvas(form, borderwidth=0, background="#f5f5f5")
    scrollbar = Scrollbar(form, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Create main frame inside canvas
    main_frame = Frame(canvas, background="#f5f5f5")
    canvas.create_window((0, 0), window=main_frame, anchor='nw')

    # Scroll event binding
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    main_frame.bind("<Configure>", on_frame_configure)

    # --- Now use main_frame instead of form below ---
    banner_frame = Frame(main_frame, height=120, bg='#1976D2')
    banner_frame.pack(fill="x", pady=(0, 25))

    logo_frame = Frame(banner_frame, bg='#1976D2', width=80, height=80)
    logo_frame.place(relx=0.1, rely=0.5, anchor='center')
    Label(logo_frame, text="JM", font=("Helvetica", 28, "bold"), fg='white', bg='#2196F3',
          width=3, height=1, relief="raised", borderwidth=2).pack(padx=5, pady=5)

    Label(banner_frame, text="RECRUITER DASHBOARD", foreground='white', bg='#1976D2',
          font=("Helvetica", 28, "bold")).place(relx=0.5, rely=0.5, anchor='center')

    tagline = Label(main_frame, text="Find the best candidate match for your job role",
                    fg='#555555', bg='#f5f5f5', font=("Helvetica", 12, "italic"))
    tagline.pack(pady=(0, 10))

    card_frame = Frame(main_frame, bg='white', relief="raised", borderwidth=1)
    card_frame.pack(fill="both", expand=True, padx=40, pady=20)

    input_frame = Frame(card_frame, background='white', padx=30, pady=25)
    input_frame.pack(fill="both", expand=True)

    Label(input_frame, text="Job Requirements", foreground='#1976D2', bg='white',
          font=("Helvetica", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 8), sticky="w")
    Frame(input_frame, height=2, bg='#2196F3').grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 25))

    Label(input_frame, text="Select Job Role", fg='#555555', bg='white',
          font=("Helvetica", 12, "bold")).grid(row=2, column=0, sticky="w", pady=12)

    job_role_var = StringVar()
    job_roles_list = list(job_roles.keys())
    job_role_var.set(job_roles_list[0])

    job_dropdown = ttk.Combobox(input_frame, textvariable=job_role_var, values=job_roles_list,
                                font=("Helvetica", 12), width=30, state="readonly")
    job_dropdown.grid(row=2, column=1, sticky="w", pady=12)

    custom_skills_var = BooleanVar(value=False)
    custom_check = Checkbutton(input_frame, text="Add Custom Skills", variable=custom_skills_var,
                               command=lambda: toggle_custom_skills(custom_skills_var, custom_skills_entry),
                               bg='white', fg='#555555', font=("Helvetica", 12, "bold"),
                               activebackground='white', activeforeground='#1976D2')
    custom_check.grid(row=3, column=0, columnspan=2, sticky="w", pady=12)

    custom_skills_entry = ScrolledText(input_frame, height=3, width=40, font=("Helvetica", 12), state=DISABLED)
    custom_skills_entry.grid(row=4, column=0, columnspan=2, sticky="ew", pady=12)

    Label(input_frame, text="Upload Candidate Resumes", foreground='#1976D2', bg='white',
          font=("Helvetica", 16, "bold")).grid(row=5, column=0, columnspan=2, pady=(20, 8), sticky="w")
    Frame(input_frame, height=2, bg='#2196F3').grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 15))

    uploaded_files_frame = Frame(input_frame, bg='white', relief="groove", bd=1)
    uploaded_files_frame.grid(row=7, column=0, columnspan=2, sticky="ew", pady=12)
    uploaded_files_frame.grid_columnconfigure(0, weight=1)

    uploaded_files_listbox = Listbox(uploaded_files_frame, height=8, width=70, font=("Helvetica", 10), selectbackground='#BBDEFB')
    uploaded_files_listbox.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

    listbox_scrollbar = Scrollbar(uploaded_files_frame)
    listbox_scrollbar.pack(side=RIGHT, fill=Y)
    uploaded_files_listbox.config(yscrollcommand=listbox_scrollbar.set)
    listbox_scrollbar.config(command=uploaded_files_listbox.yview)

    upload_buttons_frame = Frame(input_frame, bg='white')
    upload_buttons_frame.grid(row=8, column=0, columnspan=2, pady=15)

    upload_button = Button(upload_buttons_frame, text="Add Resume",
                           command=lambda: add_resume_file(uploaded_files_listbox),
                           font=("Helvetica", 12), bg='#E3F2FD', fg='#1976D2',
                           activebackground='#BBDEFB', activeforeground='#1976D2',
                           padx=15, pady=8, relief="flat", borderwidth=0)
    upload_button.pack(side=LEFT, padx=(0, 10))

    remove_button = Button(upload_buttons_frame, text="Remove Selected",
                           command=lambda: remove_selected_file(uploaded_files_listbox),
                           font=("Helvetica", 12), bg='#FFEBEE', fg='#D32F2F',
                           activebackground='#FFCDD2', activeforeground='#D32F2F',
                           padx=15, pady=8, relief="flat", borderwidth=0)
    remove_button.pack(side=LEFT)

    button_frame = Frame(input_frame, bg='white')
    button_frame.grid(row=9, column=0, columnspan=2, pady=25)

    analyze_button = Button(button_frame, text="Analyze Candidates",
                            command=lambda: analyze_multiple_resumes(job_role_var.get(),
                                                                     custom_skills_var.get(),
                                                                     custom_skills_entry.get("1.0", END),
                                                                     uploaded_files_listbox),
                            font=("Helvetica", 14, "bold"), bg='#1976D2', fg='black',
                            activebackground='#0D47A1', activeforeground='white',
                            padx=20, pady=10, relief="flat", borderwidth=0)
    analyze_button.pack(side=LEFT, padx=(0, 15))

    back_button = Button(button_frame, text="Back",
                         command=lambda: [form.destroy(), show_entrance_screen()],
                         font=("Helvetica", 14), bg='#F5F5F5', fg='#555555',
                         activebackground='#E0E0E0', activeforeground='#333333',
                         padx=20, pady=10, relief="flat", borderwidth=0)
    back_button.pack(side=LEFT)

    # footer = Label(main_frame, text="©️ 2025 Resume Analyzer - All Rights Reserved",
    #                fg='#777777', bg='#f5f5f5', font=("Helvetica", 10))
    # footer.pack(pady=15)

    form.mainloop()

def show_entrance_screen():
    entrance = Tk()
    entrance.geometry("550x400")
    entrance.configure(background='#f5f5f5')
    entrance.title("Job Mate - Resume Analyzer")
    
    # Banner with gradient effect
    banner_frame = Frame(entrance, height=100, bg='#2E7D32')
    banner_frame.pack(fill="x", pady=(0, 25))
    
    # Add logo placeholder
    logo_frame = Frame(banner_frame, bg='#2E7D32', width=80, height=80)
    logo_frame.place(relx=0.1, rely=0.5, anchor='center')
    Label(logo_frame, text="JM", font=("Helvetica", 28, "bold"), fg='white', bg='#4CAF50', 
          width=3, height=1, relief="raised", borderwidth=2).pack(padx=5, pady=5)
    
    banner_label = Label(banner_frame, text="JOB MATE", foreground='white', bg='#2E7D32', 
                         font=("Helvetica", 28, "bold"))
    banner_label.place(relx=0.5, rely=0.5, anchor='center')
    
    # Add a tagline
    tagline = Label(entrance, text="Select Your Role", 
                    fg='#555555', bg='#f5f5f5', font=("Helvetica", 16, "bold"))
    tagline.pack(pady=(10, 30))
    
    # Button frame
    button_frame = Frame(entrance, bg='#f5f5f5')
    button_frame.pack(pady=20)
    
    # Student button
    student_button = Button(button_frame, text="Student / Job Seeker", 
                         command=lambda: [entrance.destroy(), show_job_form()], 
                         font=("Helvetica", 14, "bold"), bg='#4CAF50', fg='black', 
                         activebackground='#2E7D32', activeforeground='white',
                         padx=20, pady=15, relief="flat", borderwidth=0,
                         width=20)
    student_button.pack(pady=10)
    
    # Recruiter button
    recruiter_button = Button(button_frame, text="Recruiter / HR", 
                           command=lambda: [entrance.destroy(), show_recruiter_form()], 
                           font=("Helvetica", 14, "bold"), bg='#1976D2', fg='black', 
                           activebackground='#0D47A1', activeforeground='white',
                           padx=20, pady=15, relief="flat", borderwidth=0,
                           width=20)
    recruiter_button.pack(pady=10)
    
    # Add hover effects
    student_button.bind("<Enter>", lambda e: e.widget.config(background='#388E3C'))
    student_button.bind("<Leave>", lambda e: e.widget.config(background='#4CAF50'))
    recruiter_button.bind("<Enter>", lambda e: e.widget.config(background='#1565C0'))
    recruiter_button.bind("<Leave>", lambda e: e.widget.config(background='#1976D2'))
    
    # Add a footer
    # footer = Label(entrance, text="©️ 2025 Resume Analyzer - All Rights Reserved", 
    #              fg='#777777', bg='#f5f5f5', font=("Helvetica", 10))
    # footer.pack(side=BOTTOM, pady=15)
    
    # Center the window on screen
    entrance.update_idletasks()
    width = entrance.winfo_width()
    height = entrance.winfo_height()
    x = (entrance.winfo_screenwidth() // 2) - (width // 2)
    y = (entrance.winfo_screenheight() // 2) - (height // 2)
    entrance.geometry(f'{width}x{height}+{x}+{y}')
    
    entrance.mainloop()

# Parse resume function
def parse_resume(cv_path):
    parsed_data = {
        'mobile_number': 'Not found',
        'email': 'Not found',
        'skills': [],
        'certifications': 'Not found',
        'degree': 'Not found',
        'experience': 'Not found',
    }

    with pdfplumber.open(cv_path) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Extract email and phone number
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\b\d{10}\b'

    email_match = re.search(email_pattern, text)
    phone_match = re.search(phone_pattern, text)

    if email_match:
        parsed_data['email'] = email_match.group(0)
    if phone_match:
        parsed_data['mobile_number'] = phone_match.group(0)

    # Extract skills based on keywords from config_data
    parsed_data['skills'] = [skill for skill in config_data["skill_keywords"] if skill.lower() in text.lower()]

    # Degree extraction (simplified)
    if "B.Tech" in text or "Bachelor" in text:
        parsed_data['degree'] = "Bachelor's Degree"
    elif "M.Tech" in text or "Master" in text:
        parsed_data['degree'] = "Master's Degree"
    elif "PhD" in text or "Doctorate" in text:
        parsed_data['degree'] = "Doctorate"

    # Enhanced certifications extraction with more flexible pattern
    cert_start_pattern = r'(' + '|'.join(config_data["certification_keywords"]) + r')(\s*[:\-]?)'
    cert_end_pattern = r'(Experience|Projects|Education|Skills|Languages|End)'
    cert_match = re.search(f"{cert_start_pattern}(.*?){cert_end_pattern}", text, re.DOTALL | re.IGNORECASE)
    if cert_match:
        certifications = cert_match.group(2).strip()
        certifications = re.sub(cert_start_pattern, '', certifications, flags=re.IGNORECASE).strip()
        parsed_data['certifications'] = certifications if certifications else "No certifications found"
    else:
        parsed_data['certifications'] = "No certifications found"

    # Enhanced experience extraction with more flexible pattern
    exp_start_pattern = r'(' + '|'.join(config_data["experience_keywords"]) + r')(\s*[:\-]?)'
    exp_end_pattern = r'(Education|Certifications|Projects|Skills|Languages|End)'
    exp_match = re.search(f"{exp_start_pattern}(.*?){exp_end_pattern}", text, re.DOTALL | re.IGNORECASE)
    if exp_match:
        experience = exp_match.group(2).strip()
        experience = re.sub(exp_start_pattern, '', experience, flags=re.IGNORECASE).strip()
        parsed_data['experience'] = experience if experience else "No experience details found"
    else:
        parsed_data['experience'] = "No experience details found"

    # Extract LinkedIn profile if available
    linkedin_pattern = r'(https?://[^\s]+linkedin\.com[^\s]*)'
    linkedin_match = re.search(linkedin_pattern, text)
    if linkedin_match:
        parsed_data['linkedin'] = linkedin_match.group(0)
    else:
        parsed_data['linkedin'] = None

    return parsed_data

# Function to open file dialog for resume selection
def OpenFile(button):
    global resume_path
    resume_path = filedialog.askopenfilename(
        initialdir="/", 
        title="Select Resume File", 
        filetypes=(("PDF files", "*.pdf"), ("Word files", "*.docx"))
    )
    if resume_path:
        button.config(text=os.path.basename(resume_path))

# Function to validate inputs
def validate_and_submit(entries, gender, cv_button, job_role_var):
    # Get values from entries
    name = entries[0].get()
    age = entries[1].get()
    selected_job = job_role_var.get()
    
    # Check if any fields are empty
    if not name or not age:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return
    
    # Validate age
    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid age.")
        return

    # Check if resume file is selected
    if not resume_path:
        messagebox.showerror("Input Error", "Please select a resume file.")
        return
    
    # Call job_recommendation with selected job role
    job_recommendation(None, entries[0], resume_path, (gender.get(), age), selected_job)

# Calculate the job role match percentage
def calculate_job_role_match(candidate_skills, job_role_skills):
    matched_skills = set(candidate_skills) & set(job_role_skills)  # Common skills
    total_skills = set(job_role_skills)  # All required skills
    match_percentage = (len(matched_skills) / len(total_skills)) * 100 if total_skills else 0
    return match_percentage

# Calculate interview readiness score
def calculate_interview_readiness(experience, certifications, skills):
    # Revised scoring system with additional criteria
    score = 0
    score += 25 if experience != "No experience details found" else 0
    score += 20 if certifications != "No certifications found" else 0
    score += min(len(skills) * 5, 50)  # Updated to cap skills score at 50

    # Additional soft skill weighting
    soft_skills = ["communication", "leadership", "teamwork", "problem solving", "critical thinking"]
    for skill in skills:
        if skill.lower() in soft_skills:
            score += 5
            break

    return f"{min(score, 100)}%"

def industry_benchmark_comparison(skills, top_job_role):
    # Convert input list to a set for easier comparison
    user_skills = set(skill.lower() for skill in skills)

    # Get the benchmark skills for the top job role
    required_skills = set(skill.lower() for skill in job_roles.get(top_job_role, []))
    
    # Analyze skill alignment with the top role
    missing = required_skills - user_skills
    
    if not missing:
        result = f"Your skills meet or exceed industry benchmarks for {top_job_role}."
    else:
        result = f"For {top_job_role}, consider gaining skills in: {', '.join(sorted(missing))}"

    return result

    
    
# Evaluate soft skills from resume
def evaluate_soft_skills(resume_text):
    # Enhanced evaluation with more soft skills keywords
    soft_skills_keywords = ["communication", "teamwork", "problem-solving", "adaptability", "leadership", "creativity"]
    matched_keywords = [skill for skill in soft_skills_keywords if skill.lower() in resume_text.lower()]
    if matched_keywords:
        return f"Shows strong skills in {', '.join(matched_keywords)}."
    else:
        return "Soft skills could not be evaluated from resume text."

# Create job role match chart
def create_job_role_match_chart(match_data):
    roles = list(match_data.keys())
    percentages = list(match_data.values())

    fig, ax = plt.subplots(figsize=(15, 4))
    ax.barh(roles, percentages, color='skyblue')
    ax.set_xlabel('Match Percentage')
    ax.set_title('Job Role Match')
    ax.set_xlim(0, 100)

    return fig

# Create skill comparison chart
def create_skill_comparison_chart(candidate_skills, benchmark_skills):
    fig, ax = plt.subplots(figsize=(4, 4))

    benchmark_set = set(benchmark_skills)
    candidate_set = set(candidate_skills)
    missing_skills = benchmark_set - candidate_set
    matched_skills = benchmark_set & candidate_set

    skills_data = {
        "Matched Skills": len(matched_skills),
        "Missing Skills": len(missing_skills)
    }   

    ax.bar(skills_data.keys(), skills_data.values(), color=['green', 'red'])
    ax.set_ylabel("Count")
    ax.set_title("Skill Comparison with Industry Benchmark")

    return fig

# Create interview readiness chart
def create_interview_readiness_chart(score):
    if isinstance(score, str) and '%' in score:
        score = float(score.replace('%', ''))
    
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie([score, 100 - score], labels=['Ready', 'Gap'], startangle=90, colors=['#4CAF50', '#FFC107'], 
           autopct='%1.1f%%', wedgeprops={'width': 0.3, 'edgecolor': 'white'})
    ax.set_title("Interview Readiness Score")

    return fig

# Show analysis charts
def show_charts(match_data, candidate_skills, benchmark_skills, readiness_score):
    try:
        # Ensure readiness_score is a float, removing percentage symbol if present
        if isinstance(readiness_score, str) and '%' in readiness_score:
            readiness_score = float(readiness_score.replace('%', ''))
        elif isinstance(readiness_score, str):
            readiness_score = float(readiness_score)
            
        # Create a new window for displaying all charts
        chart_window = Toplevel()
        chart_window.title("Candidate Skills Analysis Dashboard")
        chart_window.geometry("1200x700")  # Increased window size for better visibility
        chart_window.configure(bg="#f5f5f5")  # Light background for better contrast
        
        # Add a title at the top
        title_label = Label(chart_window, text="Skills Analysis Dashboard", 
                           font=("Helvetica", 18, "bold"), bg="#f5f5f5", fg="#333333")
        title_label.pack(side=TOP, pady=(15, 5))
        
        # Canvas and scrollbar setup for horizontal scrolling
        canvas = Canvas(chart_window, width=1180, height=550, bg="#f5f5f5", highlightthickness=0)
        canvas.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = Scrollbar(chart_window, orient=HORIZONTAL, command=canvas.xview)
        scrollbar.pack(side=BOTTOM, fill=X, padx=10)
        canvas.configure(xscrollcommand=scrollbar.set)
        
        # Create a frame within the canvas
        scrollable_frame = Frame(canvas, bg="#f5f5f5")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Configure the canvas to adjust scroll region based on the content
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Frame for holding buttons below the scrollable frame
        button_frame = Frame(chart_window, bg="#f5f5f5")
        button_frame.pack(side=BOTTOM, padx=20, pady=(0, 15), anchor='center')
        
        # Define common size for all chart boxes
        chart_width = 360
        chart_height = 450
        
        # Add charts in a row layout within the scrollable frame with equal sizes
        box1 = Frame(scrollable_frame, relief="solid", bd=2, bg="white", width=chart_width, height=chart_height)
        box1.grid(row=0, column=0, padx=15, pady=15, sticky='nsew')
        box1.pack_propagate(False)  # Prevent resizing due to content
        
        box2 = Frame(scrollable_frame, relief="solid", bd=2, bg="white", width=chart_width, height=chart_height)
        box2.grid(row=0, column=1, padx=15, pady=15, sticky='nsew')
        box2.pack_propagate(False)  # Prevent resizing due to content
        
        box3 = Frame(scrollable_frame, relief="solid", bd=2, bg="white", width=chart_width, height=chart_height)
        box3.grid(row=0, column=2, padx=15, pady=15, sticky='nsew')
        box3.pack_propagate(False)  # Prevent resizing due to content
        
        # Add chart titles
        Label(box1, text="Job Role Match Analysis", font=("Helvetica", 12, "bold"), bg="white").pack(pady=(10, 0))
        Label(box2, text="Skills Comparison", font=("Helvetica", 12, "bold"), bg="white").pack(pady=(10, 0))
        Label(box3, text="Interview Readiness", font=("Helvetica", 12, "bold"), bg="white").pack(pady=(10, 0))
        
        # Chart container frames to hold the actual charts
        chart_frame1 = Frame(box1, bg="white")
        chart_frame1.pack(fill=BOTH, expand=True, padx=10, pady=(5, 10))
        
        chart_frame2 = Frame(box2, bg="white")
        chart_frame2.pack(fill=BOTH, expand=True, padx=10, pady=(5, 10))
        
        chart_frame3 = Frame(box3, bg="white")
        chart_frame3.pack(fill=BOTH, expand=True, padx=10, pady=(5, 10))
        
        # Job Role Match Chart - Use original function without figsize
        job_role_fig = create_job_role_match_chart(match_data)
        # Adjust figure size after creation
        job_role_fig.set_size_inches(5, 5)
        job_role_fig.tight_layout()
        job_role_canvas = FigureCanvasTkAgg(job_role_fig, master=chart_frame1)
        job_role_canvas.draw()
        job_role_canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        # Skill Comparison Chart - Use original function without figsize
        skill_comparison_fig = create_skill_comparison_chart(candidate_skills, benchmark_skills)
        # Adjust figure size after creation
        skill_comparison_fig.set_size_inches(5, 5)
        skill_comparison_fig.tight_layout()
        skill_comparison_canvas = FigureCanvasTkAgg(skill_comparison_fig, master=chart_frame2)
        skill_comparison_canvas.draw()
        skill_comparison_canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        # Interview Readiness Donut Chart - Use original function without figsize
        readiness_fig = create_interview_readiness_chart(readiness_score)
        # Adjust figure size after creation
        readiness_fig.set_size_inches(5, 5)
        readiness_fig.tight_layout()
        readiness_canvas = FigureCanvasTkAgg(readiness_fig, master=chart_frame3)
        readiness_canvas.draw()
        readiness_canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        # Button styling function
        def create_button(parent, text, command, bg_color):
            return Button(
                parent, text=text, command=command,
                font=("Helvetica", 12),
                bg=bg_color, fg='white',
                padx=15, pady=8,
                relief="raised", bd=0,
                activebackground=bg_color,
                cursor="hand2",
                width=12
            )
        
        # Download Button with improved styling
        def take_screenshot():
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png", 
                filetypes=[("PNG files", "*.png")],
                title="Save Dashboard Screenshot"
            )
            if file_path:
                try:
                    # Add a small delay to ensure UI is fully rendered
                    chart_window.update()
                    chart_window.after(100)
                    
                    x = chart_window.winfo_rootx()
                    y = chart_window.winfo_rooty()
                    w = chart_window.winfo_width()
                    h = chart_window.winfo_height()
                    
                    screenshot = ImageGrab.grab(bbox=(x, y, x+w, y+h))
                    screenshot.save(file_path)
                    messagebox.showinfo("Success", "Dashboard screenshot saved successfully!")
                except Exception as screenshot_error:
                    messagebox.showerror("Screenshot Error", f"Failed to save screenshot: {screenshot_error}")
        
        
        downloadBtn = create_button(button_frame, "Download", take_screenshot, '#2196F3')
        downloadBtn.config(fg='black')
        downloadBtn.grid(row=0, column=0, padx=20)

        # Exit Button
        exitBtn = create_button(button_frame, "Close", chart_window.destroy, '#FF5722')
        exitBtn.config(fg='black')
        exitBtn.grid(row=0, column=1, padx=20)
        
        # Make the window modal
        chart_window.transient()
        chart_window.grab_set()
        chart_window.focus_set()
        chart_window.wait_window()
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while displaying the charts: {e}")
        print(f"Detailed error: {e}")  # Print to console for debugging


def job_recommendation(top, aplcnt_name, cv_path, user_info, selected_job_role=None):
    if not cv_path:
        messagebox.showerror("File Error", "Please select a resume file.")
        return

    if top:
        top.withdraw()

    parsed_data = parse_resume(cv_path)
    gender, age = user_info[0], user_info[1]

    # Resume Data Extraction
    contact = parsed_data.get('mobile_number', 'Not found')
    skills = parsed_data.get('skills', [])
    skills_text = ", ".join(skills) if skills else 'Not found'
    email = parsed_data.get('email', 'Not found')
    linkedin_url = parsed_data.get('linkedin', None)
    certifications = parsed_data.get('certifications', 'No certifications found')
    degree = parsed_data.get('degree', 'Not found')
    experience = parsed_data.get('experience', 'No experience details found')

    job_match_data = {
        role: calculate_job_role_match(skills, required_skills)
        for role, required_skills in job_roles.items()
    }

    # Prioritize selected job role
    if selected_job_role and selected_job_role in job_match_data:
        # Put selected role first, then others by match percentage
        selected_match = (selected_job_role, job_match_data[selected_job_role])
        other_matches = sorted(
            [(role, pct) for role, pct in job_match_data.items() if role != selected_job_role],
            key=lambda x: x[1], reverse=True
        )
        sorted_job_matches = [selected_match] + other_matches
    else:
        sorted_job_matches = sorted(job_match_data.items(), key=lambda x: x[1], reverse=True)

    top_job_matches = sorted_job_matches[:3]

    job_role_match_text = f"Best match: {top_job_matches[0][0]} ({top_job_matches[0][1]:.1f}%)"
    interview_readiness_score = calculate_interview_readiness(experience, certifications, skills)
    top_job, _ = top_job_matches[0]
    industry_benchmark = industry_benchmark_comparison(skills, top_job)
    resume_text = experience
    soft_skills_evaluation = evaluate_soft_skills(resume_text)

    # Main Window
    result = tk.Tk()
    result.title("Job Recommendation Results")
    result.geometry("1000x700")
    result.configure(bg='white')

    # Fonts
    title_font = Font(family='Helvetica', size=20, weight='bold')
    label_font = Font(family='Helvetica', size=12, weight='bold')
    text_font = Font(family='Helvetica', size=12)

    # Scrollable Canvas Frame
    container = ttk.Frame(result)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg='white')
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    ttk.Label(scrollable_frame, text="Job Recommendation Results", font=title_font, foreground='green').grid(row=0, column=0, columnspan=2, pady=15)

    # Candidate Info
    info_frame = ttk.LabelFrame(scrollable_frame, text="Candidate Information", padding=10)
    info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

    info_items = [
        ("Name", aplcnt_name.get()),
        ("Age", age),
        ("Contact", contact),
        ("Email", email),
        ("Degree", degree),
        ("Experience", experience[:100] + ('...' if len(experience) > 100 else '')),
        ("Skills", skills_text),
    ]

    for i, (label, value) in enumerate(info_items):
        ttk.Label(info_frame, text=f"{label}:", font=label_font).grid(row=i, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(info_frame, text=value, font=text_font).grid(row=i, column=1, sticky='w', padx=5, pady=2)

    # Job Match Frame
    match_frame = ttk.LabelFrame(scrollable_frame, text="Top Job Matches", padding=10)
    match_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

    for i, (job, match) in enumerate(top_job_matches):
        color = '#006400' if match > 70 else '#FFA500' if match > 50 else '#8B0000'
        ttk.Label(match_frame, text=f"{i + 1}. {job}: {match:.1f}%", foreground='light grey', font=text_font).grid(row=i, column=0, sticky='w', pady=2)

    # Analysis Frame
    analysis_frame = ttk.LabelFrame(scrollable_frame, text="Candidate Analysis", padding=10)
    analysis_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

    analysis_items = [
        ("Interview Readiness Score", interview_readiness_score),
        ("Industry Benchmark", industry_benchmark),
        ("Soft Skills Evaluation", soft_skills_evaluation),
    ]

    for i, (label, value) in enumerate(analysis_items):
        ttk.Label(analysis_frame, text=f"{label}:", font=label_font).grid(row=i, column=0, sticky='nw', padx=5, pady=3)
        ttk.Label(analysis_frame, text=value, font=text_font, wraplength=800).grid(row=i, column=1, sticky='w', padx=5, pady=3)

    # Recommendations
    recommendations_frame = ttk.LabelFrame(scrollable_frame, text="Recommendations", padding=10)
    recommendations_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

    top_job, _ = top_job_matches[0]
    required_skills = set(job_roles[top_job])
    candidate_skills = set(skills)
    missing_skills = required_skills - candidate_skills

    if missing_skills:
        rec_text = f"To improve match for {top_job}, develop skills in: {', '.join(missing_skills)}"
    else:
        rec_text = f"You have all the required skills for {top_job}."

    ttk.Label(recommendations_frame, text=rec_text, font=text_font, wraplength=900).grid(row=0, column=0, sticky='w')

    # Screenshot
    def take_screenshot():
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            x = result.winfo_rootx()
            y = result.winfo_rooty()
            w = x + result.winfo_width()
            h = y + result.winfo_height()
            ImageGrab.grab().crop((x, y, w, h)).save(file_path)
            messagebox.showinfo("Screenshot Saved", "Screenshot saved successfully!")

    def open_linkedin():
        if linkedin_url:
            webbrowser.open(linkedin_url)
        else:
            messagebox.showinfo("LinkedIn Profile", "No LinkedIn profile found.")

    def back_to_form():
        result.destroy()
        show_job_form()

    # Button Bar
    button_frame = ttk.Frame(scrollable_frame, padding=10)
    button_frame.grid(row=6, column=0, columnspan=2, pady=20)

    if linkedin_url:
        ttk.Button(button_frame, text="View LinkedIn", command=open_linkedin).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="View Analytics", command=lambda: show_charts(job_match_data, skills, job_roles[top_job], interview_readiness_score)).grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="Back", command=back_to_form).grid(row=0, column=2, padx=10)
        ttk.Button(button_frame, text="Exit", command=result.destroy).grid(row=0, column=3, padx=10)
    else:
        ttk.Button(button_frame, text="View Analytics", command=lambda: show_charts(job_match_data, skills, job_roles[top_job], interview_readiness_score)).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Back", command=back_to_form).grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="Exit", command=result.destroy).grid(row=0, column=2, padx=10)

    result.mainloop()

# Function to show the job recommendation form
def show_job_form():
    form = Tk()
    form.geometry("650x700")
    form.configure(background='#f5f5f5')
    form.title("Job Role Recommendation System Via Resume")
    
    # Add a custom font
    form.option_add("*Font", "Helvetica 12")
    
    # Banner with gradient effect
    banner_frame = Frame(form, height=120, bg='#2E7D32')
    banner_frame.pack(fill="x", pady=(0, 25))
    
    # Add logo placeholder
    logo_frame = Frame(banner_frame, bg='#2E7D32', width=80, height=80)
    logo_frame.place(relx=0.1, rely=0.5, anchor='center')
    Label(logo_frame, text="JM", font=("Helvetica", 28, "bold"), fg='white', bg='#4CAF50', 
          width=3, height=1, relief="raised", borderwidth=2).pack(padx=5, pady=5)
    
    banner_label = Label(banner_frame, text="JOB SEEKER DASHBOARD", foreground='white', bg='#2E7D32', 
                         font=("Helvetica", 28, "bold"))
    banner_label.place(relx=0.5, rely=0.5, anchor='center')
    
    # Add a tagline
    tagline = Label(form, text="Your path to career success starts here", 
                    fg='#555555', bg='#f5f5f5', font=("Helvetica", 12, "italic"))
    tagline.pack(pady=(0, 10))
    
    # Create a card-like container for the form
    card_frame = Frame(form, bg='white', relief="raised", borderwidth=1)
    card_frame.pack(fill="both", expand=True, padx=40, pady=20)
    
    # Add some padding inside the card
    input_frame = Frame(card_frame, background='white', padx=30, pady=25)
    input_frame.pack(fill="both", expand=True)
    
    # Form title with underline effect
    form_title = Label(input_frame, text="Enter Your Details", foreground='#2E7D32', bg='white', 
                      font=("Helvetica", 18, "bold"))
    form_title.grid(row=0, column=0, columnspan=2, pady=(0, 8), sticky="w")
    
    # Add separator under title
    separator = Frame(input_frame, height=2, bg='#4CAF50')
    separator.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 25))
    
    # Form labels and entries with improved styling
    labels = ["Full Name", "Age"]
    entries = []
    
    for i, label in enumerate(labels):
        Label(input_frame, text=label, foreground='#555555', bg='white', 
              font=("Helvetica", 12, "bold")).grid(row=i+2, column=0, sticky="w", pady=12)
        
        # Create a frame for each entry to add bottom border effect
        entry_frame = Frame(input_frame, background='white')
        entry_frame.grid(row=i+2, column=1, sticky="w", pady=12)
        
        entry = Entry(entry_frame, font=("Helvetica", 12), width=30, relief="flat", bg='#f9f9f9', fg='black')
        entry.pack(fill="x", ipady=8)
        entries.append(entry)
        
        # Add a separator for the bottom border effect
        Frame(entry_frame, height=1, bg='#cccccc').pack(fill="x")
    
    # Gender selection with improved radio buttons
    Label(input_frame, text="Gender", foreground='#555555', bg='white', 
          font=("Helvetica", 12, "bold")).grid(row=4, column=0, sticky="w", pady=12)
    
    gender = StringVar()
    gender.set("Male")
    
    gender_frame = Frame(input_frame, bg='white')
    gender_frame.grid(row=4, column=1, sticky="w", pady=12)
    
    style_rb = {"bg": 'white', "fg": '#333333', "selectcolor": '#4CAF50', "font": ("Helvetica", 12),
                "activebackground": 'white', "activeforeground": '#4CAF50', "padx": 10}
    
    Radiobutton(gender_frame, text="Male", variable=gender, value="Male", **style_rb).pack(side=LEFT, padx=(0, 20))
    Radiobutton(gender_frame, text="Female", variable=gender, value="Female", **style_rb).pack(side=LEFT)

        
    
    # Resume upload button with improved styling
    # Job Role Selection Dropdown - NEW CODE
    Label(input_frame, text="Select Job Role", foreground='#555555', bg='white', 
      font=("Helvetica", 12, "bold")).grid(row=5, column=0, sticky="w", pady=12)

    job_role_var = StringVar()
    job_roles_list = list(job_roles.keys())
    job_role_var.set(job_roles_list[0])

    job_dropdown_frame = Frame(input_frame, bg='white')
    job_dropdown_frame.grid(row=5, column=1, sticky="w", pady=12)

    job_dropdown = ttk.Combobox(job_dropdown_frame, textvariable=job_role_var,
                            values=job_roles_list, font=("Helvetica", 12),
                            width=28, state="readonly")
    job_dropdown.pack(fill="x", ipady=4)

# Resume upload button with improved styling
    Label(input_frame, text="Upload Resume", foreground='#555555', bg='white', 
      font=("Helvetica", 12, "bold")).grid(row=6, column=0, sticky="w", pady=18)
    
    upload_frame = Frame(input_frame, bg='white')
    upload_frame.grid(row=6, column=1, sticky="w", pady=18)
    
    cv_button = Button(upload_frame, text="Browse Files", command=lambda: OpenFile(cv_button), 
                     font=("Helvetica", 12), bg='#E3F2FD', fg='#1976D2', relief="flat",
                     activebackground='#BBDEFB', activeforeground='#1976D2',
                     padx=15, pady=8, borderwidth=0)
    cv_button.pack(side=LEFT)
    
    # Add file info label
    Label(upload_frame, text="No file selected", fg='black', bg='white', 
          font=("Helvetica", 10, "italic")).pack(side=LEFT, padx=15)
    
    # Button frame for submit and exit
    button_frame = Frame(input_frame, bg='white')
    button_frame.grid(row=7, column=0, columnspan=2, pady=25)
    
    # Submit button with improved styling
    submit_button = Button(button_frame, text="Analyze Resume", 
                     command=lambda: validate_and_submit(entries, gender, cv_button, job_role_var),
                         font=("Helvetica", 14, "bold"), bg='#4CAF50', fg='black', 
                         activebackground='#2E7D32', activeforeground='white',
                         padx=20, pady=10, relief="flat", borderwidth=0)
    submit_button.pack(side=LEFT, padx=(0, 15))
    
    # Add hover effect to submit button
    submit_button.bind("<Enter>", lambda e: e.widget.config(background='#388E3C'))
    submit_button.bind("<Leave>", lambda e: e.widget.config(background='#4CAF50'))
    
    # Exit button with improved styling
    exit_button = Button(button_frame, text="Exit", command=form.destroy, 
                       font=("Helvetica", 14), bg='#FFEBEE', fg='#D32F2F',
                       activebackground='#FFCDD2', activeforeground='#D32F2F',
                       padx=20, pady=10, relief="flat", borderwidth=0)
    exit_button.pack(side=LEFT)
    
    # Add hover effect to exit button
    exit_button.bind("<Enter>", lambda e: e.widget.config(background='#FFCDD2'))
    exit_button.bind("<Leave>", lambda e: e.widget.config(background='#FFEBEE'))
    
    # Add a footer
    # footer = Label(form, text="©️ 2025 Resume Analyzer - All Rights Reserved", 
    #              fg='#777777', bg='#f5f5f5', font=("Helvetica", 10))
    # footer.pack(pady=15)
    
    # Center the window on screen
    form.update_idletasks()
    width = form.winfo_width()
    height = form.winfo_height()
    x = (form.winfo_screenwidth() // 2) - (width // 2)
    y = (form.winfo_screenheight() // 2) - (height // 2)
    form.geometry(f'{width}x{height}+{x}+{y}')
    
    form.mainloop()

# Main function to start the application
# Main function to start the application
def main():
    show_entrance_screen()  # Start with entrance screen instead of job form

if __name__ == "__main__":
    main()