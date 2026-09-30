# Cybersecurity Risk Assessment Framework for Small Businesses
# Desktop GUI using tkinter (comes with Python, no extra install)

from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

# List of common cybersecurity risks to assess
RISKS = [
    "Phishing",
    "Ransomware",
    "Insider Threat",
    "Weak Passwords",
    "Data Theft",
]

# Simple recommendations for each risk
RECOMMENDATIONS = {
    "Phishing": "Train staff to spot suspicious emails. Do not click unknown links.",
    "Ransomware": "Keep backups offline. Update software and avoid unknown files.",
    "Insider Threat": "Give staff only the access they need. Review accounts regularly.",
    "Weak Passwords": "Use strong unique passwords and enable two-factor authentication.",
    "Data Theft": "Encrypt important data and limit who can copy or share files.",
}

SCORE_CHOICES = ["1", "2", "3", "4", "5"]


def classify_risk(score):
    """Turn a risk score into Low, Medium, or High."""
    if score <= 5:
        return "Low"
    elif score <= 12:
        return "Medium"
    else:
        return "High"


def extra_action(level):
    """Give a short next step based on the risk level."""
    if level == "High":
        return "Act immediately. Fix this risk first."
    if level == "Medium":
        return "Plan improvements within a few weeks."
    return "Keep current controls and review later."


def overall_level(average_score):
    """Classify the whole business using the average score."""
    return classify_risk(round(average_score))


def build_report_text(business_name, business_type, date_time, results):
    """Create the full report as one string for the screen and file."""
    lines = []
    lines.append("=" * 50)
    lines.append("ASSESSMENT SUMMARY")
    lines.append("=" * 50)
    lines.append("Business Name: " + business_name)
    lines.append("Business Type: " + business_type)
    lines.append("Date and Time: " + date_time)
    lines.append("")

    ranked = sorted(results, key=lambda item: item["score"], reverse=True)

    high_count = 0
    medium_count = 0
    low_count = 0
    total_score = 0

    for item in ranked:
        total_score += item["score"]
        if item["level"] == "High":
            high_count += 1
        elif item["level"] == "Medium":
            medium_count += 1
        else:
            low_count += 1

        lines.append(item["risk"])
        lines.append("  Likelihood: " + str(item["likelihood"]))
        lines.append("  Impact: " + str(item["impact"]))
        lines.append("  Score: " + str(item["score"]) + " | Level: " + item["level"])
        lines.append("  Recommendation: " + item["advice"])
        lines.append("  Next step: " + extra_action(item["level"]))
        lines.append("")

    average_score = total_score / len(ranked)
    top_risk = ranked[0]

    lines.append("-" * 50)
    lines.append("OVERALL RESULT")
    lines.append("-" * 50)
    lines.append("High risks: " + str(high_count))
    lines.append("Medium risks: " + str(medium_count))
    lines.append("Low risks: " + str(low_count))
    lines.append("Average score: " + str(round(average_score, 1)))
    lines.append("Overall level: " + overall_level(average_score))
    lines.append("Highest priority: " + top_risk["risk"] + " (score " + str(top_risk["score"]) + ")")
    lines.append("")
    lines.append("Assessment complete.")
    return "\n".join(lines)


class RiskApp:
    """Main window for the risk assessment tool."""

    def __init__(self, window):
        self.window = window
        self.window.title("Cybersecurity Risk Assessment Framework")
        self.window.geometry("820x720")
        self.window.minsize(700, 600)

        self.report_text = ""
        self.business_name_for_file = ""

        self.name_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.likelihood_vars = {}
        self.impact_vars = {}

        self.build_layout()

    def build_layout(self):
        """Create all labels, boxes, and buttons on the window."""
        title = tk.Label(
            self.window,
            text="Cybersecurity Risk Assessment Framework\nfor Small Businesses",
            font=("Segoe UI", 14, "bold"),
            justify="center",
        )
        title.pack(pady=(12, 8))

        form = ttk.Frame(self.window, padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Business name:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.name_var, width=40).grid(row=0, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(form, text="Business type:").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.type_var, width=40).grid(row=1, column=1, sticky="w", padx=4, pady=4)

        help_label = tk.Label(
            self.window,
            text="For each risk, choose Likelihood and Impact from 1 (lowest) to 5 (highest).",
            font=("Segoe UI", 9),
        )
        help_label.pack(pady=(0, 6))

        table = ttk.Frame(self.window, padding=10)
        table.pack(fill="x")

        ttk.Label(table, text="Risk", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=6, pady=4, sticky="w")
        ttk.Label(table, text="Likelihood (1-5)", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=6, pady=4)
        ttk.Label(table, text="Impact (1-5)", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=6, pady=4)

        for index, risk in enumerate(RISKS, start=1):
            ttk.Label(table, text=risk).grid(row=index, column=0, padx=6, pady=4, sticky="w")

            like_var = tk.StringVar(value="1")
            impact_var = tk.StringVar(value="1")
            self.likelihood_vars[risk] = like_var
            self.impact_vars[risk] = impact_var

            ttk.Combobox(
                table,
                textvariable=like_var,
                values=SCORE_CHOICES,
                state="readonly",
                width=8,
            ).grid(row=index, column=1, padx=6, pady=4)

            ttk.Combobox(
                table,
                textvariable=impact_var,
                values=SCORE_CHOICES,
                state="readonly",
                width=8,
            ).grid(row=index, column=2, padx=6, pady=4)

        buttons = ttk.Frame(self.window, padding=10)
        buttons.pack(fill="x")

        ttk.Button(buttons, text="Calculate Assessment", command=self.calculate).pack(side="left", padx=4)
        ttk.Button(buttons, text="Scoring Guide", command=self.show_scoring_guide).pack(side="left", padx=4)
        ttk.Button(buttons, text="Save Report", command=self.save_report).pack(side="left", padx=4)
        ttk.Button(buttons, text="Clear", command=self.clear_form).pack(side="left", padx=4)

        ttk.Label(self.window, text="Results").pack(anchor="w", padx=14)

        self.output = ScrolledText(self.window, wrap="word", height=16, font=("Consolas", 10))
        self.output.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.output.config(state="disabled")

    def show_scoring_guide(self):
        """Show a popup that explains how scoring works."""
        messagebox.showinfo(
            "Scoring Guide",
            "Likelihood: 1 = rare, 5 = very likely\n"
            "Impact: 1 = small harm, 5 = severe harm\n\n"
            "Risk Score = Likelihood x Impact\n\n"
            "1-5   = Low\n"
            "6-12  = Medium\n"
            "13-25 = High",
        )

    def calculate(self):
        """Read the form, calculate scores, and show the summary."""
        business_name = self.name_var.get().strip()
        business_type = self.type_var.get().strip()

        if business_name == "" or business_type == "":
            messagebox.showerror("Missing details", "Please enter the business name and business type.")
            return

        results = []
        for risk in RISKS:
            likelihood = int(self.likelihood_vars[risk].get())
            impact = int(self.impact_vars[risk].get())

            if likelihood < 1 or likelihood > 5 or impact < 1 or impact > 5:
                messagebox.showerror("Invalid score", "Each score must be a number from 1 to 5.")
                return

            risk_score = likelihood * impact
            level = classify_risk(risk_score)

            results.append({
                "risk": risk,
                "likelihood": likelihood,
                "impact": impact,
                "score": risk_score,
                "level": level,
                "advice": RECOMMENDATIONS[risk],
            })

        date_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.report_text = build_report_text(business_name, business_type, date_time, results)
        self.business_name_for_file = business_name
        self.show_report(self.report_text)

    def show_report(self, text):
        """Put the report into the results box."""
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text)
        self.output.config(state="disabled")

    def save_report(self):
        """Save the current report as a .txt file chosen by the user."""
        if self.report_text == "":
            messagebox.showwarning("No report yet", "Please calculate an assessment before saving.")
            return

        safe_name = self.business_name_for_file.replace(" ", "_")
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = "risk_report_" + safe_name + "_" + stamp + ".txt"

        file_path = filedialog.asksaveasfilename(
            title="Save report",
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )

        if file_path == "":
            return

        report_file = open(file_path, "w", encoding="utf-8")
        report_file.write(self.report_text)
        report_file.write("\n")
        report_file.close()

        messagebox.showinfo("Saved", "Report saved successfully.")

    def clear_form(self):
        """Reset the form so another business can be assessed."""
        self.name_var.set("")
        self.type_var.set("")
        for risk in RISKS:
            self.likelihood_vars[risk].set("1")
            self.impact_vars[risk].set("1")
        self.report_text = ""
        self.business_name_for_file = ""
        self.show_report("")


def main():
    window = tk.Tk()
    RiskApp(window)
    window.mainloop()


if __name__ == "__main__":
    main()
