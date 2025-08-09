import torch
from transformers import AutoTokenizer, AutoModel
from typing import Dict, List
import time

class ModelOptimizer:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def benchmark_models(self, model_ids: List[str], test_texts: List[str]) -> Dict:
        """Benchmark multiple models for performance"""
        
        results = {}
        
        for model_id in model_ids:
            try:
                start_time = time.time()
                
                # Load model
                tokenizer = AutoTokenizer.from_pretrained(model_id)
                model = AutoModel.from_pretrained(model_id)
                model.to(self.device)
                
                load_time = time.time() - start_time
                
                # Test inference
                inference_times = []
                for text in test_texts:
                    start_inference = time.time()
                    
                    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
                    inputs = {k: v.to(self.device) for k, v in inputs.items()}
                    
                    with torch.no_grad():
                        outputs = model(**inputs)
                    
                    inference_times.append(time.time() - start_inference)
                
                results[model_id] = {
                    "load_time": round(load_time, 3),
                    "avg_inference_time": round(sum(inference_times) / len(inference_times), 3),
                    "model_size_mb": self._get_model_size(model),
                    "device": self.device,
                    "status": "success"
                }
                
            except Exception as e:
                results[model_id] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results
    
    def _get_model_size(self, model) -> float:
        """Calculate model size in MB"""
        param_size = 0
        for param in model.parameters():
            param_size += param.nelement() * param.element_size()
        
        buffer_size = 0
        for buffer in model.buffers():
            buffer_size += buffer.nelement() * buffer.element_size()
        
        size_mb = (param_size + buffer_size) / 1024 / 1024
        return round(size_mb, 2)
    
    def optimize_for_production(self, model_id: str) -> Dict:
        """Optimize model for production deployment"""
        
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            model = AutoModel.from_pretrained(model_id)
            
            # Optimization techniques
            optimizations = {}
            
            # 1. Model quantization (if supported)
            try:
                quantized_model = torch.quantization.quantize_dynamic(
                    model, {torch.nn.Linear}, dtype=torch.qint8
                )
                optimizations["quantization"] = "Applied INT8 quantization"
            except:
                optimizations["quantization"] = "Not supported"
            
            # 2. TorchScript compilation
            try:
                model.eval()
                example_input = tokenizer("Sample text", return_tensors="pt")
                traced_model = torch.jit.trace(model, (example_input["input_ids"],))
                optimizations["torchscript"] = "Model traced successfully"
            except:
                optimizations["torchscript"] = "Tracing failed"
            
            # 3. ONNX export recommendation
            optimizations["onnx_export"] = "Recommended for CPU inference"
            
            return {
                "model_id": model_id,
                "optimizations": optimizations,
                "recommendations": [
                    "Use model quantization for faster inference",
                    "Consider ONNX export for production deployment",
                    "Implement model caching for repeated queries"
                ]
            }
            
        except Exception as e:
            return {"error": str(e)}

def analyze_huggingface_repository():
    """Main analysis function for HuggingFace repository"""
    
    analyzer = HuggingFaceAnalyzer()
    optimizer = ModelOptimizer()
    
    # Analyze available models
    model_analysis = analyzer.analyze_repository_models()
    
    # Test sentiment models
    sentiment_test = analyzer.test_sentiment_models()
    
    # Get recommendations
    recommendations = analyzer.recommend_models_for_hrms()
    
    # Benchmark key models
    key_models = [
        "cardiffnlp/twitter-roberta-base-sentiment-latest",
        "sentence-transformers/all-MiniLM-L6-v2"
    ]
    
    test_texts = [
        "Employee feedback about work environment",
        "Resume text for job matching analysis"
    ]
    
    benchmark_results = optimizer.benchmark_models(key_models, test_texts)
    
    return {
        "repository_analysis": {
            "available_models": model_analysis,
            "sentiment_testing": sentiment_test,
            "recommendations": recommendations,
            "performance_benchmarks": benchmark_results
        },
        "summary": {
            "total_models_analyzed": len(model_analysis),
            "recommended_models": len(recommendations),
            "benchmarked_models": len(benchmark_results)
        }
    }