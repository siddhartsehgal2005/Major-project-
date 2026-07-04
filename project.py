import tkinter as tk
from tkinter import ttk, messagebox

MIN_ATTENDANCE = 75
SUBJECTS = {
    "Math": (60, 20),
    "Physics": (50, 25),
    "Chemistry": (40, 30),
    "Computer": (70, 40),
}
STUDENTS = {
    "Dhiraj": {
        "Math": (40, 15),
        "Physics": (30, 20),
        "Chemistry": (25, 20),
        "Computer": (50, 30),
    },
    "Priya": {
        "Math": (50, 18),
        "Physics": (40, 22),
        "Chemistry": (30, 25),
        "Computer": (60, 35),
    },
    "Aman": {
        "Math": (30, 10),
        "Physics": (20, 15),
        "Chemistry": (15, 10),
        "Computer": (40, 20),
    },
}


def get_attendance_marks(avg_att):
    if avg_att >= 95:
        return 6
    if avg_att >= 90:
        return 5
    if avg_att >= 85:
        return 4
    if avg_att >= 80:
        return 3
    if avg_att >= 75:
        return 2
    return 0


def build_report_data(student_name):
    if student_name not in STUDENTS:
        raise ValueError("Student not found")

    rows = []
    for subject in SUBJECTS:
        total_lec, total_lab = SUBJECTS[subject]
        att_lec, att_lab = STUDENTS[student_name][subject]

        lec_per = att_lec * 100 / total_lec
        lab_per = att_lab * 100 / total_lab
        avg_att = (lec_per + lab_per) / 2

        req_lec = (total_lec * MIN_ATTENDANCE + 99) // 100
        req_lab = (total_lab * MIN_ATTENDANCE + 99) // 100

        need_lec = max(0, req_lec - att_lec)
        need_lab = max(0, req_lab - att_lab)

        rem_lec = total_lec - att_lec
        rem_lab = total_lab - att_lab

        rows.append(
            {
                "subject": subject,
                "lecture_percentage": round(lec_per, 2),
                "lab_percentage": round(lab_per, 2),
                "average_percentage": round(avg_att, 2),
                "attendance_marks": get_attendance_marks(avg_att),
                "need_lec": need_lec,
                "need_lab": need_lab,
                "remaining_lec": rem_lec,
                "remaining_lab": rem_lab,
                "lecture_status": "Possible" if need_lec <= rem_lec else "Not Possible",
                "lab_status": "Possible" if need_lab <= rem_lab else "Not Possible",
            }
        )
    return rows


class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Report Dashboard")
        self.root.geometry("1120x650")
        self.root.minsize(940, 560)
        self.root.configure(bg="#f3f6fb")
        self.root.option_add("*Font", "Arial 10")

        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("TFrame", background="#f3f6fb")
        style.configure("Card.TFrame", background="#ffffff", relief="groove", borderwidth=1)
        style.configure("TLabel", background="#f3f6fb", foreground="#22354c")
        style.configure("Title.TLabel", font=("Arial", 20, "bold"), foreground="#16324f", background="#f3f6fb")
        style.configure("SubTitle.TLabel", font=("Arial", 10), foreground="#4b5d73", background="#f3f6fb")
        style.configure("Accent.TButton", font=("Arial", 10, "bold"), background="#2563eb", foreground="white")
        style.map("Accent.TButton", background=[("active", "#1d4ed8"), ("pressed", "#1e40af")])
        style.configure("TCombobox", padding=6)
        style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="#22354c", rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#dbeafe", foreground="#16324f")
        style.map("Treeview", background=[("selected", "#60a5fa")], foreground=[("selected", "white")])

        header_frame = ttk.Frame(root, padding=(0, 0, 0, 12))
        header_frame.pack(fill="x")
        ttk.Label(header_frame, text="Student Attendance Report", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header_frame, text="Review attendance performance, required classes, and status at a glance.", style="SubTitle.TLabel").pack(anchor="w", pady=(4, 0))

        card = ttk.Frame(root, style="Card.TFrame", padding=16)
        card.pack(fill="x", pady=(0, 12))

        control_frame = ttk.Frame(card)
        control_frame.pack(fill="x")

        ttk.Label(control_frame, text="Select student:").pack(side="left")
        self.student_var = tk.StringVar()
        self.student_combo = ttk.Combobox(control_frame, textvariable=self.student_var, width=28, state="readonly")
        self.student_combo.pack(side="left", padx=(8, 10))
        self.student_combo["values"] = list(STUDENTS.keys())
        self.student_combo.current(0)

        ttk.Button(control_frame, text="Generate Report", style="Accent.TButton", command=self.show_report).pack(side="left")

        self.summary_var = tk.StringVar(value="Choose a student to view the report.")
        ttk.Label(card, textvariable=self.summary_var, foreground="#1f4e79", wraplength=900).pack(anchor="w", pady=(12, 0))

        table_frame = ttk.Frame(root, style="Card.TFrame", padding=8)
        table_frame.pack(fill="both", expand=True)

        columns = ("subject", "lecture", "lab", "average", "marks", "need", "remaining", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.heading("subject", text="Subject")
        self.tree.heading("lecture", text="Lecture %")
        self.tree.heading("lab", text="Lab %")
        self.tree.heading("average", text="Avg %")
        self.tree.heading("marks", text="Marks / 6")
        self.tree.heading("need", text="Need")
        self.tree.heading("remaining", text="Remaining")
        self.tree.heading("status", text="Status")

        self.tree.column("subject", width=140, anchor="center")
        self.tree.column("lecture", width=100, anchor="center")
        self.tree.column("lab", width=100, anchor="center")
        self.tree.column("average", width=100, anchor="center")
        self.tree.column("marks", width=100, anchor="center")
        self.tree.column("need", width=170, anchor="center")
        self.tree.column("remaining", width=170, anchor="center")
        self.tree.column("status", width=220, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def show_report(self):
        student_name = self.student_var.get().strip()
        if not student_name:
            messagebox.showwarning("Input required", "Please choose a student.")
            return

        try:
            rows = build_report_data(student_name)
        except ValueError as exc:
            messagebox.showerror("Not found", str(exc))
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in rows:
            self.tree.insert(
                "",
                "end",
                values=(
                    row["subject"],
                    f"{row['lecture_percentage']}%",
                    f"{row['lab_percentage']}%",
                    f"{row['average_percentage']}%",
                    f"{row['attendance_marks']}/6",
                    f"{row['need_lec']} lec, {row['need_lab']} lab",
                    f"{row['remaining_lec']} lec, {row['remaining_lab']} lab",
                    f"Lec: {row['lecture_status']} | Lab: {row['lab_status']}",
                ),
            )

        self.summary_var.set(f"{student_name} has an average attendance report across all subjects.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()