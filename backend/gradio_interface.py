import gradio as gr
import requests
import json

def analyze_sentiment(feedback_text):
    """Analyze employee feedback sentiment"""
    try:
        response = requests.post(
            "http://localhost:8000/api/v2/ai/sentiment-analysis",
            params={"feedback_text": feedback_text}
        )
        result = response.json()
        return f"Sentiment: {result['sentiment']}\nConfidence: {result['confidence']}\nRisk Level: {result['risk_level']}"
    except:
        return "Error analyzing sentiment"

def calculate_epf(salary):
    """Calculate EPF contributions"""
    try:
        response = requests.post(
            "http://localhost:8000/api/epf-calculator",
            json={"basic_salary": float(salary)}
        )
        result = response.json()
        return f"Employee: RM{result['employee_share']}\nEmployer: RM{result['employer_share']}\nTotal: RM{result['total']}"
    except:
        return "Error calculating EPF"

def predict_attrition(employee_id):
    """Predict employee attrition"""
    try:
        response = requests.get(f"http://localhost:8000/api/v2/ai/attrition-prediction/{employee_id}")
        result = response.json()
        return f"Risk: {result['risk_level']}\nProbability: {result['attrition_probability']}\nRecommendations: {', '.join(result['recommendations'])}"
    except:
        return "Error predicting attrition"

# Create Gradio interface
with gr.Blocks(title="HRMS Malaysia AI Interface") as demo:
    gr.Markdown("# 🇲🇾 HRMS Malaysia - AI Interface")
    
    with gr.Tab("Sentiment Analysis"):
        feedback_input = gr.Textbox(label="Employee Feedback", placeholder="Enter employee feedback...")
        sentiment_output = gr.Textbox(label="Analysis Result")
        sentiment_btn = gr.Button("Analyze Sentiment")
        sentiment_btn.click(analyze_sentiment, inputs=feedback_input, outputs=sentiment_output)
    
    with gr.Tab("EPF Calculator"):
        salary_input = gr.Number(label="Basic Salary (RM)", value=5000)
        epf_output = gr.Textbox(label="EPF Calculation")
        epf_btn = gr.Button("Calculate EPF")
        epf_btn.click(calculate_epf, inputs=salary_input, outputs=epf_output)
    
    with gr.Tab("Attrition Prediction"):
        employee_input = gr.Textbox(label="Employee ID", placeholder="EMP123456")
        attrition_output = gr.Textbox(label="Attrition Prediction")
        attrition_btn = gr.Button("Predict Attrition")
        attrition_btn.click(predict_attrition, inputs=employee_input, outputs=attrition_output)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)