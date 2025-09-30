import tkinter as tk
from tkinter import ttk, scrolledtext
from difflib import SequenceMatcher

class SimpleRAGSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("RAG System")
        self.root.geometry("800x600")
        
        # Sample passages (you can modify these)
        self.passages = [
            "Power BI is a tool for data visualization and reporting.",
            "Python is a programming language widely used for AI and automation.",
            "AWS offers cloud services such as EC2, S3, and Lambda.",
        ]
        self.setup_ui()
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="RAG System", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Question input
        question_label = ttk.Label(main_frame, text="Enter your question:")
        question_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.question_entry = ttk.Entry(main_frame, width=80)
        self.question_entry.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.question_entry.bind('<Return>', lambda event: self.ask_question())
        
        # Ask button
        ask_button = ttk.Button(main_frame, text="Ask Question", command=self.ask_question)
        ask_button.grid(row=2, column=1, padx=(10, 0), pady=(0, 10))
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Answer section
        answer_label = ttk.Label(results_frame, text="Answer:")
        answer_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.answer_text = scrolledtext.ScrolledText(results_frame, width=70, height=4, wrap=tk.WORD)
        self.answer_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.answer_text.config(state=tk.DISABLED)
        
        # Retrieved passage section
        passage_label = ttk.Label(results_frame, text="Most Relevant Passage:")
        passage_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.passage_text = scrolledtext.ScrolledText(results_frame, width=70, height=3, wrap=tk.WORD)
        self.passage_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.passage_text.config(state=tk.DISABLED)
        
        # Similarity score
        score_label = ttk.Label(results_frame, text="Similarity Score:")
        score_label.grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        
        self.score_var = tk.StringVar(value="Not calculated yet")
        score_value = ttk.Label(results_frame, textvariable=self.score_var)
        score_value.grid(row=4, column=1, sticky=tk.W, pady=(0, 5))
        
        # Passages frame
        passages_frame = ttk.LabelFrame(main_frame, text="Available Passages", padding="10")
        passages_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.passages_text = scrolledtext.ScrolledText(passages_frame, width=70, height=6, wrap=tk.WORD)
        self.passages_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add passages to the text widget
        for i, passage in enumerate(self.passages, 1):
            self.passages_text.insert(tk.END, f"{i}. {passage}\n\n")
        self.passages_text.config(state=tk.DISABLED)
        
        # Explanation frame
        explanation_frame = ttk.LabelFrame(main_frame, text="How This System Works", padding="10")
        explanation_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        explanation_text = """
1. SEARCH: The system compares your question with each passage using text similarity.
2. RETRIEVE: The passage with the highest similarity score is selected.
3. GENERATE: The system uses the retrieved passage to formulate an answer.

This is a simplified version of RAG (Retrieval-Augmented Generation) used in AI systems.
        """
        
        explanation_widget = scrolledtext.ScrolledText(explanation_frame, width=70, height=4, wrap=tk.WORD)
        explanation_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        explanation_widget.insert(tk.END, explanation_text)
        explanation_widget.config(state=tk.DISABLED)
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(4, weight=1)
        main_frame.rowconfigure(5, weight=1)
        results_frame.columnconfigure(0, weight=1)
        passages_frame.columnconfigure(0, weight=1)
        explanation_frame.columnconfigure(0, weight=1)

        
    def calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts using SequenceMatcher"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def ask_question(self):
        question = self.question_entry.get().strip()
        
        if not question:
            self.answer_text.config(state=tk.NORMAL)
            self.answer_text.delete(1.0, tk.END)
            self.answer_text.insert(tk.END, "Please enter a question.")
            self.answer_text.config(state=tk.DISABLED)
            return
        
        # Step 1: Search for the most relevant passage
        best_score = 0
        best_passage = ""
        best_index = -1
        
        for i, passage in enumerate(self.passages):
            score = self.calculate_similarity(question, passage)
            if score > best_score:
                best_score = score
                best_passage = passage
                best_index = i
        
        # Step 2: Retrieve the passage
        # Step 3: Generate an answer
        if best_score > 0.1:  # Minimum threshold
            answer = f"Based on the available information: {best_passage}"
        else:
            answer = "I couldn't find a relevant passage to answer your question."
        
        # Display results
        self.answer_text.config(state=tk.NORMAL)
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.END, answer)
        self.answer_text.config(state=tk.DISABLED)
        
        self.passage_text.config(state=tk.NORMAL)
        self.passage_text.delete(1.0, tk.END)
        self.passage_text.insert(tk.END, best_passage if best_index >= 0 else "No relevant passage found")
        self.passage_text.config(state=tk.DISABLED)
        
        self.score_var.set(f"{best_score:.2f}")

def main():
    root = tk.Tk()
    app = SimpleRAGSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()